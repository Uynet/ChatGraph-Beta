from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QSplitter, QVBoxLayout, QWidget

from editors.types.dataType import NodeViewData
from editors.views.nodeWindows.propertyArea import NodePropertyArea
from layout.components.addPropArea import AddPropArea
from utils.enums import PropertyType
from utils.styles import Styles

# ウインドウ上部の幅
flameHeight = 20
pad = 15

defaultFieldTypeSet = {
     PropertyType.CHAT,
     None
}


class NodeWidget(QWidget):
    def __init__(self,nodeWindow , nodeView , nodeModel):
        super().__init__()
        self.nodeView = nodeView
        self.nodeWindow = nodeWindow
        self.nodeModel = nodeModel
        self.propertyAreas =[]
        self.mainLayout = QVBoxLayout()
        self.splitter= QSplitter(Qt.Vertical)
        self.splitter.setObjectName("nodeSplitter")
        # 閉じれないようにする
        self.splitter.setChildrenCollapsible(False)

        # s  = (Styles.className("nodeSplitter"))
        s  = (Styles.qClass("nodeSplitter","QSplitter","nodeWidget.scss"))

        self.splitter.setStyleSheet(s)
        # 全て折りたたみ不可能にする

        self.mainLayout.setContentsMargins(0,0,0,0)
        self.mainLayout.addWidget(self.splitter)
        # bw = AddPropArea(nodeModel)
        # self.mainLayout.addWidget(bw)
        self.setStyleSheet(Styles.className("nodeWidget","nodeWidget.scss"))
        self.setLayout(self.mainLayout)

    # nodeModelの状態をviewに同期させる
    # model-to-viewへのデータを受け渡すクラスが欲しい 
    def initProperties(self,nodeData:NodeViewData):
        for propertyArea in self.propertyAreas:
            propertyArea : NodePropertyArea
            propertyArea.initProperties(nodeData)
        # self.updateView()
        return

    def updateView(self):
        for propertyArea in self.propertyAreas:
            propertyArea : NodePropertyArea
            propertyArea.updateView()
        return

    def onInput(self, **kwards):
        propName:str = kwards["propName"]
        for propertyArea in self.propertyAreas:
            propertyArea : NodePropertyArea
            if propertyArea.propertyName == propName:
               propertyArea.onInput(**kwards)
        return

    def onFinished(self ,data:str , propName:str):
        for propertyArea in self.propertyAreas:
            propertyArea : NodePropertyArea
            if propertyArea.propertyName == propName:
               propertyArea.onFinished(data,propName)
        return

    def onResize(self, width , height):
        self.setFixedHeight(height)
        self.setFixedWidth(width)

    def addSlot(self, label , typeSet = defaultFieldTypeSet):
        area = NodePropertyArea(self,self.nodeModel,label,typeSet)
        self.propertyAreas.append(area)
        self.splitter.addWidget(area)
        return area