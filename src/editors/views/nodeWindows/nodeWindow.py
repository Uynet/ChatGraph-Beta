from PyQt5.QtCore import QRectF
from PyQt5.QtGui import QBrush, QColor, QPainterPath, QPen
from PyQt5.QtWidgets import (QGraphicsItem, QGraphicsPathItem,
                             QGraphicsProxyWidget)

from editors.types.dataType import NodeViewData
from editors.views.nodeIconImage import NodeIconImage
from editors.views.nodeWindows.nodeStatusIcon import NodeStatusIcon
from editors.views.nodeWindows.nodeWidget import NodeWidget
from editors.views.nodeWindows.nodeWindowController import NodeWindowController
from editors.views.nodeWindows.WindowFlameLabel import WindowFlameLabel
from utils.enums import NodeProcessState
from utils.styles import Styles


class NodeWindow(QGraphicsPathItem):
    def __init__(self, nodeView , nodeModel):
        self.nodeModel = nodeModel 
        self.nodeWidget = None
        self.controller = NodeWindowController(self)
        self.properties = []

        self.path = QPainterPath()
        defaultWidth = 200
        defaultHeight = 200
        self.path.addRoundedRect(QRectF(0, 0, defaultWidth, defaultHeight), 5, 5)
        super().__init__(self.path)
        self.setPos(0,0)
        self.nodeView = nodeView
        self.nodeWidget = NodeWidget(self, nodeView, nodeModel)

        self.proxyWidget = QGraphicsProxyWidget(self)
        self.proxyWidget.setWidget(self.nodeWidget)
        self.proxyWidget.setParentItem(self)

        self.nodeLabel = WindowFlameLabel("Node",self.nodeModel,self)
        self.iconImage = NodeIconImage(nodeModel , self)
        self.statusIcon = NodeStatusIcon(nodeModel , self)
        self.statusIcon.hide()

        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges)
        self.setFlag(QGraphicsItem.ItemSendsScenePositionChanges, True)
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)
        self.setAcceptHoverEvents(True)
        self.setZValue(-4)
        self.isSelectByNgc = False

        stateNames = ["nodeWait","nodeRunning","nodeFinished","nodeStopped","nodeError"]
        colorName = stateNames[0]
        colorCode = Styles.getColor(colorName)
        color = QColor(colorCode)
        pen = QPen(color, 1)
        self.setPen(pen)

        if nodeModel.nodeType == "TextInputNode": attribute = "In"
        elif nodeModel.nodeType == "OutputNode": attribute = "Out"
        elif nodeModel.nodeType == "ExecNode": attribute = "Script"
        elif nodeModel.nodeType == "ModuleNode": attribute = "Module"
        elif nodeModel.nodeType == "GPTNode": attribute = "Chat"
        else : attribute = "Default"
        windowName = attribute + "NodeWindow"
        self.windowColor = QColor(Styles.getColor(windowName))
        self.setBrush(QBrush(self.windowColor))
    def getModel(self):
        return self.nodeModel

    def onDeselect(self):
        self.setSelected(False)
        self.isSelectByNgc = False
        colorName = "nodeWait" 
        self.setFlag(QGraphicsItem.ItemIsMovable , False)
        color = QColor(Styles.getColor(colorName))
        pen = QPen(color, 1)
        self.setPen(pen)

    def onSelect(self):
        self.setSelected(True)
        self.isSelectByNgc = True 
        color = Styles.getQColor("nodeSelected") 
        self.setFlag(QGraphicsItem.ItemIsMovable , True)
        pen = QPen(color, 4)
        self.setPen(pen)

    def update(self):
        self.updateView()
        super().update()

    def updateView(self): 
        nodeData = self.nodeModel.nodeData
        self.setPos(nodeData.positionX,nodeData.positionY)
        self.resetSize()
        self.nodeLabel.updateView()
        self.iconImage.updateView()
        self.nodeWidget.updateView()
        self.statusIcon.updateView()

    def onFinished(self,data,propName):
        self.nodeWidget.onFinished(data,propName)

    def onInput(self,**kwargs):
        self.nodeWidget.onInput(**kwargs)

    def initProperties(self , nodeData:NodeViewData):
        self.setPos(nodeData.positionX,nodeData.positionY)
        self.iconImage.initProperties(nodeData)
        self.nodeLabel.initProperties(nodeData)
        self.nodeWidget.initProperties(nodeData)
        self.resetSize()
        return

    def resetPos(self):
        x = self.nodeModel.getProperty("positionX")
        y = self.nodeModel.getProperty("positionY")
        scenePos = self.nodeView.mapToScene(x,y)
        self.setPos(scenePos)

    # initにしか使ってないっぽい
    def resetSize(self):
        self.path = QPainterPath()
        w = self.nodeModel.getProperty("width")
        h = self.nodeModel.getProperty("height")
        if w == None:w = 200
        if h == None:h = 200

        flameHeight = int(Styles.getNodeWindowStyle("flame-height"))
        borderWidth = int(Styles.getNodeWindowStyle("border-width"))
        borderRadius = int(Styles.getNodeWindowStyle("border-radius"))
        self.path.addRoundedRect(QRectF(0, 0,float(w) ,float(h)), borderRadius, borderRadius)
        self.setPath(self.path)
        contentHeight = int(h) - int(flameHeight)
        contentWidth = int(w) - int(borderWidth) 
        self.nodeWidget.onResize(contentWidth,contentHeight)
        self.proxyWidget.setPos(borderWidth/2,flameHeight-borderWidth/2)
        return

    def addSlot(self, label , typeSet = None):
        self.nodeWidget.addSlot(label , typeSet) 

    def onSetState(self, state):
        state : NodeProcessState
        if state == NodeProcessState.RUNNING:
            self.statusIcon.show()
            self.setBrush(Styles.getQColor("nodeRunning"))
        else :
            self.statusIcon.hide()
            self.setBrush(self.windowColor)
    def getController(self):
        return self.controller

    def getCgpView(self):
        return self

    def onHover(self,event):
        self.controller.onHover(event)
    def onLeave(self,event):
        self.controller.onLeave()

    def paint(self, painter, option, widget):
        # 選択時の点線を描画しないように設定
        from PyQt5.QtWidgets import QStyle
        option.state &= ~QStyle.State_Selected 
        super().paint(painter, option, widget)