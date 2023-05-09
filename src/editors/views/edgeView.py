from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from editors.models.edgeModel import EdgeModel

from PyQt5.QtCore import QRectF, Qt, QTimer, QVariantAnimation, QPointF
from PyQt5.QtGui import QPen
from PyQt5.QtWidgets import QGraphicsItem, QGraphicsRectItem
from utils.styles import Styles

class EdgeView(QGraphicsRectItem ):
    def __init__(self,model,sp:QPointF,ep :QPointF, flip = False):
        x = min(sp.x() , ep.x())
        y = min(sp.y() , ep.y())
        w = abs(sp.x() - ep.x())
        h = abs(sp.y() - ep.y())
        super(EdgeView, self).__init__(x,y,w,h)
        self.startPos = sp
        self.endPos:QPointF = ep 
        self.model:EdgeModel= model
        self.flip = flip
        self.setPos(0,0)
        # # self.glView = EdgeLine(model , self)
        # self.proxyWidget = QGraphicsProxyWidget(self)
        # self.proxyWidget.setWidget(self.glView)
        # self.proxyWidget.setParentItem(self)
        # self.onResize(sp,ep)
        self.phase = 0
        self.color = Styles.getQColor("edgeNormal")
        self.penwidth = 2
        self.timer = QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(16)  # Update every 16 ms (approx. 60 FPS)
        self.vel = 0.1
        # Z Value
        self.setZValue(-3)

        # selectable
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges)
        self.setFlag(QGraphicsItem.ItemSendsScenePositionChanges, True)


    def getBB(self):
        x = min(self.startPos.x(), self.endPos.x())
        y = min(self.startPos.y(), self.endPos.y())
        w = abs(self.startPos.x() - self.endPos.x())
        h = abs(self.startPos.y() - self.endPos.y())
        return QRectF( x  , y , w , h ) 

    def setOpacity(self, opacity: float) -> None:
        return super().setOpacity(opacity)

    def onResize( self , sp,ep):
        self.startPos = sp
        self.endPos = ep
        rect = self.getBB()
        # self.proxyWidget.setGeometry(rect)
        # self.glView.onResize(sp,ep)

    def update(self):
        sign = -1 if self.flip else 1
        self.phase += sign * self.vel
        super().update()

    def easeOutExpo(self, t:float):
        q = 2
        return pow(2, -q* t)

    def speedUp(self, value):
        t = value /1000
        self.vel = 0.1 + 0.7 * self.easeOutExpo(t)

    def resetColor(self):
        self.color = Styles.getQColor("edgeNormal")
        self.vel = 0.1

    def onSelect(self):
        self.setSelected(True)

    def onDeselect(self):
        self.setSelected(False)

    #### Events
    def onOutput(self):
        self.color = Styles.getQColor("edgeActive")
        self.animation = QVariantAnimation()
        self.animation.valueChanged.connect(self.speedUp)
        self.animation.finished.connect(self.resetColor)
        self.animation.setStartValue(0)
        self.animation.setEndValue(1000)
        self.animation.setDuration(1000)  # 1000ms (1秒)
        self.animation.start()

    def paint(self, painter, option, widget):
        if self.isSelected():
            c = Styles.getQColor("nodeSelected")
        else :
            c = self.color
        pen = QPen(c, self.penwidth, Qt.DashLine)
        pen.setDashOffset(self.phase)
        painter.setPen(pen)
        painter.drawLine( self.startPos , self.endPos )

    def getModel(self):
        return self.model