from prompts import get_system_prompt
from api import get_operation
import time
from operating_system import OperatingSystem

operating_system = OperatingSystem()

debug = False


def main():
    print("[multimodal-gamer]")

    system_prompt = get_system_prompt()
    system_message = {"role": "system", "content": system_prompt}
    messages = [system_message]
    # wait for two seconds

    time.sleep(2)
    if debug:
        print("[multimodal-gamer] starting")

    loop_count = 0

    loop_max = 3

    while True:

        operations = get_operation(messages)
        print("[multimodal-gamer] operation", operations)
        operate(operations)

        loop_count += 1
        if loop_count > loop_max:
            break


def operate(operations):
    for operation in operations:

        action = operation.get("action").lower()
        thought = operation.get("thought")

        print("[multimodal-gamer] action", action)
        print("[multimodal-gamer] thought", thought)

        if action == "up":
            key = "w"
        elif action == "right":
            key = "d"
        elif action == "down":
            key = "s"
        elif action == "left":
            key = "a"
        elif action == "attack":
            key = "j"
        elif action == "jump":
            key = "k"
        else:
            raise Exception("The action is not known: ", action)

        print("[multimodal-gamer] key", key)
        print("-- action complete -- ")

        operating_system.press(key)


if __name__ == "__main__":
    main()
