"""
this module simplifies work with .json files
"""
import json


class JsonDB:
    def __init__(self, file_path: str):
        self.file_path = file_path
        file = open(file_path, "r", encoding="utf-8")
        self.dictionary = json.loads(file.read())
        file.close()

    def write(self):
        file = open(self.file_path, "w", encoding="utf-8")
        file.write(json.dumps(self.dictionary, ensure_ascii=False))
        file.close()
