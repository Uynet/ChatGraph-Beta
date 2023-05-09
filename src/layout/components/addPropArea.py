from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QPushButton

from utils.util import Util

class AddPropArea(QPushButton):
    def __init__(self,nodeModel):
        super().__init__()
        size = 48
        self.size = size
        from editors.models.nodes.nodeModel import NodeModel
        self.nodeModel:NodeModel = nodeModel
        garbageIcon = Util.getImageFilePath("addArea.png")
        img = QPixmap(garbageIcon).scaled(size,size,Qt.KeepAspectRatio, Qt.SmoothTransformation)
        # self.setIcon(QIcon(img))
        self.setObjectName("buttonWidget")
        self.setFixedHeight(24)
        self.setText("+ Add Prop")
        # s = Styles.qClass("buttonWidget","buttonWidget")
        return

    def mousePressEvent(self, event) -> None:
        if event.button() == Qt.LeftButton:
            self.onClick()
        return super().mousePressEvent(event)

    def onClick(self):
        label = "custom"
        typeSet = {}
        self.nodeModel.addSlot(label,typeSet)

