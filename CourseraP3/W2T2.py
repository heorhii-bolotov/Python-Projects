from bs4 import BeautifulSoup
from decimal import Decimal
from enum import Enum


CBRF_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:68.0) Gecko/20100101 Firefox/68.0'
}


class DB(Enum):
    RUR = ("http://www.cbr.ru/scripts/XML_daily.asp", {})

    def __init__(self, api, params):
        self.api = api
        self.params = params


def convert(amount, cur_from, cur_to, date, requests):
    api, params = DB.RUR.value
    params.setdefault("date_req", date)

    resp = requests.get(api, params, headers=CBRF_HEADERS)
    soup = BeautifulSoup(resp.content, "xml")

    try:
        cur_from = soup.find("CharCode", string=cur_from).parent
        cur_from = int(cur_from.Nominal.string) / Decimal(cur_from.Value.string.replace(",", "."))
    except AttributeError:
        cur_from = 1

    try:
        cur_to = soup.find("CharCode", string=cur_to).parent
        cur_to = int(cur_to.Nominal.string) / Decimal(cur_to.Value.string.replace(",", "."))
    except AttributeError:
        cur_to = 1

    val = (cur_to / cur_from) * amount

    return val.quantize(Decimal(".0001"))
