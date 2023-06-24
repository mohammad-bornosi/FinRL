import yfinance as yf
import requests_cache


class YahooFinance():
    def __init__(self, api, ticker_list, start, end, interval='1d', proxy=None):
        self.api = api
        self.ticker_list = ticker_list
        self.start = start
        self.end = end
        self.interval = interval
        self.proxy = proxy

    def download(self):
        data = yf.download(tickers=self.ticker_list, start=self.start,
                           end=self.end, interval=self.interval, ignore_tz=True, proxy=self.proxy)

        return data

    def smartScrapping(self):
        session = requests_cache.CachedSession('yfinance.cache')
        session.headers['User-agent'] = 'my-program/1.0'
# The scraped response will be stored in the cache
        ticker = yf.Ticker('EURUSD', session=session)
        return ticker.history(period=' 1mo', start=self.start, end=self.end)
