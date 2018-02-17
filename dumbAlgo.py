# strategy.py
from qtpylib.algo import Algo


class DumbAlgo(Algo):

    def on_start(self):
        # optional method that gets called once upon start
        pass

    def on_fill(self, instrument, order):
        # optional method that gets called on every order fill
        pass

    def on_orderbook(self, instrument):
        # optional method that gets called on every orderbook change
        pass

    def on_quote(self, instrument):
        # optional method that gets called on every quote change
        pass

    def on_tick(self, instrument):
        # optional method that gets called on every tick received
        pass

    def on_bar(self, instrument):
        # optional method that gets called on every bar received

        # buy if position = 0, sell if in position > 0
        if instrument.positions['position'] == 0:
            instrument.buy(100)
        else:
            instrument.exit()


if __name__ == "__main__":
    # initialize the algo
    strategy = DumbAlgo(
        instruments=["AAPL"],
        resolution="1T"  # 1Min bar resolution (Pandas "resample" resolutions)
    )

    # run the algo
    strategy.run()
