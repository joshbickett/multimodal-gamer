class Adapter:
    def __init__(self):
        self.verbose = False

    #         ```
    # [{{ "thought": "write a thought here", "operation": "click", "x": "x percent (e.g. 0.10)", "y": "y percent (e.g. 0.13)" }}]  # "percent" refers to the percentage of the screen's dimensions in decimal format
    # ```

    def sm64(self, operation):
        operations = []
        actions = operation.get("actions")
        duration = operation.get("duration")
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
                key = ""
                raise Exception("The action is not known: ", action)

            operation = {"operation": "press", "key": key, "duration": duration}

            operations.append(operation)

        return operations

    def poker(self, operation):
        x = operation.get("x")
        y = operation.get("y")

        operation = {
            "operation": "click",
            "x": x,
            "y": y,
        }

        return [operation]

    def chess(self, operation):
        # print("[Adapter][chess] operation:", operation)
        action = operation.get("action")
        # action = operation.get("uci")

        operation_highlight_text = {"operation": "press", "keys": ["command", "a"]}
        operation_delete_old_text = {"operation": "press", "keys": ["backspace"]}

        operation = {"operation": "write", "content": action}
        operations = [operation_highlight_text, operation_delete_old_text, operation]
        completion_operation = {"operation": "press", "keys": ["enter"]}
        operations.append(completion_operation)

        # print("[Adapter][chess] operations:", operations)

        return operations
