import multiprocessing
import time
import random
from telegram_bot import Bot
from dice import throw_dice
import parser
import digest
import locations
import jsondb


delays = jsondb.load_db("db.json")["delays"]
commands = jsondb.load_db("commands.json")["commands"]
quotes = jsondb.load_db("quotes.json")["quotes"]


# this function update parser's data
def update_parser(shadow_db, lock, delay):
    while True:
        lock.acquire()
        shadow_db["bitcoin"] = parser.crypto_currencies_usd("bitcoin")
        shadow_db["ethereum"] = parser.crypto_currencies_usd("ethereum")
        shadow_db["ripple"] = parser.crypto_currencies_usd("ripple")
        lock.release()
        time.sleep(delay)


def message_handler(incoming_message):
    global commands
    global quotes
    global shadow_db
    result = None
    for command in commands.keys():
        if incoming_message["text"] == command:
            result = {
                "method": "send_message",
                "text": commands[command],
                "chat_id": incoming_message["chat_id"]
            }
    # crypto currencies feature
    if incoming_message["text"] in ["/bitcoin", "/ethereum", "/ripple"]:
        result = {
            "method": "send_message",
            "text": shadow_db[incoming_message["text"][1:]],
            "chat_id": incoming_message["chat_id"]
        }
    # random quote feature
    if incoming_message["text"] == "/quote":
        result = {
            "method": "send_message",
            "text": random.choice(quotes),
            "chat_id": incoming_message["chat_id"]
        }
    # throwing dice feature
    if incoming_message["text"].startswith("/dice"):
        result = {
            "method": "send_message",
            "text": throw_dice(incoming_message["text"]),
            "chat_id": incoming_message["chat_id"]
        }
    # random choice feature
    if incoming_message["text"].startswith("/random"):
        random_result = ""
        try:
            random_result = random.choice(incoming_message["text"].split(" ")[1:])
        except:
            random_result = "Type command correctly"
        finally:
            result = {
                "method": "send_message",
                "text": random_result,
                "chat_id": incoming_message["chat_id"]
            }
    # days until newyear or summer feature
    if incoming_message["text"] == "/newyear":
        result = {
            "method": "send_message",
            "text": digest.days_until_newyear(),
            "chat_id": incoming_message["chat_id"]
        }
    if incoming_message["text"] == "/summer":
        result = {
            "method": "send_message",
            "text": digest.days_until_summer(),
            "chat_id": incoming_message["chat_id"]
        }
    # locations feature
    if incoming_message["text"].startswith("/where"):
        try:
            location = incoming_message["text"].split(" ")[1]
            result = {
                "method": "send_location",
                "coordinates": locations.get_coordinates(location),
                "chat_id": incoming_message["chat_id"]
            }
        except:
            result = {
                "method": "send_message",
                "text": "Type command correctly",
                "chat_id": incoming_message["chat_id"]
            }
    # chat id getter
    if incoming_message["text"] == "/chat_id":
        result = {
            "method": "send_message",
            "text": incoming_message["chat_id"],
            "chat_id": incoming_message["chat_id"]
        }
    return result


# this function collects updates for bot from telegram and response on it
def bot_processor(shadow_db, lock, delay):
    # load dictionaries that stores token, last update's id, command, quotes etc.
    db = jsondb.load_db("db.json")
    bot = Bot(token=db["token"], keep_log=True)
    bot.last_checked_update_id = db["last_checked_update_id"]
    while True:
        lock.acquire()
        messages = bot.get_last_messages()
        for message in messages:
            if round(time.time()) - message["date"] <= db["max_time_diff"]:
                try:
                    incoming_message = {"text": message["text"], "chat_id": message["chat"]["id"]}
                # some messages have not text (stickers, files etc)
                except:
                    continue
                outgoing_message = message_handler(incoming_message)
                if outgoing_message is None:
                    continue
                elif outgoing_message["method"] == "send_message":
                    bot.send_message(outgoing_message["chat_id"], outgoing_message["text"])
                elif outgoing_message["method"] == "send_location":
                    bot.send_location(outgoing_message["chat_id"], outgoing_message["coordinates"])
        db["last_checked_update_id"] = bot.last_checked_update_id
        jsondb.save_db("db.json", db)
        lock.release()
        time.sleep(delay)


if __name__ == '__main__':
    lock = multiprocessing.Lock()
    manager = multiprocessing.Manager()
    shadow_db = manager.dict()
    shadow_db["bitcoin"], shadow_db["ethereum"], shadow_db["ripple"] = "unknown", "unknown", "unknown"

    parser_updater = multiprocessing.Process(target=update_parser, args=(shadow_db, lock, delays["parser"]))
    bot_process = multiprocessing.Process(target=bot_processor, args=(shadow_db, lock, delays["bot"]))

    parser_updater.start()
    bot_process.start()

    parser_updater.join()
    bot_process.join()
