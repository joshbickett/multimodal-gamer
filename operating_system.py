import subprocess
import pyautogui
import time


class OperatingSystem:

    def press(self, keys):
        try:
            for key in keys:
                pyautogui.keyDown(key)
            time.sleep(0.1)
            for key in keys:
                pyautogui.keyUp(key)
        except Exception as e:
            print("[OperatingSystem][press] error:", e)

    def capture_screen(self, file_path):
        subprocess.run(["screencapture", "-C", file_path])
