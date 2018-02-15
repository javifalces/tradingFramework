import datetime.datetime
from enum import Enum

from trading_framework.statics import DEFAULT_START_DATE_DOWNLOAD

class Period(Enum):
    Day='D',
    Hour='H',
    Minute='M',
    Week='W'

class HistoricalPriceSettings:
    period=None
    symbols=None

    start_date=DEFAULT_START_DATE_DOWNLOAD
    end_date=datetime.datetime.now()

    def __init__(self,period,symbols,start_date,end_date):
        self.period=period
        self.start_date=start_date
        self.end_date=end_date
        self.symbols=symbols

class HistoricalFundamentalSettings:

    symbols=None
    fundamental=None

    start_date=DEFAULT_START_DATE_DOWNLOAD
    end_date=datetime.datetime.now()

    def __init__(self,symbols,fundamental,start_date,end_date):
        self.start_date=start_date
        self.fundamental=fundamental
        self.end_date=end_date
        self.symbols=symbols




class HistoricalFundamentalDataIfc:

    def download(self,historicalFundamentalSettings):
        raise Exception('must implement download method on %s' % self.__class__)



class HistoricalPriceDataIfc:

    def download(self,historicalPriceSettings):
        raise Exception('must implement download method on %s' % self.__class__)