"""
this module simplifies work with .json files
'load_db' returns dictionary after reading .json file
'save_db' gets dictionary and writes it to .json file
"""
import json


def load_db(filename):
    file = open(filename, "r", encoding="utf-8")
    database = json.loads(file.read())
    file.close()
    return database


def save_db(filename, database):
    file = open(filename, "w", encoding="utf-8")
    file.write(json.dumps(database, ensure_ascii=False))
    file.close()
