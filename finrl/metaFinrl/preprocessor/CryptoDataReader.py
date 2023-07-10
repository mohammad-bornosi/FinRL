## 3.3 : use finnhub to get crypto market data  
import finnhub
import pandas as pd
import datetime
import calendar
import pandas as pd
import numpy as np
import time
class CryptoDataLoader:

    def __init__(
    self,
    symbols_list,
    api_key  = 'cbj22uqad3i2thcmtg80'
    ):
        self.symbol_list = symbols_list
        self.finnhub_client = finnhub.Client(api_key=api_key)
        self.crypto_symbol = [] 
    
### load choosed_symbols
    def load_choosed_symbols (self, exchange = 'BINANCE'):
        crypto_symbol = []
        binance_crypto_symbols = self.finnhub_client.crypto_symbols(exchange)
        for symbol in binance_crypto_symbols:
            crypto_0 = symbol['displaySymbol'].split('/')[0]
            crypto_1 = symbol['displaySymbol'].split('/')[1]
            check  = all(item in self.symbol_list for item in [crypto_0,crypto_1])
            if check :
                crypto_symbol.append(symbol)
        return crypto_symbol

    def add_tic_column_to_data(self, symbol_name, stock_df):
        shape = stock_df.shape
        data_list = [symbol_name] * shape[0]
        stock_df['symbol'] = data_list
        return stock_df


    def load_symbol_candles(self, symbol,start,end):
        candles_data = self.finnhub_client.crypto_candles(symbol, resolution='D', 
        _from = calendar.timegm(start),
        to = calendar.timegm(end) 
        )
        return candles_data

    def load_crypto_candles(self, start = datetime.date(2019,1,1).timetuple(),end = datetime.date(2022,8,14).timetuple()):
        self.crypto_symbol = self.load_choosed_symbols()
        crypto_symbols_df = pd.DataFrame()
        for symbol in self.crypto_symbol:
            new_candles = self.load_symbol_candles(symbol['symbol'], start, end)
            if (new_candles['s'] != 'no_data'):
                new_crypto_candles = self.add_tic_column_to_data(symbol['symbol'], pd.DataFrame(new_candles))
                crypto_symbols_df = pd.concat([crypto_symbols_df, new_crypto_candles])
        return crypto_symbols_df

    def cleansing_holcv_dataframes(self, symbols_df):
        symbols_df.rename(columns={'c':'close','h':'high','l':'low','o':'open','t':'date','v':'volume','symbol':'tic'},inplace=True)
        symbols_df.drop(columns={'s'}, inplace=True)
        return symbols_df

    def crypto_clean_data(self,data) :
        df = data.copy()
        df = df.sort_values(["date", "tic"], ignore_index=True)
        df.index = df.date.factorize()[0]
        merged_closes = df.pivot_table(index="date", columns="tic", values="close")
        print(max(merged_closes.isna().sum()))
        bool = merged_closes.isna().sum() != 302
        all_tics = bool.index
        merged_closes = merged_closes.drop(columns = all_tics[np.where(bool == True)])
        merged_closes = merged_closes.dropna(axis=0)
        dates = merged_closes.index
        df = df[df.date.isin(dates)]
        return df