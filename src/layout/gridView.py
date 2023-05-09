import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from PyQt5.QtCore import QPointF, QRect, QRectF, Qt, QTimer, QVariantAnimation
from PyQt5.QtGui import (QBrush, QColor, QPainter, QPainterPath,
                         QPainterPathStroker, QPen)
from PyQt5.QtWidgets import (QApplication, QGraphicsItem, QGraphicsPathItem,
                             QGraphicsProxyWidget, QGraphicsRectItem, QWidget)

from editors.views.edgeLine import EdgeLine
from editors.views.shaderRect import ShaderRect
from utils.styles import Styles


class GridItem(QGraphicsRectItem):
    def __init__(self,graphView):
        self.viewPortRect = graphView.sceneRect()
        rect = QRectF(
            self.viewPortRect.x(),
            self.viewPortRect.y(),
            self.viewPortRect.width(),
            self.viewPortRect.height()
        )
        super(GridItem, self).__init__(-1000,-1000,20,20)
        self.graphView = graphView
        # self.setPos(0,0)
        self.gridView = GridView(self , self.viewPortRect)
        self.proxyWidget = QGraphicsProxyWidget(self)
        self.proxyWidget.setWidget(self.gridView)
        self.proxyWidget.setParentItem(self)
        self.proxyWidget.setGeometry(self.viewPortRect)
        # z-value
        self.setZValue(-10)
    # def onResize():
    # def boundingRect(self):
    #     # rect = QRectF(
    #     #     self.viewPortRect.x(),
    #     #     self.viewPortRect.y(),
    #     #     self.viewPortRect.width(),
    #     #     self.viewPortRect.height()
    #     # )
    #     rect = QRectF(0,0,1200,1200)
    #     return rect

class GridView(ShaderRect):
    def __init__(self, model , viewPortRect):
        vertShaderPath = "resources/images/shaders/grid.vert"
        fragShaderPath = "resources/images/shaders/grid.frag"
        # view props
        # self.sp = viewPortRect.startPos
        # self.ep = viewPortRect.endPos
        # props = ShaderProps(
        #     startPos = self.sp,
        #     endPos = self.ep
        # )
        props = {}
        super().__init__(model , props, vertShaderPath, fragShaderPath)
        # sp,epを結ぶ太さwの線を描画する