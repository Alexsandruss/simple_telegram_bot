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
# default / and ? commands from commands.json
commands = jsondb.load_db("commands.json")["commands"]
# quotes for bot's random quote feature
quotes = jsondb.load_db("quotes.json")["quotes"]


# this function update parser's data
def update_parser(lock, delay):
    global shadow_db
    while True:
        lock.acquire()
        for c_name in parser.currency_links.keys():
            shadow_db[c_name] = parser.rate_usd(c_name)
        lock.release()
        time.sleep(delay)


def message_handler(incoming_message):
    global commands
    global quotes
    global shadow_db
    result = {
        "method": "send_message",
        "chat_id": incoming_message["chat_id"],
        "text": "?"
    }
    for command in commands.keys():
        if incoming_message["text"] == command:
            result["text"] = commands[command]
    # crypto currencies feature
    if incoming_message["text"] in ["/"+key for key in parser.currency_links.keys()]:
        result["text"] = shadow_db[incoming_message["text"][1:]]
    if incoming_message["text"] == "/currencies":
        currencies_list = ""
        for key in parser.currency_links.keys():
            currencies_list += "/" + key + "\n"
        result["text"] = currencies_list
    # random quote feature
    if incoming_message["text"] == "/quote":
        result["text"] = random.choice(quotes)
    # throwing dice feature
    if incoming_message["text"].startswith("/dice"):
        result["text"] = throw_dice(incoming_message["text"])
    # random choice feature
    if incoming_message["text"].startswith("/random"):
        random_result = ""
        try:
            random_result = random.choice(incoming_message["text"].split(" ")[1:])
        except:
            random_result = "Type command correctly"
        finally:
            result["text"] = random_result
    # days until newyear or summer feature
    if incoming_message["text"] == "/newyear":
        result["text"] = digest.days_until_newyear()
    if incoming_message["text"] == "/summer":
        result["text"] = digest.days_until_summer()
    # locations feature
    if incoming_message["text"].startswith("/where"):
        try:
            location = incoming_message["text"].split(" ")[1]
            result["text"] = locations.get_coordinates(location)
        except:
            result["text"] = "Type command correctly"
    if incoming_message["text"].startswith("/location"):
        try:
            location = incoming_message["text"].split(" ")[1:]
            result = {
                "method": "send_location",
                "coordinates": {"latitude": float(location[0]), "longitude": float(location[1])},
                "chat_id": incoming_message["chat_id"]
            }
        except:
            result["text"] = "Type command correctly"
    # chat id getter
    if incoming_message["text"] == "/chat_id":
        result["text"] = incoming_message["chat_id"]
    # unix time feature
    if incoming_message["text"] == "/unix_time":
        result["text"] = "{} seconds since 00:00:00 1 January 1970".format(str(round(time.time())))
    # holiday feature
    if incoming_message["text"] == "/holiday":
        result["text"] = digest.check_holiday()
    if result["text"] == "?":
        result = None
    return result


def bot_processor(lock, delay):
    db = jsondb.load_db("db.json")
    bot = Bot(token=db["token"])
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
                elif outgoing_message["method"] == "send_photo":
                    bot.send_photo(outgoing_message["chat_id"], outgoing_message["photo"])
                elif outgoing_message["method"] == "send_audio":
                    bot.send_audio(outgoing_message["chat_id"], outgoing_message["audio"])
        db["last_checked_update_id"] = bot.last_checked_update_id
        jsondb.save_db("db.json", db)
        lock.release()
        time.sleep(delay)


if __name__ == '__main__':
    lock = multiprocessing.Lock()
    manager = multiprocessing.Manager()
    shadow_db = manager.dict()
    for name in parser.currency_links.keys():
        shadow_db[name] = ""

    parser_updater = multiprocessing.Process(target=update_parser, args=(lock, delays["parser"]))
    bot_process = multiprocessing.Process(target=bot_processor, args=(lock, delays["bot"]))

    parser_updater.start()
    bot_process.start()

    parser_updater.join()
    bot_process.join()
