import subprocess


def capture_screen_with_cursor(file_path):
    subprocess.run(["screencapture", "-C", file_path])
