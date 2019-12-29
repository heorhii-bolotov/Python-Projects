"""
    В этом задании вы научитесь работать с библиотекой requests (http://docs.python-requests.org/en/master/),
    а также научитесь работать с API сервиса VK и его документаций,
    что является достаточно частой задачей разработчика.
"""


from collections import defaultdict
from datetime import datetime
import requests

http_proxy = "http://79.104.28.46:35405"
https_proxy = "https://188.0.138.147:8080"

proxy_dict = {
    "http": http_proxy,
    "https": https_proxy,
}


def get_html(url, params=None, proxies=None, verify=True):
    resp = requests.get(url, params=params or {}, proxies=proxies or {}, verify=verify)
    return resp.json()


class Proxy:
    PROXY_URL = "https://free-proxy-list.net/anonymous-proxy.html"
    TABLE = dict(IP=0, PORT=1, CODE=2, HTTPS=6)

    def __init__(self, proxies=None, proxy_flag=False):
        self.proxies = proxies or []
        if proxy_flag:
            if not len(self.proxies):
                self.add_proxy()

            self.proxy = self.proxies[-1]

        else:
            self.proxy = {}

    def add_proxy(self):
        try:
            from bs4 import BeautifulSoup
        except ImportError:
            return

        soup = BeautifulSoup(requests.get(self.PROXY_URL).text, "lxml")
        table = soup.find("table", id="proxylisttable")

        for tr in table.find_all("tr")[1:-1]:
            tds = tr.find_all("td")

            ip = tds[self.TABLE["IP"]].text.strip()
            port = tds[self.TABLE["PORT"]].text.strip()
            protocol = tds[self.TABLE["HTTPS"]].text.strip()
            if protocol == "yes":
                protocol = "https"
            else:
                continue
            self.proxies.append({protocol: protocol + "://" + ip + ":" + port})

            return


class VkData(Proxy):
    VK_URL = "https://api.vk.com/"
    APIVersion = 5.71

    def __init__(self, access_token=None, proxies=None, proxy_flag=False):
        self.access_token = access_token or "17da724517da724517da72458517b8abce117da17da72454d235c274f1a2be5f45ee711"
        super().__init__(proxies, proxy_flag)

    def get_id(self, user_id, verify=True):
        url = self.VK_URL + "method/users.get"
        params = {
            "access_token": self.access_token,
            "user_ids": user_id,
            "v": self.APIVersion
        }
        data = get_html(url, params=params, proxies=self.proxy, verify=verify)
        return data["response"][0]["id"]

    def get_friends(self, id, verify=True):
        url = self.VK_URL + "method/friends.get"
        params = {
            "access_token": self.access_token,
            "user_id": id,
            "fields": "bdate",
            "v": self.APIVersion
        }
        data = get_html(url, params=params, proxies=self.proxy, verify=verify)
        count, items = data["response"].values()
        return count, items


def get_ages(items):
    friends = defaultdict(int)
    cur_year = datetime.now().year
    for item in items:
        bdate = item.get("bdate", None)
        if bdate:
            try:
                day, month, year = bdate.split(".")
                age = cur_year - int(year)
                friends[age] += 1

            except ValueError:
                continue

    return sorted(friends.items(), key=lambda x: (-x[0], x[1]), reverse=True)


def calc_age(user_id):
    db = VkData(proxies=[proxy_dict, ])
    id = db.get_id(user_id)
    total, items = db.get_friends(id)
    return get_ages(items)


if __name__ == '__main__':
    print(calc_age('reigning'))