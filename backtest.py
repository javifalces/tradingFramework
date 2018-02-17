import settings
import pandas as pd


def analyze(backtestNameFile):
    csvFile = settings.backtestData + backtestNameFile
    data = pd.from_csv(csvFile)
    data['pnl'] = data['position'] * data['close'].diff()
    data['pnl'].plot()
