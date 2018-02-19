from backtestExample.broker.broker import Broker


class IbBroker(Broker):
    def sendOrder(self, order):
        # TODO send to broker using api
        pass
