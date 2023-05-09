import PyQt5.QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QSplashScreen

from utils.util import Util


# ロード中に出るロゴ
class SplashScreen(QSplashScreen):
    def __init__(self):
        super().__init__()
        self.setPixmap(PyQt5.QtGui.QPixmap(Util.getImageFilePath("splash.png")))
        self.setWindowFlags(PyQt5.QtCore.Qt.WindowStaysOnTopHint | PyQt5.QtCore.Qt.FramelessWindowHint)
        self.setMask(self.pixmap().mask())
        # エラーログよりしたに
        self.setWindowFlags(Qt.SplashScreen | Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.show()

