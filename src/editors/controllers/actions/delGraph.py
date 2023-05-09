from editors.controllers.actions.addnode import ADD_NODE
from editors.models.graphs.graphModel import GraphModel
from editors.models.nodes.nodeModel import NodeModel
from editors.models.serializer import Serializer
from editors.models.socketModel import SocketModel
from utils.sound import CSound
from editors.controllers.actions.cgpAction import CgpAction

class DEL_GRAPH(CgpAction):
    def __init__(self,nodes:list[NodeModel]):
        self.nodes = nodes
        self.edgeActions = []
        self.subGraphData = None
        super().__init__("DELETE_GRAPH")

    def doAction(self ,ngc):
        CSound.play("stop.wav")
        nodeModels = self.nodes
        nodeGraph = ngc.nodeGraph
        edges = nodeGraph.getEdges(nodeModels)
        subGraph = GraphModel(nodeModels,edges) 
        self.subGraphData = Serializer.graphToData(subGraph)

        for node in self.nodes:
            deleteAction = (CgpAction.DEL_NODE(node))
            deleteAction.doAction(ngc)

    def undo(self,ngc):
        CSound.play("put.wav")
        addGraphAction = CgpAction.ADD_GRAPH(Serializer.dataToGraph(self.subGraphData))
        ngc.onCgpAction(addGraphAction,undo=True)