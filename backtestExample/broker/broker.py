from enum import Enum


class TypeOrder(Enum):
    MKT = 'market'
    LMT = 'limit'
    STP = 'stop'


class Order:
    symbol = None
    typeOrder = TypeOrder.MKT
    price = None
    volume = None

    def __init__(self, symbol=symbol, typeOrder=typeOrder, price=price, volume=volume):
        if symbol is None:
            raise Exception('symbol must be != None %s' % symbol)
        self.symbol = symbol
        self.typeOrder = typeOrder
        self.price = price
        self.volume = volume


class Broker:

    def sendOrder(self, order):
        raise Exception('must implement sendOrder method on %s' % self.__class__)
