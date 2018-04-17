import requests
import time


class Bot:
    def __init__(self, token, keep_log: bool = False, log_file: str = "log.txt"):
        self.token = token
        self.keep_log = keep_log
        self.log_file = log_file
        self.name = self.get_me()["first_name"]
        self.last_checked_update_id = 0
        if self.keep_log:
            log = open(self.log_file, "w")
            log.write("BOT LOG")
            log.close()

    def telegram_request(self, method, parameters=None):
        response = requests.post("https://api.telegram.org/bot" + self.token + "/" + method, params=parameters).json()
        self.log_update(str(response))
        if response["ok"]:
            return response["result"]
        else:
            return {}

    def log_update(self, note):
        if self.keep_log:
            log = open(self.log_file, "a")
            log.write("\n" + str(time.time()) + ":" + note)
            log.close()

    def get_me(self):
        return self.telegram_request("getme")

    def get_updates(self, offset=None, limit=100, timeout=0, allowed_updates=None):
        params = {
            "offset": offset,
            "limit": limit,
            "timeout": timeout,
            "allowed_updates": allowed_updates
        }
        updates = self.telegram_request("getupdates", params)
        if len(updates) != 0:
            self.last_checked_update_id = updates[len(updates) - 1]["update_id"]
        return updates

    def send_message(self, chat_id, text, disable_notification=False):
        params = {
            'chat_id': chat_id,
            'text': text,
            "disable_notification": disable_notification
        }
        return self.telegram_request("sendmessage", params)

    def send_location(self, chat_id, coordinates: dict, disable_notification=False):
        params = {
            'chat_id': chat_id,
            'latitude': coordinates["latitude"],
            'longitude': coordinates["longitude"],
            "disable_notification": disable_notification
        }
        return self.telegram_request("sendlocation", params)

    def get_last_messages(self):
        updates = self.get_updates(self.last_checked_update_id + 1, allowed_updates=["message"])
        return [update["message"] for update in updates]
