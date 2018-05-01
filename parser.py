"""
this module stores functions that collect some data from websites
"""
from bs4 import BeautifulSoup
import requests

currency_links = {
    "bitcoin": "https://ru.investing.com/currencies/btc-usd",
    "ethereum": "https://ru.investing.com/crypto/ethereum",
    "ripple": "https://ru.investing.com/crypto/ripple",
    "litecoin": "https://ru.investing.com/crypto/litecoin",
    "monero": "https://ru.investing.com/crypto/monero",
    "gold": "https://ru.investing.com/commodities/gold",
    "brent_oil": "https://ru.investing.com/commodities/brent-oil",
    "eos": "https://ru.investing.com/crypto/eos",
    "tron": "https://ru.investing.com/crypto/tron",
    "neo": "https://ru.investing.com/crypto/neo",
    "stellar": "https://ru.investing.com/crypto/stellar",
    "cardano": "https://ru.investing.com/crypto/cardano",
    "dash": "https://ru.investing.com/crypto/dash",
    "iota": "https://ru.investing.com/crypto/iota"
}


def rate_usd(name, output_format="text"):
    # requests look "suspicious" for server without this header
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/52.0'
    }
    try:
        r = requests.get(currency_links[name], headers=headers)
        soup = BeautifulSoup(r.text, "lxml")
        value = soup.find("span", {"id": "last_last"}).text
    except:
        value = -1
    if output_format == "text":
        if value != -1:
            value = "{}: {} $".format(name.capitalize(), value)
        else:
            value = "{} rate is unavailable".format(name.capitalize())
    else:
        if value != -1:
            while "." in value:
                value = value.replace(".", "")
            value = value.replace(",", ".")
            value = float(value)
    return value
