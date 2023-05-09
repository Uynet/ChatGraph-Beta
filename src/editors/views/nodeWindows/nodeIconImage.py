from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QGraphicsPixmapItem

from editors.types.dataType import NodeViewData


class NodeIconImage(QGraphicsPixmapItem):
    def __init__(self, nodeModel , nodeWindow):
        super().__init__()
        self.pm = None
        self.nodeModel = nodeModel
        self.nodeWindow = nodeWindow
        self.iconPath = None
        self.setPos(0, 0)
        self.size = 50
        self.setZValue(1)
        self.setParentItem(nodeWindow)

    def getNodeView(self):
        return self.nodeModel.nodeView

    def resetTransform(self):
        self.setTransformOriginPoint(self.boundingRect().center())
        windowWidth = self.nodeWindow.boundingRect().width()
        # newX =  windowWidth - self.boundingRect().width() - 5  
        newX = - 5  
        newY = -5 - self.boundingRect().height() 
        self.setPos(newX, newY)

    def resize(self , size):
        self.size = size
        newicon = self.pm.scaled(size, size, Qt.KeepAspectRatio,Qt.SmoothTransformation)
        self.setPixmap(newicon)
        self.resetTransform()

    def setPath(self, path):
        self.iconPath = path 
        if self.pm is None:
            self.pm = QPixmap()
        self.pm.load(path)
        newicon = self.pm.scaled(self.size, self.size, Qt.KeepAspectRatio,Qt.SmoothTransformation)
        self.setPixmap(newicon)
        # not found
        if self.pm.isNull():
            iconPath = "./resources/images/chatIcons/defaults/TextInputNode.png"
            self.pm.load(iconPath)
            self.iconPath = iconPath
            # self.setPath(iconPath)

        self.resetTransform()

    # ウインドウが動くたびにアイコンが更新されてるっぽいので直したほうがいいよ
    def update(self):
        iconPath = self.nodeModel.getProperty("icon")
        # if self.iconPath == iconPath:
        #     return
        self.iconPath = iconPath
        self.setPath(self.iconPath)

    def initProperties(self,nodeData:NodeViewData):
        self.iconPath = nodeData.get("icon")
        self.setPath(self.iconPath)