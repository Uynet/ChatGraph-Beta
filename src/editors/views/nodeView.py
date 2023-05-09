from editors.models.CgpModels import CgpView
from editors.types.dataType import NodeViewData, SlotData
from editors.views.nodeWindows.nodeWindow import NodeWindow
from utils.enums import InOutType, PropertyType
from utils.util import Console


# Abstract Class
class NodeView(CgpView):
    def __init__(self,nodeModel,Window = NodeWindow):
        self.propertyFields = [] 
        self.nodeWindow = Window(self , nodeModel) 
        self.nodeModel = None
        self.setNodeModel(nodeModel)

    def initProperties(self,nodeData:NodeViewData):
        self.nodeWindow.initProperties(nodeData)


    def onSetState(self,state):
        self.nodeWindow.onSetState(state)

    # must be singleton!
    def setNodeModel(self, nodeModel):
        if self.nodeModel is not None:
           Console.warn("ERR : " + self.nodeModel.labelText + " is already setted") 
        self.nodeModel = nodeModel

    def addSlot(self, label , typeSet = None):
        self.nodeWindow.addSlot(label , typeSet) 

    def onFinished(self , data, propName):
        self.nodeWindow.onFinished(data,propName)

    def onInput(self,**kwargs):
        self.nodeWindow.onInput(**kwargs)

    def updateView(self):
        self.nodeWindow.updateView()