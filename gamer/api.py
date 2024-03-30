import os
import base64
import json
from datetime import datetime
from gamer.operating_system import OperatingSystem
from openai import OpenAI
from dotenv import load_dotenv
from gamer.utils import get_text_element, get_text_coordinates
from gamer.config import Config
from anthropic import Anthropic
import easyocr
from gamer.prompts import get_system_prompt

load_dotenv()

api_key = os.environ.get("OPENAI_API_KEY")
operating_system = OperatingSystem()

openai_client = OpenAI(
    api_key=api_key,
)
anthropic_client = Anthropic(
    # This is the default and can be omitted
    api_key=os.environ.get("ANTHROPIC_API_KEY"),
)


# Load configuration
config = Config()


def get_sm64_operation(model, messages):
    content, screenshot_filename = call_api("mario", model, messages)
    if config.debug:
        print("[multimodal-gamer] preprocessed content", content)

    content = clean_json(content)

    assistant_message = {"role": "assistant", "content": content}

    content = json.loads(content)

    messages.append(assistant_message)

    return content


def get_poker_operation(model, messages):
    content, screenshot_filename = call_api("poker", model, messages)

    content_str = content

    content_json = json.loads(content)
    action = content_json.get("action")
    print("action", action)

    action = action.lower()
    if action == "Wait" or action == "wait":

        return content_json
    elif action == "Continue" or action == "continue":
        print("action is continue")
        content_json["x"] = "0.50"
        content_json["y"] = "0.50"
        return content_json

    processed_content = process_ocr(
        messages, content_json, content_str, screenshot_filename
    )

    return processed_content


def get_chess_operation(model, messages):

    content, screenshot_filename = call_api("chess", model, messages)
    assistant_message = {"role": "assistant", "content": content}

    content = json.loads(content)

    messages.append(assistant_message)
    return content


# build this out for claude and gpt-4-vision-preview
def call_api(
    game,
    model,
    messages,
):
    if config.verbose:
        print("[call_api]")
        print("[call_api] len(messages)", len(messages))
        for i, message in enumerate(messages):
            if message["role"] != "user":
                print(f"message[{i}] => ", message["role"])

    screenshots_dir = "screenshots"
    if not os.path.exists(screenshots_dir):
        os.makedirs(screenshots_dir)

    # Use current date and time to create a unique filename
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    screenshot_filename = os.path.join(screenshots_dir, f"screenshot_{timestamp}.png")

    # Call the function to capture the screen with the cursor
    operating_system.capture_screen(screenshot_filename)

    with open(screenshot_filename, "rb") as img_file:
        img_base64 = base64.b64encode(img_file.read()).decode("utf-8")

    user_prompt = "See the screenshot of the game provide your next action. Only respond with the next action in valid json."

    system_prompt = get_system_prompt(game)
    if model == "gpt-4":

        system_message = {"role": "system", "content": system_prompt}
        # append the system message to the first index of `messages`
        messages.insert(0, system_message)
        vision_message = {
            "role": "user",
            "content": [
                {"type": "text", "text": user_prompt},
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/jpeg;base64,{img_base64}"},
                },
            ],
        }
        messages.append(vision_message)
        # now remove system prompt

        response = openai_client.chat.completions.create(
            model="gpt-4-vision-preview",
            messages=messages,
            presence_penalty=1,
            frequency_penalty=1,
            temperature=0.7,
            max_tokens=3000,
        )
        messages.pop(0)  # remove system prompt again

        content = response.choices[0].message.content
        if config.debug:
            print("[multimodal-gamer] preprocessed content", content)

        content = clean_json(content)
        print("type(content", type(content))

        return content, screenshot_filename
    elif model == "claude":
        vision_message = {
            "role": "user",
            "content": [
                {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": "image/png",  # TODO: double check this
                        "data": img_base64,
                    },
                },
                {"type": "text", "text": user_prompt},
            ],
        }
        messages.append(vision_message)

        message = anthropic_client.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=1024,
            system=system_prompt,
            messages=messages,
        )
        print("anthropic message", message.content)

        content = clean_json(message.content[0].text)

        return content, screenshot_filename
    else:
        Exception("Uh, we don't know that provider :(")


def process_ocr(messages, content, content_str, screenshot_filename):
    if config.verbose:
        print(
            "[process_ocr] content",
            content,
        )

    processed_content = None

    if config.verbose:
        print(
            "[process_ocr] operation",
            content,
        )

    text_to_click = content.get("action")

    if config.verbose:
        print(
            "[process_ocr] text_to_click",
            text_to_click,
        )
    # upcase the first letter of the text_to_click
    text_to_click = text_to_click[0].upper() + text_to_click[1:]

    # Initialize EasyOCR Reader
    reader = easyocr.Reader(["en"])

    # Read the screenshot
    result = reader.readtext(screenshot_filename)
    # if config.verbose:
    #     print("\n\n\n[process_ocr] results", result)
    #     print("\n\n\n")

    try:

        text_element_index = get_text_element(
            result, text_to_click, screenshot_filename
        )
        coordinates = get_text_coordinates(
            result, text_element_index, screenshot_filename
        )
    except Exception as e:
        print("[process_ocr] error:", e)
        print("[process_ocr] wait and try again")
        return {
            "thought": "It failed so I need to wait and try again",
            "action": "wait",
        }

    # add `coordinates`` to `content`
    content["x"] = coordinates["x"]
    content["y"] = coordinates["y"]

    if config.verbose:
        print(
            "[process_ocr] text_element_index",
            text_element_index,
        )
        print(
            "[process_ocr] coordinates",
            coordinates,
        )
        print(
            "[process_ocr] final content",
            content,
        )
    processed_content = content

    # wait to append the assistant message so that if the `processed_content` step fails we don't append a message and mess up message history
    assistant_message = {"role": "assistant", "content": content_str}
    messages.append(assistant_message)

    return processed_content


def clean_json(content):
    if content.startswith("```json"):
        content = content[
            len("```json") :
        ].strip()  # Remove starting ```json and trim whitespace
    elif content.startswith("```"):
        content = content[
            len("```") :
        ].strip()  # Remove starting ``` and trim whitespace
    if content.endswith("```"):
        content = content[
            : -len("```")
        ].strip()  # Remove ending ``` and trim whitespace

    # Normalize line breaks and remove any unwanted characters
    content = "\n".join(line.strip() for line in content.splitlines())

    return content


def reflection(model, messages):
    # TODO: implement reflection that checks the action for correctness
    # Source: https://www.youtube.com/watch?v=sal78ACtGTc&t=308s
    return
