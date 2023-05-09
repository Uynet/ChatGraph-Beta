from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from editors.models.edgeModel import EdgeModel
    from editors.models.nodes.nodeModel import NodeModel

from editors.views.nodeWindows.socketView import SocketView
from utils.enums import InOutType, PropertyType
from utils.util import Console


class SocketModel():
    def __init__(self, nodeModel, ioType:InOutType, propName:str ) : 
        self.parentNodeModel:NodeModel = nodeModel
        self.edge:EdgeModel= None
        self.name:str = "" 
        self.propName = propName
        # input or output
        self.inOutType :InOutType = ioType 
        self.view = SocketView(self ,nodeModel , ioType)

    def getParent(self) -> NodeModel:
        return self.parentNodeModel

    def connect(self, edge):
        if(self.hasEdge()): 
            Console.error("WARN : duplicate edge!!!!")
            return
        self.view.onConnect()
        self.edge = edge
         
    def isConnected(self , socket):
        if self.edge == None:
            return False
        return self.edge.isConnected(self,socket)

    def getOppositeSocket(self):
        if self.edge == None:
            return None
        return self.edge.getOppositeSocket(self)

    def isConnectableTo(self, socket):
        isDifferentType = self.inOutType != socket.inOutType
        return isDifferentType and not self.hasEdge() and not socket.hasEdge() 

    def disconnect(self):
        self.edge = None
        self.view.onDisConnect()

    def removeChain(self):
        node= self.parentNodeModel
        if self.hasEdge() :
            nodeGraph = node.nodeGraph
            nodeGraph.removeConnection(self.edge)
        node.onRemoveSocket(self)

    def onOutput(self,data:str):
        edge : EdgeModel= self.edge
        if edge:
            edge.onOutput(data)

    def onInput(self,data:str ):
        node = self.parentNodeModel
        node.onInput(data,propName=self.propName , socket=self)
        self.view.onInput(data)

    # 右
    def onFinished(self):
        edge : EdgeModel= self.edge
        if edge:
            edge.onFinished()
    # 左
    def onFinishedOutput(self):
        pass
    
    def removeFromScene(self,scene):
        scene.removeItem(self.view)
    def addToScene(self,scene):
        scene.addItem(self.view)
    def getName(self) :
        return self.name 
    def setName(self,name):
        self.name = name
        self.view.setName(name)
    
    def hasEdge(self):
        return self.edge != None

    def onItemChange(self):
        if self.edge: 
            self.edge.onResize()

    def setEnable(self,isEnable):
        pass

    def getView(self):
        return self.view