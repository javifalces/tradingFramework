import pandas as pd
import numpy as np


## get input and target methods
def getInputData(dataframe, lookback_bars=5):
    output = pd.DataFrame(dataframe['close'])
    for i in range(lookback_bars):
        if i == 0:
            output['close'] = np.log(dataframe['close'])
            output['volume'] = dataframe['volume'].diff()
        else:
            output['diff_%i' % i] = dataframe['close'] - dataframe['close'].shift(i)

    return output.fillna(0).as_matrix()


def getTargetData(dataframe):
    future_return = pd.DataFrame(dataframe['close'])
    future_return = future_return.diff().shift(-1)
    return (future_return > 0).fillna(0).astype(int).values.ravel()


def backtest_eventDriven(data, lookback_bars=5):
    import time
    start_time = time.clock()
    # Iterates each day of data
    output = data.copy()
    output['prediction'] = 0
    output['position'] = 0
    last_position = 0
    for index, row in data.iterrows():
        dataToday = pd.DataFrame(data[:index])
        if len(dataToday < lookback_bars):
            continue
        inputData = getInputData(dataToday)
        prediction = mlObject.predict(inputData)
        last_prediction = prediction[-1]
        output['prediction'][index] = last_prediction
        if last_prediction == 1 and last_position == 0:
            print 'BUY at %s' % index
            last_position = 1
            output['position'][index] = 1
        elif last_prediction == 0 and last_position == 1:
            print 'close BUY at %s' % index
            last_position = 0
            output['position'][index] = 0
        else:
            print 'dont do nothing at %s' % index

    end_time = time.clock()
    print('backtest_eventDriven took %i seconds' % (end_time - start_time))
    return output
