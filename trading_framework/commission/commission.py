class CommissionIfc:

    def getValueCommission(self, dataObject, positionDataframe, overnightPositions=True):
        raise Exception('must implement getValueCommission method on %s' % self.__class__)

    def getTradeCommission(self, openPrice, volume):
        raise Exception('must implement getTradeCommission method on %s' % self.__class__)
