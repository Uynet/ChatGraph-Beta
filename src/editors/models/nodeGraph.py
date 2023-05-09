from editors.controllers.nodeGraphController import NodeGraphController
from editors.models.CgpModels import CgpView
from editors.models.edgeModel import EdgeModel
from editors.models.graphs.graphModel import GraphModel
from editors.models.nodeFactory import NodeFactory
from editors.models.nodes.nodeModel import NodeModel
from editors.models.serializer import Serializer
from editors.models.socketModel import SocketModel
from editors.types.dataType import GraphData
from editors.views.nodeScene import NodeScene
from utils.enums import CgpViewType


# sceneと紐づくinstance
class NodeGraph:
    def __init__(self , scene:NodeScene):
        self.scene = scene
        self.controller=NodeGraphController(self)

    def getController(self):
        return self.controller

    def updateView(self):
        nodes = self.getNodeModels()
        for node in nodes:
            node.updateView()
        # for item in self.scene.items():
        #     item.update 

    def addModuleFromGraphData(self,graphJsonData:GraphData, filePath:str):
        filename = filePath.split("/")[-1]
        # 普通にシーンに追加したあとで変換をする
        subGraph : GraphModel = Serializer.dataToGraph(graphJsonData)
        nodes:list[NodeModel] = subGraph.nodes
        # edges:list[EdgeModel] = subGraph.edges

        moduleNode = NodeFactory.nodesToModule(nodes)
        moduleNode.setSubGraph(nodes)
        moduleNode.setProperty("label",filename)
        moduleNode.setProperty("source",filePath)
        moduleNode.addToScene(self.scene)
        return moduleNode

    def clearGraph(self):
        for item in self.scene.items():
                self.scene.removeItem(item) 

    ## CONTROLLERS ############################################
    def removeSocketChain(self,socket:SocketModel):
        socket.removeChain()
        socket.removeFromScene(self.scene)

    def SceneToGraphData(self) -> GraphData:
        nodes = [] 
        edges = []
        scene = self.scene
        nodeViews = scene.getObjectsByTypeSet({CgpViewType.NODE , CgpViewType.HUB})
        for item in nodeViews :
            node:NodeModel = item.nodeModel
            nodes.append(node)
            edges.extend(node.getEdges())
        # filer dups 
        edges = list(set(edges))
        graphData = Serializer.graphToData(GraphModel(nodes,edges))
        return graphData

    # ノードの接続
    def getEdges(self,nodes:list[NodeModel]) -> list[EdgeModel]:
        edges:list[EdgeModel] = []
        for node in nodes:
            edges.extend(node.getEdgesIn(nodes))
        edges = list(set(edges))
        return edges

    def getNodeViews(self):
        return self.scene.getObjectsByTypeSet({CgpViewType.NODE , CgpViewType.HUB})

    def getNodeModels(self) -> list[NodeModel]:
        nodeViews:list[CgpView] = self.getNodeViews()
        nodes = []
        for nodeView in nodeViews:
            nodes.append(nodeView.getModel())
        return nodes


    def find(self,nodeName) -> NodeModel:
        nodes:list[NodeModel] = self.getNodeModels()
        for node in nodes :
            name = node.getProperty("label")
            if name == nodeName:
                return node 
        return None

    def findNodesByType(self ,type) -> list[NodeModel]:
        nodes = self.getNodeModels()
        tNodes = []
        for node in nodes:
            if node.nodeType == type:
                tNodes.append(node)
        return tNodes