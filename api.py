import os
import base64
import json
from operating_system import OperatingSystem
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

api_key = os.environ.get("OPENAI_API_KEY")
operating_system = OperatingSystem()

client = OpenAI(
    api_key=api_key,
)

debug = False


def get_operation(messages):
    if debug:
        print("[multimodal-gamer] get_operation")

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
        max_tokens=3000,
    )

    content = response.choices[0].message.content
    if debug:
        print("[multimodal-gamer] preprocessed content", content)

    content = clean_json(content)

    assistant_message = {"role": "assistant", "content": content}

    content = json.loads(content)

    messages.append(assistant_message)

    return content


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
