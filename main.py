import multiprocessing
import time
import random
import images
from telegram_bot import Bot
from dice import throw_dice
import parser
import digest
import locations
from jsondb import JsonDB

# delays determine how often processes run
delays = JsonDB("delays.json").dictionary["delays"]
# default / and ? commands from commands.json
commands = JsonDB("commands.json").dictionary["commands"]
# quotes for bot's random quote feature
quotes = JsonDB("quotes.json").dictionary["quotes"]


# this function update parser's data
def update_parser(delay):
    global shadow_db, lock
    while True:
        lock.acquire()
        for c_name in parser.cc_chart_currencies.keys():
            shadow_db[c_name] = parser.cc_chart_price_usd(c_name)
        lock.release()
        time.sleep(delay)


def message_handler(incoming_message):
    global commands, quotes, shadow_db
    result = {
        "method": "send_message",
        "chat_id": incoming_message["chat_id"],
        "text": "?"
    }
    for command_name in commands.keys():
        if incoming_message["text"] == command_name:
            result["text"] = commands[command_name]
    # crypto currencies feature
    if incoming_message["text"] in ["/"+key for key in parser.cc_chart_currencies.keys()]:
        result["text"] = shadow_db[incoming_message["text"][1:]]
    if incoming_message["text"] == "/currencies":
        currencies_list = ""
        for key in parser.cc_chart_currencies.keys():
            currencies_list += "/" + key + "\n"
        result["text"] = currencies_list
    # old inv com currencies list
    if incoming_message["text"] == "/invcom_currencies":
        currencies_list = ""
        for key in parser.invcom_currency_links.keys():
            currencies_list += "/live_" + key + "\n"
        result["text"] = currencies_list
    if incoming_message["text"].startswith("/live_"):
        result["text"] = parser.invcom_rate_usd(incoming_message["text"][6:])
    # random quote feature
    if incoming_message["text"] == "/quote":
        result["text"] = random.choice(quotes)
    # throwing dice feature
    if incoming_message["text"].startswith("/dice"):
        result["text"] = throw_dice(incoming_message["text"])
    # random choice feature
    if incoming_message["text"].startswith("/random"):
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
            result = {
                "method": "send_location",
                "coordinates": locations.get_coordinates(location),
                "chat_id": incoming_message["chat_id"]
            }
        except:
            result = {
                "method": "send_message",
                "chat_id": incoming_message["chat_id"],
                "text": "Type command correctly"
            }
    if incoming_message["text"].startswith("/location") and incoming_message["text"] != "/locations":
        try:
            location = incoming_message["text"].split(" ")[1:]
            result = {
                "method": "send_location",
                "coordinates": {"latitude": float(location[0]), "longitude": float(location[1])},
                "chat_id": incoming_message["chat_id"]
            }
        except:
            result = {
                "method": "send_message",
                "chat_id": incoming_message["chat_id"],
                "text": "Type command correctly"
            }
    # chat id getter
    if incoming_message["text"] == "/chat_id":
        result["text"] = incoming_message["chat_id"]
    # unix time feature
    if incoming_message["text"] == "/unix_time":
        result["text"] = "{} seconds since 00:00:00 1 January 1970".format(str(round(time.time())))
    # holiday feature
    if incoming_message["text"] == "/holiday":
        result["text"] = digest.check_holiday()
    # rgb feature
    if incoming_message["text"].startswith("/rgb"):
        try:
            rgb = [int(color) for color in incoming_message["text"].split(" ")[1:]]
            rgb = tuple(rgb)
            if len(rgb) != 3:
                raise ValueError
        except:
            rgb = (255, 255, 255)
        finally:
            result = {
                "method": "send_photo",
                "photo": open(images.show_color_rgb(rgb), "rb"),
                "caption": "Red - {}, Green - {}, Blue - {}".format(rgb[0], rgb[1], rgb[2]),
                "chat_id": incoming_message["chat_id"]
            }
    # drop log file feature
    if incoming_message["text"] == "/droplog":
        result = {
            "method": "send_document",
            "caption": "Log",
            "chat_id": incoming_message["chat_id"]
        }
    if "text" in result.keys():
        if result["text"] == "?":
            result = None
    return result


def bot_processor(delay):
    global lock
    db = JsonDB("db.json")
    bot = Bot(db.dictionary["token"])
    while True:
        lock.acquire()
        messages = bot.get_last_messages()
        for message in messages:
            if round(time.time()) - message["date"] <= db.dictionary["max_time_diff"]:
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
                    bot.send_photo(outgoing_message["chat_id"], outgoing_message["photo"], outgoing_message["caption"])
                elif outgoing_message["method"] == "send_audio":
                    bot.send_audio(outgoing_message["chat_id"], outgoing_message["audio"])
                elif outgoing_message["method"] == "send_document":
                    if outgoing_message["caption"].startswith("Log"):
                        if outgoing_message["chat_id"] == bot.admin_id:
                            bot.send_document(bot.admin_id, open(bot.log_file, "rb"), outgoing_message["caption"])
                        else:
                            bot.send_message(bot.admin_id, "Unresolved attempt to access to log file from {}".format(
                                outgoing_message["chat_id"]))
                    else:
                        pass
        db.dictionary["last_checked_update_id"] = bot.last_checked_update_id
        db.write()
        lock.release()
        time.sleep(delay)


if __name__ == '__main__':
    lock = multiprocessing.Lock()
    manager = multiprocessing.Manager()
    shadow_db = manager.dict()
    for name in parser.cc_chart_currencies.keys():
        shadow_db[name] = ""

    parser_updater = multiprocessing.Process(target=update_parser, args=(delays["parser"],))
    bot_process = multiprocessing.Process(target=bot_processor, args=(delays["bot"],))

    parser_updater.start()
    bot_process.start()

    parser_updater.join()
    bot_process.join()
