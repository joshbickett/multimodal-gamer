import os
import base64
import json
from gamer.operating_system import OperatingSystem
from openai import OpenAI
from dotenv import load_dotenv
from gamer.utils import get_text_element, get_text_coordinates
from gamer.config import Config
import easyocr

load_dotenv()

api_key = os.environ.get("OPENAI_API_KEY")
operating_system = OperatingSystem()

client = OpenAI(
    api_key=api_key,
)

# Load configuration
config = Config()


def get_sm64_operation(messages):
    if config.verbose:
        print("[multimodal-gamer] get_sm64_operation")

    screenshots_dir = "screenshots"
    if not os.path.exists(screenshots_dir):
        os.makedirs(screenshots_dir)

    screenshot_filename = os.path.join(screenshots_dir, "screenshot.png")
    # Call the function to capture the screen with the cursor
    operating_system.capture_screen(screenshot_filename)

    with open(screenshot_filename, "rb") as img_file:
        img_base64 = base64.b64encode(img_file.read()).decode("utf-8")

    user_prompt = "See the screenshot of the game provide your next action. Only respond with the next action in valid json."

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

    response = client.chat.completions.create(
        model="gpt-4-vision-preview",
        messages=messages,
        presence_penalty=1,
        frequency_penalty=1,
        temperature=0.7,
        max_tokens=3000,
    )

    content = response.choices[0].message.content
    if config.verbose:
        print("[multimodal-gamer] preprocessed content", content)

    content = clean_json(content)

    assistant_message = {"role": "assistant", "content": content}

    content = json.loads(content)

    messages.append(assistant_message)

    return content


def get_poker_operation(messages):
    if config.verbose:
        print("[multimodal-gamer] get_poker_operation")

    screenshots_dir = "screenshots"
    if not os.path.exists(screenshots_dir):
        os.makedirs(screenshots_dir)

    screenshot_filename = os.path.join(screenshots_dir, "screenshot.png")
    # Call the function to capture the screen with the cursor
    operating_system.capture_screen(screenshot_filename)

    with open(screenshot_filename, "rb") as img_file:
        img_base64 = base64.b64encode(img_file.read()).decode("utf-8")

    user_prompt = "See the screenshot of the game provide your next action. Only respond with the next action in valid json."

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

    response = client.chat.completions.create(
        model="gpt-4-vision-preview",
        messages=messages,
        presence_penalty=1,
        frequency_penalty=1,
        temperature=0.7,
        max_tokens=3000,
    )

    content = response.choices[0].message.content
    if config.verbose:
        print("[multimodal-gamer] preprocessed content", content)

    content = clean_json(content)

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
    #     print(
    #         "[process_ocr] result",
    #         result,
    #     )
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
