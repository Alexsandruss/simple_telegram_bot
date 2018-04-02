"""
this module stores functions that collect some data from websites
"""
from bs4 import BeautifulSoup
import requests


def bitcoin():
    # requests looks "suspicious" for server without this header
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/52.0'
    }
    try:
        r = requests.get("https://ru.investing.com/currencies/btc-usd", headers=headers)
        soup = BeautifulSoup(r.text, "lxml")
        value = soup.find("span", {"id": "last_last"}).text
        result = "Bitcoin: " + value + "$"
    except:
        result = "Bitcoin rate is unavailable"
    return result
