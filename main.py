import time
from gamer.prompts import get_system_prompt

from gamer.api import get_sm64_operation, get_poker_operation
from gamer.adapter import Adapter

adapters = Adapter()


from gamer.operating_system import OperatingSystem

operating_system = OperatingSystem()

debug = True


def main(game):
    print("[multimodal-gamer]")

    system_prompt = get_system_prompt(game)
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

        if game == "poker":
            operation = get_poker_operation(messages)
        elif game == "sm64":
            operation = get_poker_operation(messages)
        else:
            operation = get_sm64_operation(messages)
        print("[multimodal-gamer] operation", operation)
        operate(operation, game)

        loop_count += 1
        if loop_count > loop_max:
            break


def operate(preprocessed_operation, game):
    if debug:
        print("[multimodal-gamer] operate")

    # print("[multimodal-gamer] action", action)
    # print("[multimodal-gamer] thought", thought)
    # print("[multimodal-gamer] duration", thought)
    if game == "poker":
        operations = adapters.poker(preprocessed_operation)
    else:
        operations = adapters.sm64(preprocessed_operation)
    if debug:
        print("[multimodal-gamer] operations", operations)

    for operation in operations:
        # if debug:
        #     print("[multimodal-gamer] operation", operation)
        operate_type = operation.get("operation")
        if operate_type == "press":
            if debug:
                print("[multimodal-gamer] press operation!")
            key = operation.get("key")
            duration = operation.get("duration", 0.5)
            operating_system.press(key, duration)
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

            operating_system.mouse(click_detail)
        else:
            print("[multimodal-gamer] operation not mapped, no problem!")
            return


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Run the game with specified options.")
    parser.add_argument(
        "-game",
        type=str,
        default="poker",
        help='The name of the game to run. Default is "poker".',
    )
    args = parser.parse_args()

    main(game=args.game)
