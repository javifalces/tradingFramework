from trading_framework.historical_data.historical_data import HistoricalPriceDataIfc


class YahooHistoricalData(HistoricalPriceDataIfc):

    def download(self, historicalPriceSettings):
        # TODO implement it
        return HistoricalPriceDataIfc.download(self, historicalPriceSettings)
