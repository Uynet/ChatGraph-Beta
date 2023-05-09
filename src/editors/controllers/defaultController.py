
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QTransform
from editors.controllers.actions.cgpAction import CgpAction
from editors.controllers.cgpController import CgpController

from editors.controllers.dragRect import DragRectController
from editors.controllers.dragWipConnection import DragWipController
from editors.models.edgeModel import EdgeModel
from editors.models.socketModel import SocketModel
from editors.views.nodeWindows.socketView import SocketView
from editors.models.wipEdge import WipEdge
from editors.views.nodeScene import NodeScene
from editors.views.nodeWindows.nodeWindow import NodeWindow
from editors.views.nodeWindows.nodeWindowController import NodeWindowController
from utils.enums import CgpViewType, InOutType
from utils.sound import CSound


# ngc = NodeGraphController
class DefaultController(CgpController):
    def __init__(self , ngc):
        self.ngc = ngc
        super().__init__()
    def getNgc(self):
        return self.ngc

    def mousePressEvent(self,ngc, scene, event):
        from layout.contextMenu import showMenu
        if event.button() == Qt.RightButton:
            item = scene.itemAt(event.scenePos(), QTransform())
            showMenu(scene, event.scenePos(), item)
        if event.button() == Qt.LeftButton:
            self.onLeftClick(scene,event)
        return

    # 通常時にSocketにホバーするとハイライトしたいが、
    # ドラッグ中は接続可能なSocketにホバーしたときのみハイライトしたい
    def mouseMoveEvent(self,ngc,scene:NodeScene,event):
        scene.onHoverItems(event)

    def onLeftClick(self,scene:NodeScene,event):

        set = {CgpViewType.SOCKET,CgpViewType.NODE,CgpViewType.HUB}
        pos = event.scenePos()
        hoveringItem = scene.getHoveringItemByTypes(set , pos)
        cgpViewType = CgpViewType.getFrom(hoveringItem)
        if cgpViewType == CgpViewType.SOCKET:
            self.onClickSocket(scene,event,hoveringItem)
        if cgpViewType in {CgpViewType.NODE , CgpViewType.HUB}:
            self.onClickNode(scene,event,hoveringItem)
        if cgpViewType == CgpViewType.BG:
            self.onClickBG(scene,event,hoveringItem)
        return

    def onClickBG(self,scene,event,hoveringItem):
        ngc = self.getNgc()
        ngc.resetSelect()
        ctrl = DragRectController(ngc,event.scenePos())
        ngc.setFocus(ctrl)
        ctrl.onFocus( ngc,scene,event)

    def onClickNode(self,scene,event,hoveringItem):
        from editors.controllers.nodeGraphController import NodeGraphController
        ngc:NodeGraphController = self.getNgc()
        nodeWindow:NodeWindow = hoveringItem
        ctrl:NodeWindowController = nodeWindow.controller
        ngc.setFocus(ctrl)
        # 最初のフレームだけ呼ばれないので明示的にやる
        ctrl.mousePressEvent(ngc,scene,event)

    def onClickSocket(self,scene,event,hoveringItem):
        ngc = self.getNgc()
        ngc.resetSelect()
        socket :SocketModel= hoveringItem.getModel()
        if socket.hasEdge():
            oSoc = socket.getOppositeSocket()
            self.replaceSocket(oSoc)
            socket = oSoc
        self.onDragStartWipConnection(socket,scene,event.scenePos())
        # if socket.hasEdge():
        #     node = socket.getParent()
        #     ioType = socket.inOutType
        #     propName = socket.propName
        #     name = socket.getName() 
        #     socket = node.addSocket(ioType , propName)

    def onDragStartWipConnection(self,socket:SocketModel ,scene:NodeScene,pos):
        ngc = self.getNgc()
        socketView:SocketView = socket.view
        startPos = socketView.getScenePos()
        flip = socket.inOutType == InOutType.OUT
        wipConnection = WipEdge(startPos , pos,flip )
        wipConnection.addToScene(scene)
        ngc.setFocus(DragWipController(wipConnection, socket))
        CSound.play("connect.wav")
        return
    
    def replaceSocket(self,socket:SocketModel):
        edgeModel:EdgeModel= socket.edge
        action = CgpAction.DEL_EDGE(edgeModel)
        self.ngc.onCgpAction(action)
