from download import Download
from resolution import Resolution
import datetime
import pandas as pd
import numpy as np


class QuandlDownload(Download):

    def download(self, symbol, start, end=datetime.datetime.now(), resolution=Resolution.one_day):
        return self.get_ib(symbol, start, end, resolution)

    def get_ib(self, symbol, start, end, resolution=Resolution.one_day):
        # TODO
        pass


if __name__ == "__main__":
    out = QuandlDownload().download(symbol='AAPL', start=datetime.datetime(2018, 2, 1), resolution=Resolution.one_hour)
    out.to_csv('temp_data.csv')
    print (out.head())
