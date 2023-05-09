import numpy as np
from PyQt5.QtCore import QRectF, Qt, QVariantAnimation
from PyQt5.QtGui import QColor, QPainter, QPen
from PyQt5.QtWidgets import QGraphicsItem

defaultWidth = 2

# 常にゆっくり点線が移動する
class StaticAnimation(QVariantAnimation):
    def __init__(self, parent):
        super(StaticAnimation, self).__init__()
        self.parent = parent
        self.setDuration(100)
        self.setStartValue(0)
        self.setEndValue(100)
        self.setLoopCount(-1)
        self.valueChanged.connect(parent.onStaticAnimationValueChanged)
        self.start()

class SimpleLine(QGraphicsItem):
    def __init__(self,direction, sx, sy, ex, ey):
        super(SimpleLine, self).__init__()
        # unselctable

        # true : out -> in
        self.direction = direction

        self.staticAnimation = StaticAnimation(self)
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)
        self.setFlag(QGraphicsItem.ItemIsMovable, True)
        # self.setFlag(QGraphicsItem.ItemSendsGeometryChanges, False)
        # self.setFlag(QGraphicsItem.ItemSendsScenePositionChanges, False)
        self.penwidth = defaultWidth 
        self.dashOffset = 0
        connectedColor = QColor(235, 225, 176)
        self.color = QColor("#939393")
        # self.color = connectedColor

        self.sx = sx
        self.sy = sy
        self.ex = ex
        self.ey = ey
    
    def onStaticAnimationValueChanged(self, value):
        # diection = True / False -> ds = 1 / -1
        ds = -1 if self.direction else 1
        self.dashOffset = self.dashOffset + ds * value/500
        self.update()

    def boundingRect(self):
        return QRectF( self.sx, self.sy, self.ex - self.sx, self.ey - self.sy)

    def curve(self):
        path = self.curveToRight()
        return path
    

    def create_control_points(self, p0, p1):
        dist = np.linalg.norm(p1 - p0)
        direction = (p1 - p0) / dist
        ortho_direction = np.array([-direction[1], direction[0]])

        offset = dist * 0.5  # 距離に応じてオフセットを変更できます

        p2 = p0 + direction * dist / 3 - ortho_direction * offset
        p3 = p1 - direction * dist / 3 - ortho_direction * offset

        return p2, p3



    def onInput(self):
        self.animation = QVariantAnimation()
        self.animation.valueChanged.connect(self.updateColor)
        self.animation.finished.connect(self.resetColor)
        self.animation.setStartValue(0)
        self.animation.setEndValue(1000)
        self.animation.setDuration(1000)  # 1000ms (1秒)
        self.animation.start()

    # t:0-1 -> out : 1-0
    def easeOutExpo(self, t:float):
        q = 2
        return pow(2, -q* t)

    def updateColor(self, value:float):
        t = value /1000
        self.dashOffset -= self.easeOutExpo(t)
        # self.penwidth = defaultWidth + (1-t) * 1
        # serp color
        startColor = QColor("#ff6699")
        disconnectedColor = QColor("#939393")
        endColor = disconnectedColor 
        r = startColor.red() + (endColor.red() - startColor.red()) * t
        g = startColor.green() + (endColor.green() - startColor.green()) *t
        b = startColor.blue() + (endColor.blue() - startColor.blue()) * t
        self.color = QColor(r, g, b)

        self.update()

    def resetColor(self):
        self.update()

    def paint(self, painter, option, widget):
        pen = QPen(self.color, self.penwidth, Qt.DashLine)
        pen.setDashOffset(self.dashOffset)  # ここでオフセットを更新する
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(QPen(self.color, 2, Qt.SolidLine))
        
        # 直線を描画
        painter.drawLine(self.sx, self.sy, self.ex, self.ey)
        # dashed
        painter.setPen(pen)

    
    def setColor(self, color):
        self.color = color
        self.update()
