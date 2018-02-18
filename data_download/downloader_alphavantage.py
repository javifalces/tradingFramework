# load the workflow module
from qtpylib import workflow as wf
import settings
import pandas as pd
import datetime

'''resolution::  1 sec, 5 secs, 15 secs, 30 secs, 1 min (default), 2 mins, 3 mins, 5 mins, 15 mins, 30 mins, 1 hour, 1 day'''


def get_alphavantage_intraday(symbol, start, resolution='1hour'):
    from alpha_vantage.timeseries import TimeSeries
    import settings

    ts = TimeSeries(key=settings.alpha_vantage_token, retries=5, output_format='pandas', indexing_type='date')
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
    output = data_d[['close', 'open', 'high', 'low', 'volume']]

    output['symbol'] = symbol
    return output[["symbol", "open", "high", "low", "close", "volume"]][start:]


def download(symbol, start, resolution="1 hour"):
    # load your existing market data as Pandas DataFrame.
    # here, we'll download 1-min intraday data from Google
    # startStr = datetime.datetime.strftime(start,format='%d/%m/%Y')
    # endStr = datetime.datetime.strftime(end, format='%d/%m/%Y')
    if resolution != '1 day':
        external_data = get_alphavantage_intraday(symbol=symbol, start=start, resolution='1 hour')
    else:
        external_data = wf.get_data_yahoo(symbol, start=start)

    # convert the data into a QTPyLib-compatible
    # data will be saved in ~/Desktop/AAPL.csv

    df = wf.prepare_data(symbol, data=external_data, output_path=settings.csvData)

    # store converted bar data in MySQL
    # optional, requires a running Blotter
    wf.store_data(df, kind="BAR")


if __name__ == "__main__":
    download('AAPL', datetime.datetime(2018, 2, 1))
