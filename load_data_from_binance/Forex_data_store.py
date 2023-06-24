import requests


class DataStore:
    store = {}
    proxy = None

    @classmethod
    def loadKlineHistory(self, currency="dotusdt", date=None, api_key=None):
        date = "" if date is None else str(date)
        api_key = "" if api_key is None else str(api_key)
        sig = currency + "@" + 'Daily' + "-" + \
            "|" + date
        url = "https://marketdata.tradermade.com/api/v1/historical?currency={}&date={}&api_key={}"
        if currency:
            url += "&currency={}".format(currency.upper())
        if date:
            url += "&date={}".format(date)
        if api_key:
            url += "&api_key={}".format(api_key)
        print(url)
        r = requests.get(url, proxies=DataStore.proxy)
        data = r.json()
        self.store[sig] = data
        return data
