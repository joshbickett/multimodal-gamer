from prompts import get_system_prompt


def main():

    system_prompt = get_system_prompt()
    system_message = {"role": "system", "content": system_prompt}
    messages = [system_message]

    loop_count = 0

    loop_max = 25

    while True:

        try:

            loop_count += 1
            if loop_count > loop_max:
                break
        except Exception as e:
            print("[main.py] e, ", e)


if True:
    print("main.py")
