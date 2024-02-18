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

    loop_max = 20

    while True:

        if len(messages) > 5:
            print("[multimodal-gamer] truncating earlier message")
            messages = [system_message] + messages[-4:]

        operation = get_operation(messages)
        print("[multimodal-gamer] operation", operation)
        operate(operation)

        loop_count += 1
        if loop_count > loop_max:
            break


def operate(operation):

    actions = operation.get("actions")
    thought = operation.get("thought")
    duration = operation.get("duration")

    # print("[multimodal-gamer] action", action)
    # print("[multimodal-gamer] thought", thought)
    # print("[multimodal-gamer] duration", thought)

    keys = []
    for action in actions:
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

        keys.append(key)

    # print("[multimodal-gamer] key", key)
    # print("-- action complete -- ")

    operating_system.press(keys, duration)


if __name__ == "__main__":
    main()
