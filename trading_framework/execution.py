import sys,os

class ExecutionSettings:
    symbols=[]
    period=None
    fundamentals=[]



class ExecutionIfc:

    executionSettings=None
    def __init__(self,executionSettings):
        self.executionSettings = executionSettings


    def onInit(self,data):
        raise Exception('must implement onInit method on %s'%self.__class__)


    def onBar(self,data):
        raise Exception('must implement onInit method on %s' % self.__class__)
