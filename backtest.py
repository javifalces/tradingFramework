import settings
import pandas as pd
import matplotlib.pyplot as plt

def analyze(backtestNameFile):
    csvFile = settings.backtestData + backtestNameFile
    data = pd.DataFrame.from_csv(csvFile)
    data['returns'] = data['position'] * data['close'].diff()
    data['pnl'] = data['returns'].cumsum()
    data['returns_benchmark'] = data['close'].diff()
    data['pnl_benchmark'] = data['returns_benchmark'].cumsum()
    data[['pnl', 'pnl_benchmark']].plot()
    plt.savefig(settings.backtestPicsData + backtestNameFile + '.jpg')
    plt.close()
