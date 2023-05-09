from __future__ import annotations
from typing import TYPE_CHECKING

from editors.models.nodes.nodeModel import NodeModel
if TYPE_CHECKING:
    from editors.controllers.nodeGraphController import NodeGraphController
    from editors.models.wipEdge import WipEdge
from editors.controllers.actions.cgpAction import CgpAction
from editors.controllers.cgpController import CgpController
from editors.models.nodes.hubNode import HubNode
from editors.models.socketModel import SocketModel
from editors.views.nodeWindows.socketView import SocketView
from editors.views.nodeScene import NodeScene
from utils.enums import CgpViewType, EventType
from utils.sound import CSound


class DragWipController(CgpController):
    def __init__(self , wipConnection:WipEdge , socket:SocketModel):
        super().__init__()
        self.wipEdge = wipConnection
        self.startSocket = socket
        # ホバー中のもの
        self.hoveringItem= None
        self.hoverSearchSet = {CgpViewType.SOCKET,CgpViewType.NODE,CgpViewType.HUB,CgpViewType.BG}

    def onEvent(self,ngc:NodeGraphController,eventType:EventType,scene,event):
        assert self.wipEdge is not None
        assert self.startSocket is not None
        super().onEvent(ngc,eventType,scene,event)

    def mousePressEvent(self,ngc:NodeGraphController,scene:NodeScene, event):
        # ドラッグ中にクリックしている場合
        ngc.resetFocus()
        scene.removeItem(self.wipEdge)
        return

    def mouseMoveEvent(self,ngc:NodeGraphController,scene:NodeScene, event):
        # 接続可能ソケットの時だけいい感じにハイライトする用
        pos = event.scenePos()
        self.wipEdge.onMouseMove( pos )

        # ??? 
        scene.onHoverItems(event,{CgpViewType.SOCKET,CgpViewType.HUB})

        self.hoveringItem = scene.getHoveringItemByTypes(self.hoverSearchSet,pos)

        cgpViewType = CgpViewType.getFrom(self.hoveringItem) 
        if cgpViewType == CgpViewType.SOCKET:
            socketView:SocketView = self.hoveringItem
            socketModel :SocketModel = socketView.getModel()
            # if not socketModel.isConnectableTo(self.startSocket):
            #     self.hoveringItem.onLeave(event)

    def mouseReleaseEvent(self,ngc:NodeGraphController,scene, event):
        self.wipEdge.onRelease(scene)
        ngc.resetFocus()

        hoveringItem = self.hoveringItem 
        cgpViewType = CgpViewType.getFrom(hoveringItem)
        if cgpViewType == CgpViewType.SOCKET:
            socketView:SocketView = hoveringItem
            socketModel = socketView.getModel() 
            node:NodeModel = socketModel.parentNodeModel 
            if isinstance(node,HubNode):
                # HUBノードのソケット
                self.onDropToHub(ngc,node)
            else :
                self.onDropToSocket(ngc,hoveringItem)
        # HUBノード
        elif cgpViewType == CgpViewType.HUB:
            model = hoveringItem.getModel()
            self.onDropToHub(ngc,model)

        # 接続のないソケットを削除
        startNode = self.startSocket.parentNodeModel
        startNode.onReleaseWip()

    def onDropToHub(self,ngc,hubModel:HubNode):
        # 自己結合は禁止
        n1 = self.startSocket.parentNodeModel
        if(n1==hubModel):
            CSound.play("stop.wav")
            return
        eio = self.startSocket.inOutType.other()

        soc = hubModel.addSocket(inOutType=eio,propName="none")
        soc.view.setZValue(1)
        self.tryConnect(soc,ngc)

    def onDropToSocket(self,ngc:NodeGraphController,hoverItem:SocketView):
        endSocketView:SocketView = hoverItem 
        endSocket:SocketModel = endSocketView.getModel()
        self.tryConnect(endSocket,ngc)

    def tryConnect(self,endSocket:SocketModel,ngc:NodeGraphController):
        if self.startSocket.isConnectableTo(endSocket):
            createEdgeAction = CgpAction.ADD_EDGE(self.startSocket,endSocket)
            ngc.onCgpAction(createEdgeAction)
            CSound.play("connect.wav")
        else :
            CSound.play("stop.wav")
