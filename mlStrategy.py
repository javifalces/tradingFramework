# strategy.py
from qtpylib.algo import Algo
import pickle
import tpot
from xgboost import XGBClassifier

mlTrainedFile = 'trainedML.pkl'
inputLookBack = 5
import pandas as pd
import numpy as np


def getInputData(bars, inputLookBack):
    output = pd.DataFrame(bars['close'])

    for i in range(inputLookBack):
        if i == 0:
            output['close'] = np.log(bars['close'])
            output['volume'] = bars['volume'].diff()
        else:
            output['diff_%i' % i] = bars['close'] - bars['close'].shift(i)

    return output.fillna(0).as_matrix()


def getTargetData(bars):
    future_return = pd.DataFrame(bars['close'])
    future_return = future_return.diff().shift(-1)
    return (future_return > 0).fillna(0).astype(int).values.ravel()


def trainTpot(symbol):
    import os
    from tpot import TPOTClassifier
    bars = pd.DataFrame.from_csv(settings.csvData + os.sep + symbol + '.BAR.csv')

    inputData = getInputData(bars, inputLookBack)
    target = getTargetData(bars)

    # mlObject = TPOTClassifier(generations=5,population_size=50,verbosity=3,n_jobs=-2)
    mlObject = XGBClassifier()
    mlObject.fit(inputData, target)
    print(mlObject.score(inputData, target))
    # save tpot
    with open(mlTrainedFile, 'wb') as output:
        pickle.dump(mlObject, output, pickle.HIGHEST_PROTOCOL)


class MLAlgo(Algo):
    position = 0
    mlTrainedObject = None

    def on_bar(self, instrument):
        if self.mlTrainedObject is None:
            with open(mlTrainedFile, 'rb') as input:
                self.mlTrainedObject = pickle.load(input)

        # get instrument history
        bars = instrument.get_bars(lookback=inputLookBack)

        # make sure we have at least 20 bars to work with
        if len(bars) < inputLookBack:
            return
        if self.mlTrainedObject is None:
            print("Trained first! tpotObject doesnt exists")
        # get Input data
        input = getInputData(bars, inputLookBack)
        prediction = self.mlTrainedObject.predict(input)
        # get current position data
        positions = instrument.get_positions()

        # trading logic - entry signal
        if prediction[-1] > 0 and self.position == 0:
            if not instrument.pending_orders:
                print("[%s] BUY prediction=%i " % (
                    bars.index[-1], prediction[-1]))
                self.position = 1
                volume = capital / bars.close[-1]
                # send a buy signal
                instrument.buy(int(volume))

        # trading logic - exit signal
        elif prediction[-1] == 0 and self.position != 0:

            print("[%s] Close Buy prediction=%i " % (
                bars.index[-1], prediction[-1]))
            # exit / flatten position
            instrument.exit()
            self.position = 0

        else:
            print("[%s] Nothing/Hold prediction=%i " % (
                bars.index[-1], prediction[-1]))


BACKTEST_ENABLE = True
TRAIN_ML = False
nameOfStrategy = 'mlStrategy'
symbol = 'AAPL'
capital = 100000
import settings
import pickle
import backtest
import os

if __name__ == "__main__":
    if TRAIN_ML or not os.path.exists(mlTrainedFile):
        print('Training ML')
        trainTpot(symbol)

    if not BACKTEST_ENABLE:
        strategy = MLAlgo(
            instruments=[(symbol, "STK", "SMART", "USD", "", 0.0,)],
            resolution="1D"
        )
        strategy.run()
    else:

        strategy = MLAlgo(
            instruments=[(symbol, "STK", "SMART", "USD", "", 0.0,)],
            resolution="1D",
            backtest=True,
            start='2017-01-01',  # YYY-MM-DD [HH:MM:SS[.MS]
            end='2018-02-16',
            output=settings.backtestData + nameOfStrategy + '.csv',
            data=settings.csvData,

        )
        strategy.run()
        backtest.analyze(backtestNameFile=nameOfStrategy + '.csv')
