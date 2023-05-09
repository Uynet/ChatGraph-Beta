import json

from PyQt5.QtCore import Qt

from api.threads import NodeThread
from editors.models.nodes.nodeModel import NodeModel
from editors.models.socketModel import SocketModel
from editors.views.nodeView import NodeView
from utils.enums import InOutType, PropertyType
from utils.sound import CSound
from utils.util import Console

class ExecNode(NodeModel):
    def __init__(self):

        # for exe
        self.input = None
        self.onEndQueue = []

        nodeType = type(self).__name__
        super().__init__( nodeType)
        self.nodeView = NodeView(self)

    def get(self , name ):
        return self.getProperty(name)
    def set(self , name , value):
        if not type(value) in {str,int,float,bool,list}:
            Console.error("not supported type",type(value))
            value = str(value)
        self.addTask(lambda : self.setProperty(name, value , isUpdateInspector=True))

    # defaultの出力先を指定した名前のノードに移動
    # (default , GPT3 , ソケット名)
    def setOutputTo(self , fromSocketName : str, toNodeName : str , toSocketName = ""):
        pass
        # from editors.models.nodeGraph import NodeGraph
        # from editors.models.socketModel import SocketModel

        # nodeGraph :NodeGraph = self.getNodeGraph() 
        # node : NodeModel = nodeGraph.find(toNodeName)
        # # default
        # fromSocket :SocketModel= self.sockets.outputs[0]

        # if node == None:
        #     raise Exception("Error:node not found <" + toNodeName + ">")

        # # 接続先が同じなら何もしない
        # toSocket : SocketModel = node.sockets.inputs[0]
        # assert toSocket is not None
        # isconnected : bool = fromSocket.isConnected(toSocket)
        # if isconnected : return
        # else :
        #     if fromSocket.hasEdge():
        #         self.addTask(lambda:nodeGraph.removeConnection(fromSocket.edge))
        #     self.addTask(lambda:nodeGraph.createConnection(fromSocket, toSocket))

    def setIconSize(self , size):
        self.nodeView.nodeWindow.iconImage.resize(size)

    def addTask(self, task):
        self.onEndQueue.append(task)
        self.currentThread.task.emit("onAddTask")

    def onAddTask(self, data):
        while self.onEndQueue != []:
            task = self.onEndQueue.pop(0)
            task()

    def onInput(self,data:str,propName:str,socket:SocketModel):
        data = str(data)
        if propName in { "inputed" , "output"}:
            propertyType =  PropertyType.CHAT
        else:
            propertyType =  PropertyType.SET

        # fix this!
        if propertyType == PropertyType.CHAT:
            super().onInput( data=data , socket=socket ,propName ="inputed")
            self.onInputToChat(data , socket)
        elif propertyType == PropertyType.SET: 
            self.onInputSet(data ,propName,socket)

    def onInputToChat(self, data , socket:SocketModel = None):
        self.setProperty("inputed", str(data))

        script = self.getProperty("script")
        data = self.getProperty("inputed")

        self.input = data
        if self.currentThread != None:
            self.currentThread.onInputRunning(data)
        else:
            thread = NodeThread(script , self, data)
            thread.result.connect(self.onChatResult, Qt.QueuedConnection)  
            if socket != None:
                thread.result.connect(socket.onFinished, Qt.QueuedConnection)  

            thread.task.connect(self.onAddTask, Qt.QueuedConnection)
            thread.stream.connect(self.onStream, Qt.QueuedConnection)
            thread.finished.connect(self.onEnd , Qt.QueuedConnection)
            self.setThread(thread)

    def onInputSet(self, data , propName ,socket:SocketModel):
        self.setProperty(propName, data)
        socket.onFinished()
        # no output
        outSockets =[]
        super().onFinished(data = data , propName=propName ,outSockets=outSockets)


    def onEnd(self):
        if self.currentThread != None:
            self.currentThread.deleteLater()
            self.currentThread = None

     ## API
    def stream(self , data:str ,isOutput = False , socket="Default"):
        result = ({
            "state":"SUCCESS",
            "answer":str(data),
            "isOutput":str(isOutput),
            "socket":str(socket)
        })
        self.currentThread.stream.emit(json.dumps(result))

    def onStream(self , data:str):
        CSound.play("chat.wav")
        resut = json.loads(data)
        answer = resut["answer"]
        self.setProperty("output", answer , isUpdateInspector=True)
        isOutput = resut["isOutput"]
        if isOutput == "True":
            target = resut["socket"]
            outSockets = self.selectOutSocket(target)
            super().onFinished(data=answer , propName="output" ,outSockets=outSockets)

    def selectOutSocket(self , name:str):
        outSockets = self.sockets.outputs
        for socket in outSockets:
            if socket.getName() == name:
                return [socket]
        return outSockets

    def onChatResult(self, result:str):
        result = json.loads(result)

        answer = result["answer"]
        state = result["state"]
        isError = state != "SUCCESS" 
        self.setProperty("output", answer)
        if isError: target = "Error"
        else: target = "Default"

        outSockets = self.selectOutSocket(target)
        super().onFinished(data=answer , propName="output" ,outSockets=outSockets)