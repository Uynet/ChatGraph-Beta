
from PyQt5.QtCore import QRectF
from PyQt5.QtGui import QBrush, QColor, QPainterPath, QPen
from PyQt5.QtWidgets import QGraphicsItem, QGraphicsPathItem

from editors.controllers.hubController import HubController
from editors.models.socketModel import SocketModel
from editors.views.nodeWindows.socketView import SocketView
from editors.types.dataType import NodeProperty
from utils.enums import InOutType
from utils.styles import Styles


class HubWindow(QGraphicsPathItem):
    def __init__(self, nodeView , nodeModel):
        self.nodeModel = nodeModel 
        self.nodeWidget = None
        self.controller = HubController(self)
        self.properties = []

        self.path = QPainterPath()
        w = h = 60
        self.path.addRoundedRect(QRectF(0, 0, w, h), w/2, h/2)
        # path2 = QRectF(w/4,h/4, w/2, h/2)
        # self.path.addRoundedRect(path2 , w/4, h/4)
        super().__init__(self.path)
        self.setPos(0,0)
        self.nodeView = nodeView

        self.setFlag(QGraphicsItem.ItemSendsScenePositionChanges, True)
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)
        self.setZValue(-4)

        # transparent
        self.setBrush(QBrush(QColor(0,0,0,0)))
        self.setColor("nodeWait" , 2)

    def getModel(self):
        return self.nodeModel

    def onDeselect(self):
        self.isSelectByNgc = False
        self.setSelected(False)
        self.setFlag(QGraphicsItem.ItemIsMovable , False)
        self.setColor("nodeWait" , 2)

    def onSelect(self):
        self.isSelectByNgc = True 
        self.setSelected(True)
        self.setFlag(QGraphicsItem.ItemIsMovable , True)
        self.setColor("nodeSelected" , 4)

    def setColor(self,colorName , width):
        color = Styles.getQColor(colorName) 
        pen = QPen(color, width)
        self.setPen(pen)

    def update(self):
        self.updateView()
        super().update()

    def updateView(self): 
        nodeData = self.nodeModel.nodeData
        self.setPos(nodeData.positionX,nodeData.positionY)
        sockets = self.nodeModel.getAllSockets()
        self.alignSockets(sockets)

    def initProperties(self , nodeData:NodeProperty):
        self.setPos(nodeData.positionX,nodeData.positionY)

    def onHover(self,event):
        self.controller.onHover(event)
        c = QColor(255,255,255,30)
        self.setBrush(c)

    def onLeave(self,event):
        self.controller.onLeave()
        self.setBrush(QBrush(QColor(0,0,0,0)))

    def alignSockets(self , sockets:list[SocketModel]):
        w = self.nodeModel.getProperty("width")
        h = self.nodeModel.getProperty("height")
        o = 10
        ox = w/2 + o
        oy = h/2 + o 


        for soc in sockets:
            sv:SocketView = soc.view
            if soc.inOutType == InOutType.OUT: r = 40 
            else : r = 20
            vector = sv.getEdgeVector()
            dx = vector.x() * r
            dy = vector.y() * r
            x = ox + dx 
            y = oy + dy 
            sv.setPos(x,y)
            # i += 1

    def onFinished(self,data,propName):
        pass

    def onInput(self,**kwargs):
        pass

    def resetSize(self):
        pass

    def addSlot(self, label , typeSet = None):
        pass

    def onSetState(self, state):
        pass

    def getCgpView(self):
        return self

    def paint(self, painter, option, widget):
        # 選択時の点線を描画しないように設定
        from PyQt5.QtWidgets import QStyle
        option.state &= ~QStyle.State_Selected 
        super().paint(painter, option, widget)