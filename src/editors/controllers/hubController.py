from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from editors.models.nodes.nodeModel import NodeModel
    from editors.controllers.nodeGraphController import NodeGraphController

from editors.controllers.cgpController import CgpController
from editors.models.CgpModels import CgpView
from utils.enums import EventType


class HubController(CgpController):
    def __init__(self , nodeWindow:CgpView):
       super().__init__()
       self.nodeWindow = nodeWindow
       self.nodeModel = nodeWindow.getModel()

    def onEvent(self,ngc, eventType:EventType , scene,event):
        self.resetPos()
        super().onEvent(ngc,eventType,scene,event)
        self.update()

    def resetPos(self):
        pos = self.nodeWindow.pos()
        nodeModel:NodeModel = self.getModel()
        nodeModel.onChangeProperty("positionX" , str(pos.x()) , isUpdateView=False , isUpdateInspector=True)
        nodeModel.onChangeProperty("positionY" , str(pos.y()) , isUpdateView=False, isUpdateInspector=True)

    def mouseReleaseEvent(self,ngc:NodeGraphController,scene, event):
        ngc.resetFocus()

    def mousePressEvent(self, ngc:NodeGraphController,scene,event):
        self.resetPos()
        ngc.selectItems([self.nodeWindow])

    def getModel(self):
        return self.nodeModel
    def setFlag(self,*args):
        self.nodeWindow.setFlag(*args)  
    def update(self):
        self.nodeWindow.update()