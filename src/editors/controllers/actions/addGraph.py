
from editors.models.edgeModel import EdgeModel
from editors.models.graphs.graphModel import GraphModel
from editors.models.nodes.nodeModel import NodeModel
from editors.models.serializer import Serializer
from utils.sound import CSound
from editors.controllers.actions.cgpAction import CgpAction

class ADD_GRAPH(CgpAction):
    def __init__(self,graph:GraphModel):
        self.graph = graph
        self.edgeActions = []
        self.subGraphData = None
        super().__init__("ADD_GRAPH")

    def doAction(self ,ngc):
        CSound.play("put.wav")
        nodes:list[NodeModel] = self.graph.nodes
        edges:list[EdgeModel] = self.graph.edges
        for node in nodes:
            addNodeAction = CgpAction.ADD_NODE(node)
            addNodeAction.doAction(ngc)
        for edge in edges:
            # ?
            ngc.addToScene(edge)
            # addEdgeAction = CgpAction.ADD_EDGE(edge.socket1,edge.socket2)
            # addEdgeAction.doAction(ngc)

    # def undo(self,ngc):