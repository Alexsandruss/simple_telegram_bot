"""
this module stores functions that collect some data from websites
"""
from bs4 import BeautifulSoup
import requests

INVCOM_CURRENCIES_LIMIT = 8

# requests look "suspicious" for server without this header
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/59.0'
}
invcom_currency_links = {}
# getting links from investing.com
while "bitcoin" not in invcom_currency_links:
    invcom_currency_links = {}
    invcom_currency_links.update({"gold": "https://ru.investing.com/commodities/gold"})
    invcom_currency_links.update({"brent_oil": "https://ru.investing.com/commodities/brent-oil"})
    try:
        r = requests.get("https://ru.investing.com/crypto/currencies", headers=headers)
        soup = BeautifulSoup(r.text, "lxml")
        tds = soup.find_all("td", {"class": "left bold elp name cryptoName first js-currency-name"})
        for td in tds:
            invcom_currency_links.update(
                {td.find("a")["href"].split("/")[2].replace("-", "_"): 'https://ru.investing.com' +
                                                                       td.find("a")["href"]})
            if len(invcom_currency_links) > INVCOM_CURRENCIES_LIMIT:
                break
    except:
        continue
# getting links from cryptocurrencychart.com
r = requests.get("https://www.cryptocurrencychart.com/", headers=headers)
soup = BeautifulSoup(r.text, "lxml")
trs = soup.find_all("tr", {"class": "row"})
cc_chart_currencies = {}
[cc_chart_currencies.update({tr.find("td", {"class": "name"})["data-value"].lower().replace(" ", "_"):
                                 tr.find("td", {"class": "name"}).find("a")["href"]}) for tr in trs]


def invcom_rate_usd(name, output_format="text"):
    try:
        r = requests.get(invcom_currency_links[name], headers=headers)
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


def cc_chart_price_usd(name, output_format="text"):
    try:
        r = requests.get(cc_chart_currencies[name], headers=headers)
        soup = BeautifulSoup(r.text, "lxml")
        value = soup.find("td", {"class": "right currency"})["data-value"]
    except:
        value = -1
    name = name.capitalize().replace("_", " ")
    if output_format == "text":
        value = "{}: {} $".format(name, value) if value != -1 else "{} rate is unavailable".format(name)
    else:
        if value != -1:
            while "," in value:
                value = value.replace(",", "")
            value = float(value)
    return value
