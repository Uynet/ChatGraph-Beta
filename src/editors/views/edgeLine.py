from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from editors.shaderProps import ShaderProps
from editors.views.shaderRect import ShaderRect


class EdgeViewProps(ShaderProps):
    def __init__(self):
        self.startPos = None
        self.endPos = None

class EdgeLine(ShaderRect):
    def __init__(self, model , viewPortRect):
        vertShaderPath = "resources/images/shaders/edge.vert"
        fragShaderPath = "resources/images/shaders/edge.frag"
        # view props
        self.sp = viewPortRect.startPos
        self.ep = viewPortRect.endPos
        props = ShaderProps(
            startPos = self.sp,
            endPos = self.ep
        )
        super().__init__(model , props, vertShaderPath, fragShaderPath)
        # sp,epを結ぶ太さwの線を描画する

    def onResize(self,sp,ep):
        self.sp = sp
        self.ep = ep
        # dir = ep - sp
        # Qreftf
        # from PyQt5.QtCore import QPoint
        # dir = QPoint(ep.x() - sp.x() , ep.y() - sp.y())

        # sign = 1
        # if dir.x() * dir.y() < 0:
        #     sign = -1

        self.props.set(startPos = sp)
        self.props.set(endPos = ep)