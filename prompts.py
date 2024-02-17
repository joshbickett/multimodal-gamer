SYSTEM_PROMPT = """
You are playing {game}. Your goal is {goal}

You have the following controls: `up`, `right`, `left`, `right`, `attack`, `jump`  

You should think about what you're doing at each step. Provide output in JSON format as follows:

[{{"thought":"...","control":"..."}}]
"""


def get_system_prompt():
    """
    This is a system prompt for the game
    """
    game = "Super Mario 64"
    goal = "to collect Power Stars scattered across various levels in the game, which are accessed through paintings in Princess Peach's castle. The player, as Mario, aims to collect these stars to progress through the castle, unlock new areas, and ultimately defeat Bowser in three different battles to rescue Princess Peach."
    prompt = SYSTEM_PROMPT.format(game=game, goal=goal)
    return prompt
