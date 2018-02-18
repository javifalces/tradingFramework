# load the workflow module
from qtpylib import workflow as wf
import settings
import datetime

'''resolution::  1 sec, 5 secs, 15 secs, 30 secs, 1 min (default), 2 mins, 3 mins, 5 mins, 15 mins, 30 mins, 1 hour, 1 day'''


def download(symbol, start, resolution="1 hour"):
    # load your existing market data as Pandas DataFrame.
    # here, we'll download 1-min intraday data from Google
    startStr = datetime.datetime.strftime(start, format='%Y-%m-%d %H:%M:%S')  # YYYY-MM-DD [HH:MM:SS[.MS]
    symbolIB = (symbol, "STK", "SMART", "USD", "", 0.0,)
    # instrument, start, resolution = "1 min", blotter = None, output_path = None)
    external_data = wf.get_data_ib(symbolIB, start=startStr, resolution=resolution)

    # convert the data into a QTPyLib-compatible
    # data will be saved in ~/Desktop/AAPL.csv
    df = wf.prepare_data(symbol, data=external_data, output_path=settings.csvData)

    # store converted bar data in MySQL
    # optional, requires a running Blotter
    wf.store_data(df, kind="BAR")


if __name__ == "__main__":
    download('AAPL', datetime.datetime(2018, 2, 10), '1 hour')
