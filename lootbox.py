import random
from jsondb import JsonDB


def usual_lootbox():
    return random.choice(JsonDB("lootbox.json").dictionary["usual_items"])
