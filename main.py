import multiprocessing
import time
import random
from telegram_bot import Bot
from dice import throw_dice
import parser
import jsondb

# delays determine how often processes run
delays = jsondb.load_db("db.json")["delays"]


# this function update parser's data
def update_parser(shadow_db, lock, delay):
    while True:
        lock.acquire()
        shadow_db["bitcoin"] = parser.bitcoin()
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
        try:
            messages = bot.get_last_messages()
            for message in messages:
                text = message["text"]
                chat_id = message["chat"]["id"]
                for command in commands.keys():
                    if text == command:
                        bot.send_message(chat_id, commands[command])
                # bitcoin rate feature
                if text == "/bitcoin":
                    bot.send_message(chat_id, shadow_db["bitcoin"])
                # random quote feature
                if text == "/quote":
                    bot.send_message(chat_id, random.choice(quotes))
                # throwing dice feature
                if text.startswith("/dice"):
                    bot.send_message(chat_id, throw_dice(text))
        finally:
            lock.release()
            db["last_checked_update_id"] = bot.last_checked_update_id
            jsondb.save_db("db.json", db)
        time.sleep(delay)


if __name__ == '__main__':
    lock = multiprocessing.Lock()
    manager = multiprocessing.Manager()
    shadow_db = manager.dict()
    shadow_db["bitcoin"] = "unknown"

    parser_updater = multiprocessing.Process(target=update_parser, args=(shadow_db, lock, delays["bitcoin"]))
    bot_process = multiprocessing.Process(target=bot_processor, args=(shadow_db, lock, delays["bot"]))

    parser_updater.start()
    bot_process.start()

    parser_updater.join()
    bot_process.join()
