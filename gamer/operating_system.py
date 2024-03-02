import subprocess
import pyautogui
import time
import math
from gamer.config import Config

DEBUG = True

# Load configuration
config = Config()


class OperatingSystem:

    def press(self, keys, duration=1.0):
        if DEBUG:
            print("[press]")
            print("[press] keys", keys)

        if not isinstance(keys, list):
            keys = [keys]
        try:
            for key in keys:
                pyautogui.keyDown(key)
            time.sleep(duration)
            for key in keys:
                pyautogui.keyUp(key)
        except Exception as e:
            print("[OperatingSystem][press] error:", e)

    def capture_screen(self, file_path):
        subprocess.run(["screencapture", "-C", file_path])

    def mouse(self, click_detail):
        try:
            x = convert_percent_to_decimal(click_detail.get("x"))
            y = convert_percent_to_decimal(click_detail.get("y"))

            if click_detail and isinstance(x, float) and isinstance(y, float):
                self.click_at_percentage(x, y)

        except Exception as e:
            print("[OperatingSystem][mouse] error:", e)

    def click_at_percentage(
        self,
        x_percentage,
        y_percentage,
        duration=0.2,
        circle_radius=50,
        circle_duration=0.5,
    ):
        try:
            screen_width, screen_height = pyautogui.size()
            x_pixel = int(screen_width * float(x_percentage))
            y_pixel = int(screen_height * float(y_percentage))

            pyautogui.moveTo(x_pixel, y_pixel, duration=duration)

            start_time = time.time()
            while time.time() - start_time < circle_duration:
                angle = ((time.time() - start_time) / circle_duration) * 2 * math.pi
                x = x_pixel + math.cos(angle) * circle_radius
                y = y_pixel + math.sin(angle) * circle_radius
                pyautogui.moveTo(x, y, duration=0.1)

            if config.verbose:
                print("[click_at_percentage] clicking at:", x_pixel, y_pixel)

            pyautogui.click(x_pixel, y_pixel)
            pyautogui.moveTo(screen_width / 2, screen_height / 2, duration=0.1)

        except Exception as e:
            print("[OperatingSystem][click_at_percentage] error:", e)


def convert_percent_to_decimal(percent):
    try:
        # Remove the '%' sign and convert to float
        decimal_value = float(percent)

        # Convert to decimal (e.g., 20% -> 0.20)
        return decimal_value
    except ValueError as e:
        print(f"[convert_percent_to_decimal] error: {e}")
        return None
