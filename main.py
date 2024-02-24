import time
from gamer.prompts import get_system_prompt

from gamer.api import get_sm64_operation
from gamer.adapter import Adapter

adapters = Adapter()


from gamer.operating_system import OperatingSystem

operating_system = OperatingSystem()

debug = True


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

        operation = get_sm64_operation(messages)
        print("[multimodal-gamer] operation", operation)
        operate(operation)

        loop_count += 1
        if loop_count > loop_max:
            break


def operate(operation):
    if debug:
        print("[multimodal-gamer] operate")

    actions = operation.get("actions")
    thought = operation.get("thought")
    duration = operation.get("duration")

    # print("[multimodal-gamer] action", action)
    # print("[multimodal-gamer] thought", thought)
    # print("[multimodal-gamer] duration", thought)

    operations = adapters.sm64(actions)

    for operation in operations:
        if debug:
            print("[multimodal-gamer] operation", operation)
        operate_type = operation.get("operation")
        if operate_type == "press":
            if debug:
                print("[multimodal-gamer] press operation!")
            key = operation.get("key")
            operating_system.press(key)
        elif operate_type == "write":
            if debug:
                print("[multimodal-gamer] write operation!")
            content = operation.get("content")
            operate_detail = content
            # operating_system.write(content)
        elif operate_type == "click":
            if debug:
                print("[multimodal-gamer] click operation!")
            x = operation.get("x")
            y = operation.get("y")
            click_detail = {"x": x, "y": y}
            operate_detail = click_detail

            operating_system.mouse(click_detail)


if __name__ == "__main__":
    main()
