from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from editors.views.nodeWindows.nodeWindow import NodeWindow
    from editors.controllers.nodeGraphController import NodeGraphController
    from editors.models.nodes.nodeModel import NodeModel
from enum import Enum

from PyQt5.QtCore import QRectF, Qt
from PyQt5.QtWidgets import QGraphicsItem
from editors.controllers.cgpController import CgpController

from editors.controllers.mainWindowController import MainWindowController


# ウィンドウの端を掴んだりする操作の状態
# valueはマウスカーソルの形状に対応する
class WindowControllerState(Enum):
    NONE = Qt.ArrowCursor 
    DRAG = Qt.ClosedHandCursor 
    RESIZE_X = Qt.SizeHorCursor
    RESIZE_Y = Qt.SizeVerCursor
    RESIZE_XY = Qt.SizeFDiagCursor 

class NodeWindowController(CgpController):
    def __init__(self , nodeWindow:NodeWindow):
       super().__init__()
       self.nodeWindow = nodeWindow
       self.nodeModel = nodeWindow.getModel() 
       self.dragState = WindowControllerState.NONE

    # ウィンドウの左右の端を掴んでいる状態
    def isResizableWidth(self,pos):
        col = 30 # 当たり判定のふとさ
        path = self.nodeWindow.path
        rect:QRectF = path.boundingRect()
        x = rect.right()
        dist1 = abs(pos - x)
        left = 0
        dist2 = abs(pos - left)
        return dist1 < col #or dist2 < col

    # ウィンドウの上下の端を掴んでいる状態
    def isResizableHeight(self,pos):
        col = 30 # 当たり判定のふとさ
        path = self.nodeWindow.path
        rect:QRectF = path.boundingRect()
        y= rect.height()
        dist = abs(pos - y)
        return dist < col

    def resetPos(self):
        pos = self.nodeWindow.pos()
        nodeModel:NodeModel = self.getModel()
        nodeModel.onChangeProperty("positionX" , str(pos.x()) , isUpdateView=False , isUpdateInspector=True)
        nodeModel.onChangeProperty("positionY" , str(pos.y()) , isUpdateView=False, isUpdateInspector=True)

    def onHover(self, event):
        scenePos = event.scenePos()
        pos = self.nodeWindow.mapFromScene(scenePos)
        # get bounding rect
        isResizableWidth = self.isResizableWidth(pos.x()) 
        isResizableHeight = self.isResizableHeight(pos.y())
        isResizable = isResizableWidth or isResizableHeight
        if isResizable:
            # 上下にリサイズ可能な状態
            if isResizableHeight:
                self.setCursor(WindowControllerState.RESIZE_Y.value)
            # 左右にリサイズ可能な状態
            if isResizableWidth:
                self.setCursor(WindowControllerState.RESIZE_X.value)
            if isResizableWidth and isResizableHeight:
                # 左右上下にリサイズ可能な状態
                self.setCursor(WindowControllerState.RESIZE_XY.value)
        else:
            self.setCursor(WindowControllerState.NONE.value)

    def onLeave(self):
        self.setCursor(WindowControllerState.NONE.value)

    def mouseReleaseEvent(self,ngc:NodeGraphController,scene, event):
        self.resetPos()
        MainWindowController.getInstance().setInspectorItem(self.nodeModel)
        self.dragState = WindowControllerState.NONE
        ngc.resetFocus()

    def mousePressEvent(self, ngc:NodeGraphController,scene,event):
        self.resetPos()
        nodeModel = self.nodeModel
        MainWindowController.getInstance().setInspectorItem(nodeModel)
        cursorShape = self.nodeWindow.cursor().shape()
        self.dragState = WindowControllerState(cursorShape) 
        # リサイズ中の時はウィンドウが動かないようにする
        if self.dragState in { WindowControllerState.RESIZE_X , WindowControllerState.RESIZE_Y , WindowControllerState.RESIZE_XY }:
            self.setFlag(QGraphicsItem.ItemIsMovable , False)
        else :
            window :NodeWindow = self.nodeWindow

            # 選択中にクリックしたら何もしない
            if window.isSelectByNgc: 
                return
                # ngc.selectNodes([])
            else : self.setFlag(QGraphicsItem.ItemIsMovable , True)
            ngc.selectItems([self.nodeWindow])
        self.update()


    def mouseMoveEvent(self, ngc:NodeGraphController,scene,event):
        self.resetPos()
        minWidth = 80
        propLen = self.nodeWindow.nodeWidget.propertyAreas.__len__()
        scenePos = event.scenePos()
        pos = self.nodeWindow.mapFromScene(scenePos)
        FlameHiehgt = 30
        minHeight = 45 * propLen + FlameHiehgt
        nodeModel:NodeModel = self.nodeModel
        if self.dragState in { WindowControllerState.RESIZE_X ,  WindowControllerState.RESIZE_XY }:
            width = max(pos.x() , minWidth)
            width = int(width) 
            nodeModel.onChangeProperty("width" , width , isUpdateView=False , isUpdateInspector=True)

        if self.dragState in { WindowControllerState.RESIZE_Y ,  WindowControllerState.RESIZE_XY }:
            height = max(pos.y(),minHeight)
            nodeModel.onChangeProperty("height" , height , isUpdateView=False , isUpdateInspector=True)
        self.update()


    def getModel(self):
        return self.nodeModel
    
    def setCursor(self, cursorShape):
        self.nodeWindow.setCursor(cursorShape)
    def setFlag(self,*args):
        self.nodeWindow.setFlag(*args)  
    def update(self):
        self.nodeWindow.update()