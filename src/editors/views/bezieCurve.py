import numpy as np
from PyQt5.QtCore import QPointF, QRect, QRectF, Qt, QVariantAnimation
from PyQt5.QtGui import (QColor, QPainter, QPainterPath, QPainterPathStroker,
                         QPen)
from PyQt5.QtWidgets import (QApplication, QGraphicsItem, QGraphicsPathItem,
                             QWidget)

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

class BezierCurve(QGraphicsItem):
    def __init__(self,direction, sx, sy, ex, ey):
        super(BezierCurve, self).__init__()
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

    # 要注意！！！　ここのreturnを解除するとアプリがクラッシュする現象が発生し、原因が不明
    def boundingRect(self):
        return QRectF()
        # sx,syからex,eyまでの矩形を返す
        # x = self.sx
        # y = self.sy
        # w = self.ex - self.sx
        # h = self.ey - self.sy
        # return QRectF(0,0,1200,1200) 
        # rect =  self.curve().boundingRect()
        # return rect

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


    def curveToRight(self):
        # t
        def bezier_point(t, p0, p1, p2, p3):
            mt = 1 - t
            return p0 * mt**3 + 3 * p1 * mt**2 * t + 3 * p2 * mt * t**2 + p3 * t**3

        path = QPainterPath()

        # 新しいtの範囲
        t_start = 0.0
        t_end = 1.0
         # 制御点の計算
        q = 0.5 
        # ちょっと内側によせる
        sx = self.sx + 5 
        sy = self.sy
        ex = self.ex - 5
        ey = self.ey
        cx1 = sx + (ex - sx) * q  
        cy1 = sy + (ey - sy) * (1-q )
        cx2 = sx + (ex - sx) * (1-q )
        cy2 = sy + (ey - sy) * q

        # 新しい始点と終点を計算
        sx_new = bezier_point(t_start, sx, cx1, cx2, ex)
        sy_new = bezier_point(t_start, sy, cy1, cy2, ey)
        ex_new = bezier_point(t_end, sx, cx1, cx2, ex)
        ey_new = bezier_point(t_end, self.sy, cy1, cy2, ey)

        # 新しい始点に移動
        path.moveTo(sx_new, sy_new)

        # 新しい始点と終点を使用して、制御点を再計算
        q = 0.9
        cx1_new = sx_new + (ex_new - sx_new) * q
        cy1_new = sy_new + (ey_new - sy_new) * (1 - q)
        cx2_new = sx_new + (ex_new - sx_new) * (1 - q)
        cy2_new = sy_new + (ey_new - sy_new) * q

        # 新しい制御点を使用してベジエカーブを描画
        path.cubicTo(cx1_new, cy1_new, cx2_new, cy2_new, ex_new, ey_new)

        return path

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
        painter.setRenderHint(QPainter.Antialiasing)
        pen = QPen(self.color, self.penwidth, Qt.DashLine)
        pen.setDashOffset(self.dashOffset)  # ここでオフセットを更新する
        painter.setPen(pen)
        painter.drawPath(self.curveToRight())
    
    def setColor(self, color):
        self.color = color
        self.update()