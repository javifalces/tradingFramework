# strategy.py
from qtpylib.algo import Algo

minBars = 20


class CrossOver(Algo):

    def on_bar(self, instrument):

        # get instrument history
        bars = instrument.get_bars(lookback=minBars)

        # make sure we have at least 20 bars to work with
        if len(bars) < minBars:
            return

        # compute averages using internal rolling_mean
        bars['short_ma'] = bars['close'].rolling_mean(window=5)
        bars['long_ma'] = bars['close'].rolling_mean(window=minBars)

        # get current position data
        positions = instrument.get_positions()

        # trading logic - entry signal
        if bars['short_ma'].crossed_above(bars['long_ma'])[-1]:
            if not instrument.pending_orders and positions["position"] == 0:
                print("[%s] BUY shortMA=%.3f  longMA=%.3f " % (
                    bars.index[-1], bars['short_ma'][-1], bars['long_ma'][-1]))

                # send a buy signal
                instrument.buy(1)

                # record values for future analysis
                self.record(ma_cross=1)

        # trading logic - exit signal
        elif bars['short_ma'].crossed_below(bars['long_ma'])[-1]:
            if positions["position"] != 0:
                print("[%s] Close Buy shortMA=%.3f  longMA=%.3f " % (
                    bars.index[-1], bars['short_ma'][-1], bars['long_ma'][-1]))
                # exit / flatten position
                instrument.exit()

                # record values for future analysis
                self.record(ma_cross=-1)
        else:
            print(
                "[%s] Nothing shortMA=%.3f  longMA=%.3f " % (bars.index[-1], bars['short_ma'][-1], bars['long_ma'][-1]))


BACKTEST_ENABLE = True
nameOfStrategy = 'crossOver'
import settings
import pickle
import backtest

if __name__ == "__main__":
    if not BACKTEST_ENABLE:
        strategy = CrossOver(
            instruments=[("AAPL", "STK", "SMART", "USD", "", 0.0,)],
            resolution="1D"
        )
        strategy.run()
    else:

        strategy = CrossOver(
            instruments=[("AAPL", "STK", "SMART", "USD", "", 0.0,)],
            resolution="1D",
            backtest=True,
            start='2017-01-01',  # YYY-MM-DD [HH:MM:SS[.MS]
            end='2018-02-16',
            output=settings.backtestData + nameOfStrategy + '.csv',
            data=settings.csvData,

        )
        strategy.run()
        backtest.analyze(backtestNameFile=nameOfStrategy + '.csv')
