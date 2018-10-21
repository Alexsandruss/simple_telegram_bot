"""
this module stores functions that collect some data from websites
"""
from bs4 import BeautifulSoup
import requests


# requests look "suspicious" for server without this header
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/59.0'
}

# getting links from cryptocurrencychart.com
r = requests.get("https://www.cryptocurrencychart.com/", headers=headers)
soup = BeautifulSoup(r.text, "lxml")
trs = soup.find_all("tr", {"class": "row"})
cc_chart_currencies = {}
[cc_chart_currencies.update({tr.find("td", {"class": "name"})["data-value"].lower().replace(" ", "_"):
                             tr.find("td", {"class": "name"}).find("a")["href"]}) for tr in trs]


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
