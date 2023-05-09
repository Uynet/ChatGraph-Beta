from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from editors.controllers.nodeGraphController import NodeGraphController

from PyQt5.QtCore import QRectF, Qt
from PyQt5.QtGui import QColor, QPen
from PyQt5.QtWidgets import QGraphicsRectItem
from editors.controllers.cgpController import CgpController


from utils.enums import CgpViewType
from utils.styles import Styles


class DaragRectView(QGraphicsRectItem):
    def __init__(self,model,sp,ep ):
        super(DaragRectView, self).__init__()
        self.startPos = sp
        self.endPos = ep 
        self.model = model
        self.onResize(sp,ep)
        self.color = Styles.getQColor("edgeNormal")
        self.penwidth = 2
        self.setZValue(5)
    def getBB(self):
        x = min(self.startPos.x(), self.endPos.x())
        y = min(self.startPos.y(), self.endPos.y())
        w = abs(self.startPos.x() - self.endPos.x())
        h = abs(self.startPos.y() - self.endPos.y())
        return QRectF( x  , y , w , h ) 

    def boundingRect(self):
        rect = self.getBB()
        return rect
        return QRectF()

    def onResize( self , sp,ep):
        self.startPos = sp
        self.endPos = ep
        self.update()

    def paint(self, painter, option, widget):
        ec = QColor(255,255,255,255)
        c = QColor(255,255,255,80)
        pen = QPen(ec , self.penwidth, Qt.SolidLine)
        # edgeColor
        rect = self.getBB()
        painter.setPen(pen)
        painter.setBrush(c)
        painter.drawRect(rect)

class DragRect():
    def __init__(self, ngc , pos):
        self.startPos = pos 
        self.endPos = pos 
        self.view = DaragRectView(self, pos, pos) 

    def onMouseMove(self, mousePos):
        self.endPos = mousePos
        self.onResize()

    def onResize(self):
        sp = self.startPos
        ep = self.endPos
        self.view.onResize(sp,ep)
    def addToScene(self,scene):
        scene.addItem(self.view)

    def removeFromScene(self,scene):
        scene.removeItem(self.view)

class DragRectController(CgpController):
    def __init__(self, ngc:NodeGraphController, pos):
        super().__init__()
        self.ngc = ngc
        self.pos = pos
        self.model = DragRect(ngc,pos)
    
    def onFocus(self,ngc,scene,event):
        self.model.addToScene(scene)
    def mousePressEvent(self,ngc,scene, event):
        self.model.removeFromScene(scene)
        self.ngc.resetFocus()

    def mouseMoveEvent(self,ngc,scene, event):
        # get screen pos
        scenePos = event.scenePos()
        # to global pos
        pos = scenePos 
        self.model.onMouseMove(pos)
        pass

    def mouseReleaseEvent(self,ngc,scene, event):
        self.model.removeFromScene(scene)
        rect = self.model.view.getBB()
        # rectの範囲内にあるノードを選択する
        # set = {CgpViewType.NODE , CgpViewType.HUB , CgpViewType.EDGE}
        set = {CgpViewType.NODE , CgpViewType.HUB }
        items = scene.selectNodesByRect(rect, set)
        self.ngc.selectItems(items)
        self.ngc.resetFocus()