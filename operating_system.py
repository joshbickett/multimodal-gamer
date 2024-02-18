import subprocess
import pyautogui
import time

DEBUG = True


class OperatingSystem:

    def press(self, keys, duration="1"):
        if DEBUG:
            print("[press]")
            print("[press] keys", keys)

        # cast ``

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
