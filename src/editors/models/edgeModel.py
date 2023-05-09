from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from editors.models.socketModel import SocketModel

from editors.models.CgpModels import CgpModel
from editors.views.edgeView import EdgeView
from utils.enums import InOutType


class EdgeModel(CgpModel):
    def __init__(self, inSocket:SocketModel, outSocket:SocketModel):
        super().__init__()
        self.inSocket:SocketModel = inSocket
        self.outSocket:SocketModel = outSocket
        assert self.inSocket.inOutType == InOutType.IN
        assert self.outSocket.inOutType == InOutType.OUT
        assert self.inSocket.inOutType != self.outSocket.inOutType

        self.inSocket.connect(self)
        self.outSocket.connect(self)

        sp = self.inSocket.getView().getScenePos()
        ep = self.outSocket.getView().getScenePos()
        self.view = EdgeView(self,sp,ep)
    # 反対側のsocketを返す
    def getOppositeSocket(self, socket:SocketModel) -> SocketModel:
        ioType = socket.inOutType
        if ioType == InOutType.IN:
            return self.outSocket
        elif ioType == InOutType.OUT:
            return self.inSocket
        else:
            raise Exception("invalid ioType")


    def onResize(self):
        sp = self.inSocket.view.getScenePos()
        ep = self.outSocket.view.getScenePos()
        self.view.onResize(sp,ep)

    # onInput # 右 ->
    def onOutput(self , inputText):
        self.inSocket.onInput(inputText)
        self.view.onOutput()
        
        # <- 左
    def onFinished(self):
        self.outSocket.onFinishedOutput()


    def detachSockets(self):
        self.inSocket.disconnect()
        self.outSocket.disconnect()

    # from editors.models.socketModel import SocketModel
    def isConnected(self , socket1,socket2):
        return {socket1,socket2} == {self.inSocket,self.outSocket}

    def addToScene(self,scene):
        scene.addItem(self.view)

    def removeFromScene(self,scene):
        scene.removeItem(self.view)

    def onRemoveSocket(self,socketModel):
        self.detachSockets()
        return

    def getView(self):
        return self.view 