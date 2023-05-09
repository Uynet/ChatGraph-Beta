import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from PyQt5.QtGui import QOpenGLShader, QOpenGLShaderProgram
from PyQt5.QtWidgets import QOpenGLWidget

from editors.shaderProps import ShaderProps
from utils.fileLoader import FileLoader


class ShaderRect(QOpenGLWidget):
    def __init__(self, model , props:ShaderProps, vertShaderPath, fragShaderPath):
        self.model = model
        self.vertShaderPath = vertShaderPath
        self.fragShaderPath = fragShaderPath
        self.shaderProgram = None
        self.time = 0.0
        self.props = props

        x = -1.0
        y = -1.0 
        w = 2.0
        h = 2.0
        self.vertices = ShaderRect.genRect(x,y,w,h) 
        # sp = (-1.0, -1.0, 0.0)
        # ep = (1.0, 1.0, 0.0)
        # width = 0.1
        # self.vertices = ShaderRect.genLine(ep,sp,width)
        super().__init__()

    def setVertices(self, vertices):
        self.vertices = vertices

    def initializeGL(self):
        self.time = 0.0
        vertShaderPath = self.vertShaderPath
        fragShaderPath = self.fragShaderPath 
        vertSource = FileLoader.read(vertShaderPath)
        fragSource = FileLoader.read(fragShaderPath)
        self.shaderProgram =  QOpenGLShaderProgram()
        self.shaderProgram.addShaderFromSourceCode(QOpenGLShader.Vertex, vertSource)
        self.shaderProgram.addShaderFromSourceCode(QOpenGLShader.Fragment, fragSource)
        self.shaderProgram.link()
        self.shaderProgram.bind()
        # glClear(GL_COLOR_BUFFER_BIT)
        glDisable(GL_DEPTH_TEST)
        glEnable(GL_BLEND)
        glClearColor(0.094, 0.090, 0.106 ,1.0)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    @staticmethod
    def genRect(x, y, width, height):
        p1 = (x, y, 0.0)
        p2 = (x + width, y, 0.0)
        p3 = (x + width, y + height, 0.0)
        p4 = (x, y + height, 0.0)
        vertices = [
            p1[0], p1[1], p1[2],  # 0
            p2[0], p2[1], p2[2],  # 1
            p3[0], p3[1], p3[2],  # 2
            p3[0], p3[1], p3[2],  # 2
            p4[0], p4[1], p4[2],  # 3
            p1[0], p1[1], p1[2],  # 0
        ]
        return vertices 

    def genLine(sp,ep,width):
        dx = ep[0] - sp[0]
        dy = ep[1] - sp[1]
        length = np.sqrt(dx * dx + dy * dy)
        unit_dx = dx / length
        unit_dy = dy / length

        half_width = width / 2
        perp_dx = -unit_dy * half_width
        perp_dy = unit_dx * half_width

        p1 = (sp[0] + perp_dx, sp[1] + perp_dy, 0.0)
        p2 = (sp[0] - perp_dx, sp[1] - perp_dy, 0.0)
        p3 = (ep[0] + perp_dx, ep[1] + perp_dy, 0.0)
        p4 = (ep[0] - perp_dx, ep[1] - perp_dy, 0.0)

        vertices = [
            p1[0], p1[1], p1[2],  # 0
            p2[0], p2[1], p2[2],  # 1
            p3[0], p3[1], p3[2],  # 2
            p3[0], p3[1], p3[2],  # 2
            p2[0], p2[1], p2[2],  # 1
            p4[0], p4[1], p4[2],  # 3
        ]
        return vertices

    def paintGL(self):
        self.time += 0.01
        self.shaderProgram.bind()
        self.shaderProgram.setUniformValue("time", self.time)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        vertices = self.vertices 

        glBegin(GL_TRIANGLES)
        for i in range(0, len(vertices), 3):
            glVertex3f(vertices[i], vertices[i+1], vertices[i+2])
        glEnd()


    def resizeGL(self, w, h):
        glViewport(0, 0, w, h)