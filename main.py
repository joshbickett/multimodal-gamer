from prompts import get_system_prompt
from api import get_operation
import time


def main():
    print("[main]")

    system_prompt = get_system_prompt()
    system_message = {"role": "system", "content": system_prompt}
    messages = [system_message]
    # wait for two seconds

    time.sleep(2)

    # loop_count = 0

    # loop_max = 25

    # while True:

    operation = get_operation(messages)
    print("[main] operation", operation)

    # loop_count += 1
    # if loop_count > loop_max:
    #     break


if __name__ == "__main__":
    main()
