class TypeOrder(Enum):
    MKT='market'
    LMT='limit'
    STP='stop'


class Order:
    symbol
    typeOrder
    price
    volume

    def __init__(self,symbol,typeOrder,price,volume) :
        self.symbol=symbol
        self.typeOrder=typeOrder
        self.price=price
        self.volume=volume



class BrokerIfc:


    def sendOrder(self,order):
        raise Exception('must implement sendOrder method on %s' % self.__class__)

