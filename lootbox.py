import random
from jsondb import JsonDB

lootbox_db = JsonDB("lootbox.json")


def usual_lootbox():
    return random.choice(lootbox_db["usual_items"])


def weapon_lootbox():
    weights_sum = sum([lootbox_db["weapon"]["style"][key] for key in lootbox_db["weapon"]["style"].keys()])
    res = random.random()*weights_sum
    lower_bound = 0
    for key in lootbox_db["weapon"]["style"].keys():
        if lower_bound <= res < lower_bound + lootbox_db["weapon"]["style"][key]:
            res = key
            break
        lower_bound += lootbox_db["weapon"]["style"][key]
    return random.choice(lootbox_db["weapon"]["name"]) + " | " + res
