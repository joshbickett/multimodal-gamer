import time
from gamer.prompts import get_system_prompt

from gamer.api import get_sm64_operation, get_poker_operation, get_chess_operation
from gamer.adapter import Adapter

adapters = Adapter()


from gamer.operating_system import OperatingSystem

operating_system = OperatingSystem()

debug = True


def main(game, model):
    print("[multimodal-gamer]")

    messages = []
    # wait for two seconds

    if debug:
        print("[multimodal-gamer] starting")

    loop_count = 0

    loop_max = 20

    while True:
        time.sleep(2)

        if len(messages) > 5:
            print("[multimodal-gamer] truncating earlier message")
            messages = messages[-4:]

        if game == "chess":
            operation = get_chess_operation(
                model, messages
            )  # at https://www.chess.com/
        elif game == "poker":
            operation = get_poker_operation(
                model, messages
            )  # at https://www.247freepoker.com/
        elif game == "sm64":
            operation = get_sm64_operation(
                model, messages
            )  # at https://www.smbgames.be/super-mario-64.php
        else:
            Exception("game not supported")
        print("[multimodal-gamer] operation", operation)

        if operation.get("action") == "wait" or operation.get("action") == "Wait":
            print("action is wait, break")
            continue

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
    elif game == "chess":

        operations = adapters.chess(preprocessed_operation)
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
            keys = operation.get("keys")
            if not keys:
                keys = operation.get("key")

            duration = operation.get("duration")
            if not duration:
                duration = 1
            operating_system.press(keys, duration)
        elif operate_type == "write":
            if debug:
                print("[multimodal-gamer] write operation!")
            content = operation.get("content")
            operating_system.write(content)
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
        "-m",
        "--model",
        help="Specify the model to use",
        required=False,
        default="gpt-4",
    )
    parser.add_argument(
        "--game",
        type=str,
        default="chess",
        help='The name of the game to run. Default is "poker".',
    )

    try:
        args = parser.parse_args()
        main(game=args.game, model=args.model)
    except KeyboardInterrupt:
        print("Exiting...")
