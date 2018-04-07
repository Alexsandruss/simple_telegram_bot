import multiprocessing
import time
import random
from telegram_bot import Bot
from dice import throw_dice
import parser
import digest
import locations
import jsondb

# delays determine how often processes run
delays = jsondb.load_db("db.json")["delays"]


# this function update parser's data
def update_parser(shadow_db, lock, delay):
    while True:
        lock.acquire()
        shadow_db["bitcoin"] = parser.crypto_currencies_usd("bitcoin")
        shadow_db["ethereum"] = parser.crypto_currencies_usd("ethereum")
        shadow_db["ripple"] = parser.crypto_currencies_usd("ripple")
        lock.release()
        time.sleep(delay)


# this function collects updates for bot from telegram and response on it
def bot_processor(shadow_db, lock, delay):
    # load dictionaries that stores token, last update's id, command, quotes etc.
    db = jsondb.load_db("db.json")
    commands = jsondb.load_db("commands.json")["commands"]
    quotes = jsondb.load_db("quotes.json")["quotes"]
    bot = Bot(db["token"])
    bot.last_checked_update_id = db["last_checked_update_id"]
    while True:
        lock.acquire()
        messages = bot.get_last_messages()
        for message in messages:
            try:
                text = message["text"]
                chat_id = message["chat"]["id"]
            # some messages have not text (stickers, files etc)
            except:
                text = ""
                chat_id = -1
            for command in commands.keys():
                if text == command:
                    bot.send_message(chat_id, commands[command])
            # crypto currencies feature
            if text == "/bitcoin" or text == "/ethereum" or text == "/ripple":
                bot.send_message(chat_id, shadow_db[text[1:]])
            # random quote feature
            if text == "/quote":
                bot.send_message(chat_id, random.choice(quotes))
            # throwing dice feature
            if text.startswith("/dice"):
                bot.send_message(chat_id, throw_dice(text))
            # random choice feature
            if text.startswith("/random"):
                try:
                    outgoing_message = random.choice(text.split(" ")[1:])
                except:
                    outgoing_message = "Type command correctly"
                bot.send_message(chat_id, outgoing_message)
            # days until newyear or summer feature
            if text == "/newyear":
                bot.send_message(chat_id, digest.days_until_newyear())
            if text == "/summer":
                bot.send_message(chat_id, digest.days_until_summer())
            # locations feature
            if text.startswith("/where"):
                try:
                    location = text.split(" ")[1]
                    bot.send_location(chat_id, locations.get_coordinates(location))
                except:
                    bot.send_message(chat_id, "Type command correctly")
        lock.release()
        db["last_checked_update_id"] = bot.last_checked_update_id
        jsondb.save_db("db.json", db)
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
