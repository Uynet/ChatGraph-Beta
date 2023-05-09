
from editors.controllers.actions.cgpAction import CgpAction
from editors.models.nodeFactory import NodeFactory
from editors.models.socketModel import SocketModel


class ADD_EDGE(CgpAction):
    def __init__(self,s1:SocketModel ,s2:SocketModel):
        self.s1 = s1
        self.s2 = s2
        super().__init__("ADD_EDGE")

    def doAction(self ,ngc):
        edgeModel = NodeFactory.createEdge(self.s1,self.s2)
        ngc.addToScene(edgeModel)