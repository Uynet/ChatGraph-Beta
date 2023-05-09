
from editors.controllers.actions.cgpAction import CgpAction
from editors.models.nodes.nodeModel import NodeModel
from editors.models.serializer import Serializer
from editors.models.socketModel import SocketModel


class DEL_NODE(CgpAction):
    def __init__(self,node:NodeModel):
        self.node = node
        self.edgeActions = []
        self.nodeData = Serializer.nodeToJson(node) 
        super().__init__("DELETE_NODE")

    def doAction(self ,ngc):
        # CSound.play("stop.wav")
        # nodeModels = self.nodes
        nodeGraph = ngc.nodeGraph
        # edges = nodeGraph.getEdges(nodeModels)
        # subGraph = GraphModel(nodeModels,edges) 
        # self.subGraphData = Serializer.graphToData(subGraph)
        node = self.node
        for socket in node.getAllSockets():
            socket : SocketModel
            if socket.hasEdge():
                edge = socket.edge
                action = (CgpAction.DEL_EDGE(edge))
                self.edgeActions.append(action)
                action.doAction(ngc) 
        node.removeFromScene(nodeGraph.scene)

    def undo(self,ngc):
        pass
        # CSound.play("put.wav")
        # print(self.subGraphData)