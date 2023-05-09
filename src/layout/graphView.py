from PyQt5.QtCore import QPointF, Qt
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QGraphicsView

from utils.styles import Styles


class GraphView(QGraphicsView):
    def __init__(self,scene):
        super().__init__()
        self.setScene(scene)
        self.setRenderHint(QPainter.Antialiasing)
        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)

        self.middle_mouse_pressed = False
        self.last_mouse_pos = QPointF()
        # for dev
        size = 3000
        x = y = -size
        w = h = size * 2
        self.setSceneRect(x, y, w, h)
        # 初期位置を設定
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.AnchorUnderMouse)

        s = Styles.qClass("graphView","QScrollBar","graphView.scss")
        self.setStyleSheet(s)
        # グリッド
        # self.gridItem = GridItem(self)
        # scene.addItem(self.gridItem)

    def mousePressEvent(self, event):
        if event.button() == Qt.MiddleButton:
            self.middle_mouse_pressed = True
            self.last_mouse_pos = event.pos()
            self.setCursor(Qt.ClosedHandCursor)
        super(GraphView, self).mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MiddleButton:
            self.middle_mouse_pressed = False
            self.setCursor(Qt.ArrowCursor)
        super(GraphView, self).mouseReleaseEvent(event)

    def mouseMoveEvent(self, event):
        if self.middle_mouse_pressed:
            delta = self.mapToScene(event.pos()) - self.mapToScene(self.last_mouse_pos)
            self.setTransformationAnchor(QGraphicsView.NoAnchor)
            self.translate(delta.x(), delta.y())
            self.last_mouse_pos = event.pos()
        super(GraphView, self).mouseMoveEvent(event)

    def wheelEvent(self, event):
        delta = event.angleDelta().y()
        if delta > 0:
            self.scale(1.1, 1.1)
        elif delta < 0:
            self.scale(1 / 1.1, 1 / 1.1)
        event.ignore()
        # return super().wheelEvent(event)