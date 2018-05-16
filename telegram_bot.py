import requests
import time


class Bot:
    def __init__(self, token, keep_log: bool=False, log_file: str="log.txt", admin_id=None,
                 disable_notification: bool = False):
        self.token = token
        self.admin_id = admin_id
        self.keep_log = keep_log
        self.log_file = log_file
        self.disable_notification = disable_notification
        self.name = self.get_me()["first_name"]
        self.last_checked_update_id = 0
        if self.keep_log:
            log = open(self.log_file, "w")
            log.write("BOT LOG")
            log.close()

    def telegram_request(self, method, parameters=None, files=None):
        try:
            response = requests.post("https://api.telegram.org/bot" + self.token + "/" + method,
                                     params=parameters, files=files).json()
        except:
            response = {"ok": False}
        self.log_update(str(response))
        if response["ok"]:
            return response["result"]
        else:
            return {}

    def log_update(self, note):
        if self.keep_log and note not in ["{}", "[]", ""]:
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

    def send_message(self, chat_id, text):
        params = {
            'chat_id': chat_id,
            'text': text,
            "disable_notification": self.disable_notification
        }
        return self.telegram_request("sendmessage", params)

    def send_location(self, chat_id, coordinates: dict):
        params = {
            'chat_id': chat_id,
            'latitude': coordinates["latitude"],
            'longitude': coordinates["longitude"],
            "disable_notification": self.disable_notification
        }
        return self.telegram_request("sendlocation", params)

    def send_photo(self, chat_id, photo, caption=None):
        params = {
            'chat_id': chat_id,
            'caption': caption,
            "disable_notification": self.disable_notification
        }
        files = {"photo": photo}
        return self.telegram_request("sendphoto", params, files)

    def send_audio(self, chat_id, audio, caption=None):
        params = {
            'chat_id': chat_id,
            'caption': caption,
            "disable_notification": self.disable_notification
        }
        files = {"audio": audio}
        return self.telegram_request("sendaudio", params, files)

    def get_last_messages(self):
        updates = self.get_updates(self.last_checked_update_id + 1, allowed_updates=["message"])
        messages = []
        for update in updates:
            if "message" in update.keys():
                messages.append(update["message"])
        return messages
