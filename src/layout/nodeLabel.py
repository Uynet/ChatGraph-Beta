from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel

from editors.types.dataType import NodeViewData
from utils.styles import Styles


class OpenToggleButton (QLabel):
    # 0 : open
    # 1 : close
    def __init__(self , parent):
        super().__init__()
        self.area = parent 
        from utils.util import Util
        openArrowSvg = Util.getImageFilePath("openArrow.svg")
        closeArrowSvg = Util.getImageFilePath("closeArrow.svg")
        self.setMouseTracking(True)
        self.setFixedWidth(20)
        self.setFixedHeight(20)
        self.state = 0
        self.imgs = [openArrowSvg, closeArrowSvg]
        # set Icon
        self.setIcon()
    def setIcon(self):
        self.setPixmap(QPixmap(self.imgs[self.state]))

    def toggle(self, event):
        if(self.state ==  0): self.state = 1
        elif (self.state == 1): self.state = 0
        self.setIcon()

    def setTo(self, state):
        self.state = state
        self.setIcon()
        
    def mousePressEvent(self, event) -> None:
        # 右クリックでメニューを表示
        if event.button() == Qt.LeftButton:
            area = self.area
            self.toggle(event)
            area.onClick(self)
        return super().mousePressEvent(event)

# output ..とか書いてるとこ
class PropertyLabel(QLabel):
    def __init__(self,nodeModel, text  ):
        super().__init__(text)
        self.nodeModel = nodeModel
        self.setStyleSheet( Styles.className("propertyLabelStatic","nodeWidget.scss"))
    # generating
    def inActive(self):
        return
        self.setStyleSheet( Styles.className("propertyLabelActive","nodeWidget.scss"))
        pass
    # generating
    def onFinished(self, data , propName):
        return
        self.setStyleSheet( Styles.className("propertyLabelStatic","nodeWidget.scss"))
        pass
    def onInput(self,**kwargs):
        self.inActive()

    def updateView(self):
        pass

    def initProoperties(self,nodeData:NodeViewData):
        pass
    
    def contextMenuEvent(self, event):
        from layout.contextMenu import showNodePropertyMenu 
        propName = self.text()
        gpos = event.globalPos()
        showNodePropertyMenu(self.nodeModel ,  propName,gpos)

    