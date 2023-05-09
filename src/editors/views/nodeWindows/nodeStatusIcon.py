import math

from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QGraphicsPixmapItem


class NodeStatusIcon(QGraphicsPixmapItem):
    def __init__(self, nodeModel , nodeWindow):
        super().__init__()
        self.pm = None
        self.nodeModel = nodeModel
        self.nodeWindow = nodeWindow
        self.iconPath = None
        ww  = nodeWindow.boundingRect().width()
        self.size = 30
        self.setPos(60, -self.size-20)
        self.setZValue(1)
        self.setParentItem(nodeWindow)
        self.timer = QTimer()
        self.timer.timeout.connect(self.updateView)
        self.timer.start(16)  # updateView every 16 ms (approx. 60 FPS)
        self.time = 0
        self.iconPath ="./resources/images/thinking.png" 
        self.setPath(self.iconPath)

    def getNodeView(self):
        return self.nodeModel.nodeView

    def resize(self , size):
        self.size = size
        newicon = self.pm.scaled(size, size, Qt.KeepAspectRatio,Qt.SmoothTransformation)
        self.setPixmap(newicon)

    def setPath(self, path):
        self.iconPath = path 
        if self.pm is None:
            self.pm = QPixmap()
        self.pm.load(path)
        newicon = self.pm.scaled(self.size, self.size, Qt.KeepAspectRatio,Qt.SmoothTransformation)
        self.setPixmap(newicon)

    def updateView(self):
        self.time += 1
        # sin で上下に揺れる
        a = 3
        v = 0.05 
        x = 40
        y = -36
        self.setPos(x, -self.size+y + a * math.sin(self.time * v))

        pass