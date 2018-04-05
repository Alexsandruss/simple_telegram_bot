"""
this module stores functions that collect some data from websites
"""
from bs4 import BeautifulSoup
import requests


def crypto_currencies_usd(name):
    # requests look "suspicious" for server without this header
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/52.0'
    }
    currency_links = {
        "bitcoin": "https://ru.investing.com/currencies/btc-usd",
        "ethereum": "https://ru.investing.com/crypto/ethereum",
        "ripple": "https://ru.investing.com/crypto/ripple"
    }
    try:
        r = requests.get(currency_links[name], headers=headers)
        soup = BeautifulSoup(r.text, "lxml")
        value = soup.find("span", {"id": "last_last"}).text
        result = name.capitalize() + ": " + value + "$"
    except:
        result = name.capitalize() + " rate is unavailable"
    return result
