from PyQt5.QtWidgets import QGraphicsItemGroup
from editors.models.CgpModels import CgpModel

from editors.views.edgeView import EdgeView
from utils.sound import CSound


# ノードを繋いでる線のドラッグ中のやつ
class WipEdge(CgpModel):
    def __init__(self, start_pos, end_pos ,flip):
        super().__init__()
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.view = EdgeView(self, start_pos , end_pos ,flip)
        # self.view.setOpacity(0.5)

    def onMouseMove(self, mousePos):
        self.end_pos = mousePos
        self.onResize()

    def snapTo(self, pos):
        # CSound.play("connect.wav")
        self.end_pos = pos 
        self.onResize()

    def onResize(self):
        sp = self.start_pos
        ep = self.end_pos
        self.view.onResize(sp,ep)

    def addToScene(self,scene):
        scene.addItem(self.view)

    def removeFromScene(self,scene):
        scene.removeItem(self.view)

    def onRelease(self,scene):
        self.removeFromScene(scene)