import os
import base64
import json
from screen import capture_screen_with_cursor
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

api_key = os.environ.get("OPENAI_API_KEY")


client = OpenAI(
    api_key=api_key,
)


def get_operation(messages):
    print("[get_operation]")

    screenshots_dir = "screenshots"
    if not os.path.exists(screenshots_dir):
        os.makedirs(screenshots_dir)

    screenshot_filename = os.path.join(screenshots_dir, "screenshot.png")
    # Call the function to capture the screen with the cursor
    capture_screen_with_cursor(screenshot_filename)

    with open(screenshot_filename, "rb") as img_file:
        img_base64 = base64.b64encode(img_file.read()).decode("utf-8")

    vision_message = {
        "role": "user",
        "content": [
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
    print("[operate] preprocessed content", content)

    assistant_message = {"role": "assistant", "content": content}

    content = json.loads(content)
    print("[operate] processed content", content)

    messages.append(assistant_message)

    return content
