from download import Download
from resolution import Resolution
import datetime
import pandas as pd
import numpy as np


class AlphaVantageDownload(Download):
    alpha_vantage_token = 'token'

    def download(self, symbol, start, end=datetime.datetime.now(), resolution=Resolution.one_day):
        return self.get_alphavantage(symbol, start, end, resolution)

    def get_alphavantage(self, symbol, start, end, resolution=Resolution.one_day):
        from alpha_vantage.timeseries import TimeSeries
        INTERVAL = {}
        INTERVAL[Resolution.one_min] = '1min'
        INTERVAL[Resolution.five_min] = '5min'
        INTERVAL[Resolution.fifteen_min] = '15min'
        INTERVAL[Resolution.thirty_min] = '30min'
        INTERVAL[Resolution.one_hour] = '60min'

        ts = TimeSeries(key=self.alpha_vantage_token, retries=5, output_format='pandas', indexing_type='date')
        if resolution == Resolution.one_day:
            data_d, meta_data_d = ts.get_daily_adjusted(symbol=symbol, outputsize='full')
            data_d.rename(columns={'5. adjusted close': 'close'}, inplace=True)
            data_d.rename(columns={'1. open': 'open'}, inplace=True)
            data_d.rename(columns={'2. high': 'high'}, inplace=True)
            data_d.rename(columns={'3. low': 'low'}, inplace=True)
            data_d.rename(columns={'6. volume': 'volume'}, inplace=True)
            data_d.reset_index(inplace=True)
            data_d.rename(columns={'date': 'index'}, inplace=True)
            data_d.set_index('index', inplace=True)
            data_d.index = pd.to_datetime(data_d.index)


        else:
            # intervals='1min', '5min', '15min', '30min', '60min'
            data_d, meta_data_d = ts.get_intraday(symbol=symbol, interval=INTERVAL[resolution], outputsize='full')
            data_d.rename(columns={'5. volume': 'volume'}, inplace=True)
            data_d.rename(columns={'1. open': 'open'}, inplace=True)
            data_d.rename(columns={'2. high': 'high'}, inplace=True)
            data_d.rename(columns={'3. low': 'low'}, inplace=True)
            data_d.rename(columns={'4. close': 'close'}, inplace=True)
            data_d.reset_index(inplace=True)
            data_d.rename(columns={'date': 'index'}, inplace=True)
            data_d.set_index('index', inplace=True)
            data_d.index = pd.to_datetime(data_d.index)

        output = data_d[['close', 'open', 'high', 'low', 'volume']]
        output['symbol'] = symbol
        if output.index[0] < start:
            output = output[["symbol", "open", "high", "low", "close", "volume"]][start:]
        if output.index[-1] > end:
            output = output[["symbol", "open", "high", "low", "close", "volume"]][:end]

        return output


if __name__ == "__main__":
    out = AlphaVantageDownload().download(symbol='AAPL', start=datetime.datetime(2018, 2, 1),
                                          resolution=Resolution.one_hour)
    out.to_csv('temp_data.csv')
    print (out.head())
