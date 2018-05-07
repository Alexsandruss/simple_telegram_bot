"""
this module stores functions that collect some data from websites
"""
from bs4 import BeautifulSoup
import requests

CURRENCIES_LIMIT = 16

# requests look "suspicious" for server without this header
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/59.0'
}
currency_links = {}
while "bitcoin" not in currency_links:
    currency_links = {}
    currency_links.update({"gold": "https://ru.investing.com/commodities/gold"})
    currency_links.update({"brent_oil": "https://ru.investing.com/commodities/brent-oil"})
    try:
        soup = BeautifulSoup(requests.get("https://ru.investing.com/crypto/currencies", headers=headers).text, "lxml")
        tds = soup.find_all("td", {"class": "left bold elp name cryptoName first js-currency-name"})
        for td in tds:
            currency_links.update({td.find("a")["href"].split("/")[2].replace("-", "_"): 'https://ru.investing.com' +
                                                                                         td.find("a")["href"]})
            if len(currency_links) > CURRENCIES_LIMIT:
                break
    except:
        continue


def rate_usd(name, output_format="text"):
    try:
        r = requests.get(currency_links[name], headers=headers)
        soup = BeautifulSoup(r.text, "lxml")
        value = soup.find("span", {"id": "last_last"}).text
    except:
        value = -1
    if output_format == "text":
        if value != -1:
            value = "{}: {} $".format(name.capitalize().replace("_", " "), value)
        else:
            value = "{} rate is unavailable".format(name.capitalize().replace("_", " "))
    else:
        if value != -1:
            while "." in value:
                value = value.replace(".", "")
            value = value.replace(",", ".")
            value = float(value)
    return value
