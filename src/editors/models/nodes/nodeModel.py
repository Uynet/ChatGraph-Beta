from __future__ import annotations
from typing import TYPE_CHECKING

from editors.types.dataType import SlotData
if TYPE_CHECKING:
    from editors.views.nodeScene import NodeScene

from editors.controllers.mainWindowController import MainWindowController
from editors.models.CgpModels import CgpModel
from editors.models.edgeModel import EdgeModel
from editors.models.socketModel import SocketModel
from editors.views.nodeView import NodeView
from utils.enums import InOutType, NodeProcessState, PropertyType
from utils.sound import CSound
from utils.util import Console, Util


class Sockets(CgpModel):
    inputs : list[SocketModel] = []
    outputs : list[SocketModel] = []

class NodeModel(CgpModel):
    state = NodeProcessState.WAITING
    
    def __init__(self,nodeType ):
        self.id = None 
        self.nodeGraph = None
        self.nodeData =  None
        self.slots = []
        self.currentThread = None
        self.nodeView:NodeView = None 
        self.nodeType = nodeType
        self.sockets = Sockets() 
        self.sockets.inputs:list[SocketModel] = []
        self.sockets.outputs:list[SocketModel] = []
        self.setState(NodeProcessState.WAITING , False)

    def addSlots(self,slotDatas:list[SlotData]):
        for slot in slotDatas:
            propName = slot.get("propName")
            propertyTypeStr = slot.get("type")
            propertyType = PropertyType.fromStr(propertyTypeStr)
            ioTypeStr = slot.get("ioType")
            ioType = InOutType.fromStr(ioTypeStr) 
            self.addSlot(propName, propertyType, ioType )

    def addSlot(self , propName , propertyType=PropertyType.SET , ioType = InOutType.IN): 
        self.nodeView.addSlot(propName , {propertyType , ioType})
        slot = SlotData(propName=propName , type=propertyType.value,ioType=ioType.value)
        self.slots.append(slot)

    def addSocket(self, inOutType:InOutType, propName:str , name = "") -> SocketModel:
        inOutTypeString = inOutType.value
        socket:SocketModel = SocketModel(self, inOutType,propName)
        socket.setName(name)
        if inOutType == InOutType.IN:
            self.sockets.inputs.append(socket)
        elif inOutType== InOutType.OUT:
            self.sockets.outputs.append(socket)
        else:
            raise ValueError("Invalid socket type: {}".format(inOutTypeString))
        self.nodeView.updateView() 
        return socket

    def getSocketId(self,socket:SocketModel):
        if socket.inOutType == InOutType.IN:
            return self.sockets.inputs.index(socket)
        elif socket.inOutType == InOutType.OUT:
            return self.sockets.outputs.index(socket)
        else:
            Console.error("🔥ERROR : Invalid socket type: {}".format(socket.inOutType))
            return None

    ########################################################
    # MODELS
    ########################################################

    def onFinished(self, data:str , propName = "output" , outSockets=None): 
        isSendChat = self.getProperty("isSendChat")
        if isSendChat: self.sendToChatWindow()

        self.setState(NodeProcessState.FINISHED)
        self.nodeView.onFinished(data , propName)
        # 指定のない場合すべてから出力
        if outSockets is None:
            outSockets = self.sockets.outputs

        self.emitSockets(outSockets, data)

    # data : string
    def emitSockets(self,sockets:list[SocketModel] , data: str):
        CSound.play("emit.wav")
        for outputSocket in sockets:
            outputSocket.onOutput(data)

    def isRunning(self):
        return self.state == NodeProcessState.RUNNING
    
    def getId(self):
        if self.id != None:
            return self.id
        # ランダムなidを生成
        Console.warn("🔥WARN : Node id is duplicated!!")    
        self.id = Util.genRandomhash()
         
        return self.id

    def resetId(self):
        if self.id is None:
            Console.warn("🔥WARN : Reset ID!!")    
            return self.id
        # ランダムなidを生成
        self.id = Util.genRandomhash()
         
        return self.id

    def setId(self,id):
        self.id = id

    ########################################################
    def initProperties(self, nodeData):
        self.nodeData = nodeData

    # isUpdateView : Viewに即時反映させるかどうか
    def onChangeProperty(self , name , value , isUpdateView, isUpdateInspector = False):
        self.setProperty(name, value , isUpdateView , isUpdateInspector)

    # from nodeModel itself
    def setProperty(self, name, value , isUpdateView = True , isUpdateInspector = False):
        if self.nodeData is None:return
        self.nodeData.set(name, value)
        if isUpdateView : self.nodeView.updateView()
        if isUpdateInspector : MainWindowController.getInstance().onChangeNodeProperty(self ,name ,value)
        
    def getProperty(self, property_name):
        if self.nodeData is None:
            Console.error("NodeData None!")

        return self.nodeData.get(property_name)

    def getProperties(self):
        from editors.models.serializer import Serializer
        props = Serializer.nodeToJson(self)
        return props

    def setState(self, state , isUpdateView = True):
        self.state = state
        if isUpdateView :
            self.nodeView.onSetState(state)

    ########################################################
    

    def getAllSockets(self):
        return self.sockets.inputs + self.sockets.outputs

    def getSocket(self, inOutType: str, index: int):
        if inOutType not in ["input", "output"]:
            Console.error("Invalid socket type: {}".format(inOutType))
            raise ValueError("Invalid socket type: {}".format(inOutType))

        sockets = self.sockets.inputs if inOutType == "input" else self.sockets.outputs
        if index is None:
            Console.error("Invalid socket index: {}".format(index))

        if index < 0 or index >= len(sockets):
            Console.error("🔥ERR : INVALID SOCKET INDEX")
            raise ValueError("Invalid socket index: {}".format(index))

        return sockets[index]    

    def addSockets(self,socketDatas):
        for socketData in socketDatas:
            # get value from dict
            inOutTypeString = socketData["type"]
            propName = socketData["propName"]
            inOutType =InOutType(inOutTypeString)
            socket = self.addSocket(inOutType , propName)
            # set name
            if "name" in socketData:
                socket.setName(socketData["name"])

    ########################################
    #EVNET
    ########################################
    def onRemoveSocket(self , socket):
        # socketが削除されたときに呼ばれる
        if(socket.inOutType == InOutType.IN):
            self.sockets.inputs.remove(socket)
        elif(socket.inOutType == InOutType.OUT):
            self.sockets.outputs.remove(socket)
        else:
            raise ValueError("Invalid socket type: {}".format(type))

    def setThread(self, thread):
        self.currentThread = thread
        MainWindowController.getInstance().addThread(thread)

    def sendToChatWindow(self ):
        name = self.getProperty("label")
        if name == None:
            name = "" 
        chatScreenName = name
        answer = self.getProperty("output")
        MainWindowController.getInstance().sendToChat(chatScreenName, answer , self.getProperty("icon"))

    def onError(self,state,answer):
        MainWindowController.getInstance().onError( state , answer )

    def onStop(self):
        self.setState(NodeProcessState.STOPPED)
        if self.currentThread is not None:
            self.currentThread.stop()
            self.currentThread.finished.connect(self.currentThread.deleteLater)  # スレッドが終了したときにオブジェクトを削除するように指示
            self.currentThread = None

    # socketがNoneとは ... チャット欄からの入力など
    def onInput(self,data:str="",propName:str="",socket:SocketModel=None):
        self.setState(NodeProcessState.RUNNING)
        self.nodeView.onInput(data=data,propName=propName)

    # edgeのうちnodesに含まれるノードと接続されているedgeを返す
    def getEdgesIn(self,nodes):
        edges:list[EdgeModel] = []
        allSockets = self.getAllSockets()
        connectedSockets = [socket for socket in allSockets if socket.hasEdge()]
        for socket in connectedSockets: 
            socket:SocketModel
            edge:EdgeModel = socket.edge
            if edge.getOppositeSocket(socket).parentNodeModel in nodes:
                edges.append(edge)
        return edges

    def getEdges(self):
        edges = []
        allSockets = self.getAllSockets()
        connectedSockets = [socket for socket in allSockets if socket.hasEdge()]
        for socket in connectedSockets: 
            socket:SocketModel
            edge = socket.edge
            edges.append(edge) 
        return edges

    ## CONTROLLER ## 
    def addToScene(self,scene:NodeScene):
        scene.addItem(self.nodeView.nodeWindow)

    def removeFromScene(self,scene:NodeScene):
        scene.removeItem(self.nodeView.nodeWindow)

    def addToGraph(self,nodeGraph):
        self.nodeGraph = nodeGraph

    def getNodeGraph(self) :
        if self.nodeGraph is None:
            Console.warn("NodeGraph None!")
        return self.nodeGraph

    def onReleaseWip(self):
        pass

    def updateView(self):
        self.nodeView.updateView()