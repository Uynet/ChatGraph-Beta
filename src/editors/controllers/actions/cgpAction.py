from __future__ import annotations
from typing import TYPE_CHECKING

from editors.models.graphs.graphModel import GraphModel
if TYPE_CHECKING:
    from editors.controllers.nodeGraphController import NodeGraphController
from abc import ABC, abstractmethod
from editors.models.edgeModel import EdgeModel



@abstractmethod
class CgpAction(ABC):
    @staticmethod
    def ADD_GRAPH(graph:GraphModel):
        from editors.controllers.actions.addGraph import ADD_GRAPH
        return ADD_GRAPH(graph)
    def DEL_GRAPH(nodes):
        from editors.controllers.actions.delGraph import DEL_GRAPH
        return DEL_GRAPH(nodes) 

    def ADD_NODE(node):
        from editors.controllers.actions.addnode import ADD_NODE
        return ADD_NODE(node) 
    def DEL_NODE(node):
        from editors.controllers.actions.delNode import DEL_NODE
        return DEL_NODE(node)

    def ADD_EDGE(s1,s2):
        from editors.controllers.actions.addEdge import ADD_EDGE
        return ADD_EDGE(s1,s2) 
    def DEL_EDGE(edge:EdgeModel):
        from editors.controllers.actions.delEdge import DEL_EDGE
        return DEL_EDGE(edge)

    def __init__(self,name) :
        self.name = name

    def getName(self):
        return self.name

    def doAction(self,ngc:NodeGraphController):
        print("missing doAction" , self.getName())
        pass

    def undo(self,ngc:NodeGraphController):
        print("missing undo" , self.getName())
        pass