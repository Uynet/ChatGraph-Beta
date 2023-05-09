from PyQt5.QtCore import QRectF, Qt , QPointF
from PyQt5.QtGui import QColor, QPen 
from PyQt5.QtWidgets import (QGraphicsEllipseItem, QGraphicsItem,
                             QGraphicsTextItem)

from editors.models.edgeModel import EdgeModel
from utils.enums import InOutType

# 当たり判定はデカ目にしておく
innerR = 10

transparentColor = QColor(255, 255, 255, 00)
hoverColor = QColor(255, 255, 255 , 30)
disabledColor = QColor(255, 255, 255,100)
color1 = QColor("#cccccc")
# bgcolor
dirConnectedColorInput = QColor("#191721")
color2= QColor("#191721")
runningColor = QColor("#3333ff")
dekaR = 30
edgeColor =  QColor(255, 255, 255, 150)


# 当たり判定デカくする用
class SocketBody(QGraphicsEllipseItem):
    def __init__(self, parent):
        super().__init__(QRectF( - dekaR/2, - dekaR/2, dekaR, dekaR))
        self.setParentItem(parent)
        self.parent = parent
        self.setPen(transparentColor)
        self.setBrush(transparentColor)
        self.setZValue(1)
        self.setAcceptHoverEvents(True)

class SocketView(QGraphicsEllipseItem ):
    def __init__(self,model, nodeModel, ioType ):
        super().__init__(QRectF( - innerR/2, - innerR/2, innerR, innerR))
        from editors.models.nodes.nodeModel import NodeModel
        self.name:str = "" 
        self.nameLabel = None
        self.parentNodeModel = nodeModel
        self.inOutType  = ioType
        self.setZValue(2)
        self.model = model
        self.penWidth = 2
        self.edgeColor = edgeColor 
        node:NodeModel = model.parentNodeModel
        self.setParentItem(node.nodeView.nodeWindow)
        self.setFlag(QGraphicsItem.ItemSendsScenePositionChanges, True)
        self.body = SocketBody(self)
        self.genSocketView()

        pen = QPen(edgeColor, self.penWidth, Qt.DashLine)
        self.setPen(pen)
        self.setColor(color2)

    def getModel(self):
        return self.model
    def onHover(self ,pos):
        self.body.setBrush(hoverColor)
    def onLeave(self,pos):
        self.body.setBrush(transparentColor)

    def getScenePos(self) ->QPointF:
        return self.scenePos()

    # 表示上の名前
    def genSocketView(self):
        self.nameLabel = QGraphicsTextItem(self.getName(), self)
        isRight = self.inOutType == InOutType.IN 
        dx = -1 if isRight else 1
        self.nameLabel.setPos( (20 * dx)-10, - 5)
        self.nameLabel.setDefaultTextColor(Qt.white)
         
    def setNameText(self, text):
        self.nameLabel.setPlainText(text)

    def setName(self, name):
        self.name = name
        self.setNameText(name)
        
    def getName(self):
        if self.name == None:
            return ""
        return self.name


    def itemChange(self, change, value):
        if change == QGraphicsItem.ItemScenePositionHasChanged:
            self.model.onItemChange()
        return super().itemChange(change, value)

    def setColor(self, color):
        c = color
        self.color = c
        self.setBrush(c)

    def removeChain(self):
        pass
        # print("not imp! removeChain")

    def onOutput(self,inputText ):
        pass
        # print("not imp! onOutput")

    def onInput(self,inputText ):
        pass
        # print("not imp! onInput")
    # 右
    def onFinished(self):
        pass
        # print("not imp! onFinished")
    # 左
    def onFinishedOutput(self):
        pass
        # print("not imp! onFinishedOutput")

    def onConnect(self):
        pen = QPen(edgeColor, self.penWidth, Qt.SolidLine)
        self.setPen(pen)
        self.setColor(color1)
        pass

    def onDisConnect(self):
        pass
        # print("not imp!")
        pen = QPen(edgeColor, self.penWidth, Qt.DashLine)
        self.setPen(pen)
        self.setColor(color2)

    def getEdgeVector(self) -> QPointF:
        # edgeがあれば、edgeの単位ベクトルを返す
        edge:EdgeModel = self.getModel().edge
        if edge == None:
            return QPointF(0,0)
        osoc = edge.getOppositeSocket(self) 
        osocView = osoc.view
        p1:QPointF =  self.scenePos()
        p2:QPointF = osocView.scenePos() 
        v:QPointF = QPointF(p2.x() - p1.x(), p2.y() - p1.y()) 
        vLen = (v.x()**2 + v.y()**2)**0.5 
        v = v / vLen
        if(vLen == 0):
            return QPointF(0,0)
        return v 
