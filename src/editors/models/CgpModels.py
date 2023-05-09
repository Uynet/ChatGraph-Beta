from abc import ABC, abstractmethod

# Chat Graph Model - View  Objects

@abstractmethod
class CgpModel(ABC):
    def __init__(self, **kwargs):
        pass
    def addToScene(self , scene):
        pass
    def removeFromScene(self , scene):
        pass
    def setView(self, view):
        pass
    def getView(self) :
        pass
    def getController(self):
        pass

@abstractmethod
class CgpView(ABC):
    def __init__(self, model: CgpModel, **kwargs):
        self.model = model
        pass
    def updateView(self):
        pass
    # def onEvent(self, event):
    #     pass
    # def initProperties( self ,props):
    #     pass
    # def getModel(self):
    #     return self.model
    # def getController(self):
    #     pass

@abstractmethod
class CgpWidgetView():
    pass
    # def __init__(**kwargs):
    #     pass
    def updateView(self):
        pass
    # def onEvent(self, event):
    #     pass
    # def initProperties( self ,props):
    #     pass
    # def getModel(self):
    #     return self.model
    # def getController(self):
    #     pass