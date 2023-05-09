from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from editors.models.nodeGraph import NodeGraph

from collections import deque

from PyQt5.QtCore import Qt
from editors.controllers.actions.cgpAction import CgpAction
from editors.controllers.cgpController import CgpController

from editors.controllers.defaultController import DefaultController
from editors.models.CgpModels import CgpModel, CgpView
from editors.models.edgeModel import EdgeModel
from editors.models.graphs.graphModel import GraphModel
from editors.models.nodes.nodeModel import NodeModel
from editors.models.serializer import Serializer
from editors.models.socketModel import SocketModel
from editors.views.nodeWindows.nodeWindow import NodeWindow
from utils.enums import CgpViewType, EventType

class SelectedItemGroup:
    def __init__(self, nodeGraphController:NodeGraphController):
        self.nodeGraphController = nodeGraphController
        self.selectedItems:CgpView = []

    def setSelect(self , items:list[CgpView]):
        self.selectedItems = items
        for item in items:
            item.onSelect()
    def getItem(self , typeset:set(CgpViewType) = {}):
        if typeset == {}:
            return self.selectedItems
        # dummy
        ret = []
        for item in self.selectedItems:
            vt = CgpViewType.getFrom(item)
            if vt in typeset:
                ret.append(item)
        print(ret)
        return ret

class NodeGraphController:
    def __init__(self , nodeGraph:NodeGraph):
        self.props = []
        self.nodeGraph = nodeGraph
        self.selectedItems = SelectedItemGroup(self)
        # for ctrl+z
        self.actionQueue = deque(maxlen=32)
        self.clipboard = None
        # single 
        self.defaultController = DefaultController(self)
        self.focusedController = self.defaultController 
        
    def getFocusedController(self) -> CgpController:
        return self.focusedController
    def setFocus(self, focus):
        self.focusedController = focus

    def resetSelect(self):
        nodes = self.selectedItems.getItem() 
        for node in nodes: 
            node.onDeselect()
        self.selectedItems.setSelect([])

    def selectItems(self,items:list[CgpView]):
        for item in self.selectedItems.getItem():
            item .onDeselect()
        self.selectedItems.setSelect(items)
        for item in items:
            item.onSelect()

    def addToScene(self ,modelItem : CgpModel):
        modelItem.addToScene(self.scene())

    def scene(self):
        return self.nodeGraph.scene
    def getFocus(self):
        return self.focusedController
    def resetFocus(self):
        self.focusedController = self.defaultController 
    ### EVENT THROWER ############################################
    def onEvent(self , eventType:EventType, scene , event):
        focused = self.getFocusedController()
        focused.onEvent(self,eventType, scene , event )
        # 重い気がするがとりあえず
        # self.nodeGraph.updateView()

    def onCgpAction(self, cgpAction:CgpAction , undo=False ,redo=False):
        if not (undo or redo): self.actionQueue.append(cgpAction)
        cgpAction.doAction(self)
        self.nodeGraph.updateView()

    def onEdit(self,scene , eventName , event):

        focusedItem = scene.focusItem()
        if focusedItem is not None:
            return

        if eventName == "cut": self.onCut()
        elif eventName == "copy": self.onCopy(scene)
        elif eventName == "paste": self.onPaste(scene)
        elif eventName == "undo": self.onUndo()
        # elif eventName == "redo": self.onRedo(scene)
        return

    def setProp(self, nodeModel:NodeModel , name, value , isUpdateView = True , isUpdateInspector = False):
        nodeModel.setProperty(name, value , isUpdateView , isUpdateInspector)
        return

    def onUndo(self):
        if len(self.actionQueue) == 0:
            return
        action = self.actionQueue.pop()
        action.undo(self)
        pass

    def onRedo(self,scene):
        pass

    def onCut(self):
        nodeWindows:list[NodeWindow] = self.selectedItems.getItem({CgpViewType.NODE})
        nodeModels = [nodeWindow.getModel() for nodeWindow in nodeWindows] 
        deleteAction = CgpAction.DEL_GRAPH(nodeModels)
        self.onCgpAction(deleteAction)

    def onCopy(self,scene):
        nodeWindows:list[NodeWindow] = self.selectedItems.getItem({CgpViewType.NODE})
        nodeModels = [nodeWindow.nodeModel for nodeWindow in nodeWindows]
        nodeGraph :NodeGraph = self.nodeGraph
        edges = nodeGraph.getEdges(nodeModels)
        subGraph = GraphModel(nodeModels,edges) 
        subGraphData = Serializer.graphToData(subGraph)
        self.clipboard = subGraphData
        # Console.log("🔥copy" , subGraphData)

    def onPaste(self,scene):
        if self.clipboard is None:
            return
        subGraphData = self.clipboard
        graph = Serializer.dataToGraph(subGraphData)
        addGraphAction = CgpAction.ADD_GRAPH(graph)
        self.onCgpAction(addGraphAction)
        # nodes = graph.nodes
        # for node in nodes:
        #     # 完全に同じ位置だと分かりづらいので、少しずらす
        #     offset = 10 
        #     x = node.getProperty("positionX")
        #     y = node.getProperty("positionX")
        #     node.setProperty("positionX", x + offset)
        #     node.setProperty("positionY", y + offset)
        #     addNodeAction = CgpAction.ADD_NODE(node)
        #     self.onCgpAction(addNodeAction)

    # ctrl + z
    def keyPressEvent(self, scene, event):
        if event.key() == Qt.Key_V and event.modifiers() == Qt.ControlModifier:
            self.onEdit(scene, "paste" , event)
        if event.key() == Qt.Key_C and event.modifiers() == Qt.ControlModifier:
            self.onEdit(scene, "copy" , event)
        if event.key() == Qt.Key_X and event.modifiers() == Qt.ControlModifier:
            self.onEdit(scene, "cut" , event)
        if event.key() == Qt.Key_Z and event.modifiers() == Qt.ControlModifier:
            self.onEdit(scene, "undo" , event)
        if event.key() == Qt.Key_Y and event.modifiers() == Qt.ControlModifier:
            self.onEdit(scene, "redo" , event)
        else:
            return