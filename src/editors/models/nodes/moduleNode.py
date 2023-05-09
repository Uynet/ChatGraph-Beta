# 複数のnodeをまとめたもの

from editors.models.graphs.graphModel import GraphModel
from editors.models.nodes.nodeModel import NodeModel
from editors.models.nodes.textInputNode import TextInputNode
from editors.models.socketModel import SocketModel
from editors.types.dataType import GraphData
from editors.views.nodeView import NodeView
from utils.enums import InOutType, PropertyType
from utils.fileLoader import FileLoader
from utils.util import Console



class ModuleNode(NodeModel):
    def __init__(self):
        nodeType = "ModuleNode" 
        super().__init__(nodeType)
        self.subGraph : GraphModel = GraphModel([],[])
        self.nodeView= NodeView(self)
        self.moduleInputNodes = []

    def loadFile(self):
        filePath = self.getProperty("source")
        self.setProperty("source", filePath)
        FileLoader.loadGraphData(filePath , self.onLoad , self.onFailed) 
    
    # データ整合性チェック
    def onLoad(self , graphData : GraphData):
        from editors.models.serializer import Serializer
        newGraph : GraphModel = Serializer.dataToGraph(graphData)
        self.setSubGraph(newGraph)

    def onFailed(self,e):
        Console.error(f"モジュールの読み込みに失敗しました: {str(e)}")
        self.setProperty("label","failed")

    def connectToInnerNodes(self):
        nodes = self.subGraph.nodes
        for node in nodes:
            if node.nodeType == "TextInputNode":
                node : TextInputNode
                self.moduleInputNodes.append(node)
            if node.nodeType == "OutputNode":
                from editors.models.nodes.outputNode import OutputNode
                node : OutputNode
                node.connectModule(self)

    def addSocketsByNodes(self,nodes):
        for node in nodes:
            node : NodeModel
            if node.nodeType == "TextInputNode":
                node : TextInputNode
                socket = self.addSocket(InOutType.IN,PropertyType.CHAT)
                self.moduleInputNodes.append(node)
                name = node.getProperty("label")
                socket.setName(name)
            if node.nodeType == "OutputNode":
                from editors.models.nodes.outputNode import OutputNode
                node : OutputNode
                node.connectModule(self)
                socket = self.addSocket(InOutType.OUT,PropertyType.CHAT)
                name = node.getProperty("label")
                socket.setName(name)

    def setSubGraph(self,subGraph: GraphModel):
        self.subGraph = subGraph
        
    def getSubGraph (self) -> GraphModel:
        return self.subGraph

    def onInput(self,data:str,socket:SocketModel):
        self.setProperty("inputed", str(data))
        super().onInput( data=data , socket=socket ,propName ="inputed")
        for node in self.moduleInputNodes:
            node : TextInputNode
            name = socket.getName()
            if name == node.getProperty("label"):
                node.setProperty("inputed",data)
                node.onInput( data=data , socket=socket )
                return

        # モジュール内部に対応する入力がない場合
        Console.error("inputが見つかりませんでした")
        # self.setState(NodeProcessState.FINISHED)
        # 入力を内部モジュールの入力箇所にそのまま入力

    # 内部モジュールからの出力を受け取る
    def onOutput(self , data:str , nodeName:str):
        self.setProperty("output",data)
        socs : list[SocketModel] = []
        for outputSocket in self.sockets.outputs:
            if outputSocket.getName()==nodeName:
                socs.append(outputSocket)
        super().onFinished(data=data,propName=nodeName,outSockets=socs)