from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from editors.controllers.nodeGraphController import NodeGraphController
from utils.enums import EventType
from abc import ABC, abstractmethod


@abstractmethod
class CgpController(ABC):
    def __init__(self):
        pass

    def onEvent(self , ngc:NodeGraphController, eventType:EventType , scene,event):
        assert eventType in {EventType.MOUSE_PRESS,EventType.MOUSE_MOVE,EventType.MOUSE_RELEASE}
        if EventType.MOUSE_PRESS == eventType: self.mousePressEvent(ngc,scene,event)
        if EventType.MOUSE_MOVE== eventType: self.mouseMoveEvent(ngc,scene,event)
        if EventType.MOUSE_RELEASE== eventType: self.mouseReleaseEvent(ngc,scene,event)

    def mousePressEvent(self,ngc,scene, event):
        pass
    def mouseMoveEvent(self,ngc,scene, event):
        pass
    def mouseReleaseEvent(self,ngc,scene, event):
        pass
    def onHover(*args):
        pass
    def onLeave(*args):
        pass
    def getModel(self):
        pass