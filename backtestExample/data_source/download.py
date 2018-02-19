from resolution import Resolution
import datetime


class Download:
    def download(self, symbol, start, end=datetime.datetime.now(), resolution=Resolution.one_day):
        raise Exception('Must implement download function')
