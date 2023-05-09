from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGraphicsScene

from utils.enums import CgpViewType, EventType


class NodeScene(QGraphicsScene):
    def __init__(self):
        super().__init__()
        from editors.models.nodeGraph import NodeGraph
        self.nodeGraph = NodeGraph(self)

    def addItem(self, item ) -> None:
        super().addItem(item)

    def removeItem(self, item ) -> None:
        if CgpViewType.getFrom(item) == CgpViewType.NODE:
            nodeView = CgpViewType.getRoot(item)
            nodeModel = nodeView.getModel()
            nodeModel.onStop()
        super().removeItem(item)

    def getGraphView(self):
        return self.views()[0]

    def selectNodesByRect(self , rect , typeSet = {}):
        items = self.items(rect)
        node_items = [item for item in items if CgpViewType.getFrom(item) in typeSet]
        return node_items

    def getObjectsByTypeSet(self, type_set):
        result = []
        for item in self.items():
            itemCgpViewType = CgpViewType.getFrom(item)
            if itemCgpViewType in type_set:
                result.append(CgpViewType.getRoot(item))
        return result

    # 指定したtypeの中で、最も手前にあるものを返す
    # (Zindexが最大)
    def getHoveringItemByTypes(self, cgpViewTypes, scene_pos):
        result = []
        for cgpViewType in cgpViewTypes:
            items_at_pos = self.items(scene_pos, Qt.IntersectsItemShape, Qt.AscendingOrder)
            items = [item for item in items_at_pos]
            
            for item in items:
                itemCgpViewType = CgpViewType.getFrom(item) 
                if itemCgpViewType == cgpViewType:
                    result.append(CgpViewType.getRoot(item))
        if len(result) == 0:
            return None
        result.sort(key=lambda x: x.zValue())
        return result[-1]

    def onHoverItems(self , event , typeSet={CgpViewType.NODE, CgpViewType.SOCKET , CgpViewType.HUB}):
        scene_pos = event.scenePos()
        allItems = self.getObjectsByTypeSet(typeSet)
        # 重複を削除
        allItems = list(set(allItems))
        nearestItem = self.getHoveringItemByTypes(typeSet, scene_pos)

        for item in allItems:
            if item == nearestItem:
                nearestItem.onHover(event)
            else: item.onLeave(event)

    ##### EVENT #####

    def mousePressEvent(self, event):
        eventType = EventType.MOUSE_PRESS 
        self.nodeGraph.controller.onEvent(eventType,self, event)
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        eventType = EventType.MOUSE_MOVE
        self.nodeGraph.controller.onEvent(eventType,self, event)
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event): 
        eventType = EventType.MOUSE_RELEASE
        self.nodeGraph.controller.onEvent(eventType,self, event)
        super().mouseReleaseEvent(event)

    def wheelEvent(self, event):
        eventType = EventType.MOUSE_WHEEL
        self.nodeGraph.controller.onEvent(eventType,self, event)
        super().wheelEvent(event)

    def keyPressEvent(self, event):
        self.nodeGraph.controller.keyPressEvent(self, event)
        super().keyPressEvent(event)