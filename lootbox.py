import random
from jsondb import JsonDB

lootbox_db = JsonDB("lootbox.json")


def usual_lootbox():
    return random.choice(lootbox_db["usual_items"])


def weapon_lootbox():
    def get_random(d):
        weights_sum = sum([d[key] for key in d.keys()])
        res = random.random()*weights_sum
        lower_bound = 0
        for key in d.keys():
            if lower_bound <= res < lower_bound + d[key]:
                return key
            lower_bound += d[key]

    return get_random(lootbox_db["weapon"]["name"]) + " | " + get_random(lootbox_db["weapon"]["style"])
