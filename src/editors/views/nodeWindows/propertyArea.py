from __future__ import annotations

# QPoint
from PyQt5.QtCore import QPoint, Qt
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QWidget

from editors.models import socketModel
from editors.types.dataType import NodeViewData
from layout.components.buttonWidget import ButtonWidget
from layout.nodeLabel import OpenToggleButton, PropertyLabel
from layout.nodeTextField import NodeTextField
from utils.enums import InOutType, PropertyType
from utils.styles import Styles
from utils.util import Util

defaultFieldTypeSet = {
     PropertyType.CHAT,
     None
}
class NodePropertyArea(QWidget):
    def __init__(self, parent ,nodeModel, propertyName ,fieldTypeSet = defaultFieldTypeSet):
        super().__init__()
        from editors.models.nodes.nodeModel import NodeModel
        self.lastHeight = 0
        self.windowWidth = 0
        self.windowHeight = 0
        # labelと同じ名前のプロパティを取得
        # memo:  input / outputはプロパティから取得する必要はない。
        # 設定できる欄、できない欄でデザインを分ける必要がある。
        self.nodeModel : NodeModel  = nodeModel
        self.nodeWidget = parent
        self.nodeModel = nodeModel
        text = self.nodeModel.getProperty(propertyName)
        # textが配列の場合strに変換
        if type(text) == list:
            text = str(text)
        if text is None:
            text = ""
        self.propertyName = propertyName
        self.propertyLabel = PropertyLabel(nodeModel , propertyName)
        self.toggleButton = OpenToggleButton(self)
        self.toggleButton.show() 

        buttonAndLabel = QHBoxLayout()
        buttonAndLabel.addWidget(self.toggleButton)
        buttonAndLabel.addWidget(self.propertyLabel)



        field = NodeTextField(nodeModel ,self, fieldTypeSet)
        Layout = QVBoxLayout()
        Layout.addLayout(buttonAndLabel)
        Layout.addWidget(field)

        # inputなら再生成、outなら送信ボタンを表示
        isInput = InOutType.IN in fieldTypeSet
        if isInput:
            pass
        else:
            # 右に寄せる
            sendButton = ButtonWidget()
            buttonAndLabel.addWidget(sendButton)
            sendButton.clicked.connect(self.onSendButtonClicked)


        self.field = field
        self.fieldTypeSet = fieldTypeSet
        self.propertyLabel:NodeModel= self.propertyLabel
        self.setStyleSheet(Styles.className("nodePropertyArea","nodeWidget.scss"))
        # 下の端に区切り線
        self.setContentsMargins(0,0,0,0)
        # 要素を上揃えにする
        Layout.setAlignment(Qt.AlignTop)
        Layout.setSpacing(0)

         
        self.setLayout(Layout)

    def onUserInput(self ,value:str):
        from editors.models.nodes.nodeModel import NodeModel 
        nodeModel : NodeModel= self.nodeModel
        name :str = self.propertyName
        nodeModel.onChangeProperty(name,value  , isUpdateView = False , isUpdateInspector=True)
    def onInnerTextChanged(self , value:str):
        from editors.models.nodes.nodeModel import NodeModel 
        nodeModel : NodeModel= self.nodeModel
        name :str = self.propertyName
        nodeModel.onChangeProperty(name,value  , isUpdateView = False , isUpdateInspector=False)


    def isSameTypeSocket(self , socket:socketModel):
        return socket.propName == self.propertyName

    # onchange size
    def resizeEvent(self, event):
        self.updateView()
        return super().resizeEvent(event)

    # ソケット接続位置の原点をいい感じにする
    def getOriginPos(self):
        windowFlameHeight = 30 #ウインドウのフレーム幅 
        nodeLabelHiehgt = 18 #ノードラベルの高さ
        oy = windowFlameHeight + nodeLabelHiehgt
        return QPoint(0,oy) 

    def alignSocket(self , socket , index):
        origin = self.getOriginPos()
        pos = self.mapTo(self.nodeWidget,origin) 
        w = self.windowWidth 
        height = self.height()
        y = pos.y() 
        # sideFlag = socket.sideFlag
        sideFlag = True 
        of = 0
        if( ( socket.inOutType== InOutType.IN)  == sideFlag):
            x = -of 
        else :
            x = w + of
        margin = Util.getGoodMergin(10 , 80 ,height)
        # margin = 10
        k = index
        y += k * margin 
        socket.view.setPos(x , y)
        # return

    def alignSockets(self , allSockets):
        sameSockets = filter(self.isSameTypeSocket , allSockets)
        k = 0
        for socket in sameSockets:
            self.alignSocket(socket, k)
            k+=1 

    def updateView(self):
        self.field.updateView()
        propertyLabel : PropertyLabel = self.propertyLabel
        propertyLabel.updateView()
        self.windowWidth= self.nodeModel.getProperty("width")
        sockets = self.nodeModel.getAllSockets()
        self.alignSockets(sockets)

    def onInput(self,**kwards):
        field : NodeTextField = self.field
        field.onInput(**kwards)
        propertyLabel : PropertyLabel = self.propertyLabel
        propertyLabel.onInput(**kwards)
        return

    def onFinished(self,data:str , propName:str):
        field : NodeTextField = self.field
        field.onFinished( data, propName)
        propertyLabel : PropertyLabel = self.propertyLabel
        propertyLabel.onFinished(data, propName)
        return

    def showEvent(self, event): 
        self.updateView()
        return super().showEvent(event)

    def initProperties(self,nodeData:NodeViewData):
        self.windowWidth= nodeData.get("width")
        field : NodeTextField = self.field
        field.initProperties(nodeData)
        if self.propertyName == "inputed":
            self.closeField()
        return

    def closeField(self):
        # height to 30
        height = self.field.height()
        self.lastHeight = height 
        nodeModel = self.nodeModel
        h = nodeModel.getProperty("height")
        nodeModel.setProperty("height" , h - height)

        areaHeight = 35
        self.setFixedHeight(areaHeight)
        self.field.close()
        self.toggleButton.setTo(1)
        self.updateView()

    def showField(self):
        field = self.field
        field.setFixedHeight(self.lastHeight)
        nodeModel = self.nodeModel
        h = nodeModel.getProperty("height")
        nodeModel.setProperty("height" , h + self.lastHeight)
        field.show()
        self.setMinimumHeight(0)
        self.setMaximumHeight(16777215)
        self.toggleButton.setTo(0)
        self.updateView()

    def toggle(self):
        if self.field.isVisible():
            self.closeField()
        else:
            self.showField()

    def onSendButtonClicked(self):
        # ????
        self.field.returnPressed()

    def onClick(self,nodeLabel):
        self.toggle()
   