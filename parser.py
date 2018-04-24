"""
this module stores functions that collect some data from websites
"""
from bs4 import BeautifulSoup
import requests


def rate_usd(name):
    # requests look "suspicious" for server without this header
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/52.0'
    }
    currency_links = {
        "bitcoin": "https://ru.investing.com/currencies/btc-usd",
        "ethereum": "https://ru.investing.com/crypto/ethereum",
        "ripple": "https://ru.investing.com/crypto/ripple",
        "litecoin": "https://ru.investing.com/crypto/litecoin",
        "monero": "https://ru.investing.com/crypto/monero",
        "gold": "https://ru.investing.com/commodities/gold",
        "brent_oil": "https://ru.investing.com/commodities/brent-oil"
    }
    try:
        r = requests.get(currency_links[name], headers=headers)
        soup = BeautifulSoup(r.text, "lxml")
        value = soup.find("span", {"id": "last_last"}).text
        result = name.capitalize() + ": " + value + "$"
    except:
        result = name.capitalize() + " rate is unavailable"
    return result
