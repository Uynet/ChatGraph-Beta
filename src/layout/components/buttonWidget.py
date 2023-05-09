from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QPushButton

from utils.styles import Styles
from utils.util import Util


class ButtonWidget(QPushButton):
    def __init__(self, imagePath = None):
        super().__init__(imagePath)
        size = 48
        self.size = size
        garbageIcon = Util.getImageFilePath("paperclaft.png")
        img = QPixmap(garbageIcon).scaled(size,size,Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.setIcon(QIcon(img))
        self.setObjectName("buttonWidget")
        self.setFixedWidth(24)
        s = Styles.qClass("buttonWidget","buttonWidget")
        return
