from PyQt5.QtWidgets import QTabWidget

from layout.chatWindow import ChatView
from layout.graphView import GraphView
from layout.settingView import SettingView
from layout.TextEditorView import TextEditorView
from layout.views.insp.inspectorView import InspectorView
from utils.styles import Styles


class Panel(QTabWidget):
    def __init__(self , mainwindow ,nodeScene):
        self.nodeScene = nodeScene
        super().__init__()
        pass

    def addTab(self , widget , name):
        super().addTab(widget , name)

    def setStyle(self):
        tabStyle= Styles.qClass("panelTab","QTabBar")
        self.tabBar().setStyleSheet(tabStyle)

        panelStyle = Styles.qClass("panelArea","QTabWidget")
        self.setStyleSheet(panelStyle)


class LeftPanel(Panel):
    def __init__(self , mainWindow ,nodeScene):
        super().__init__( mainWindow ,nodeScene) 
        self.inspectorView = InspectorView(mainWindow)
        self.addTab(self.inspectorView, "inspector")

        # self.FileView = FileView(self.nodeScene)
        # self.addTab(self.FileView, "browser")
        self.TextEditorView = TextEditorView(self.nodeScene)
        self.addTab(self.TextEditorView, "memo")
        self.setCurrentIndex(0)
        self.setStyle()

# mainwindow は nodesceneを持つべきではないが、後で考えよう
class EditorPanel(Panel):
    def __init__(self , mainWindow,nodeScene):
        super().__init__(mainWindow ,nodeScene) 
        self.graphView = GraphView(nodeScene)
        self.settingView = SettingView(mainWindow)
        self.addTab(self.graphView, "default")
        self.addTab(self.settingView, "API Key")
        self.setCurrentIndex(0)
        self.setStyle()

class RightPanel(Panel):
    def __init__(self , mainWindow ,nodeScene):
        super().__init__(mainWindow ,nodeScene) 
        self.chatView = ChatView(self.nodeScene)
        self.addTab(self.chatView, "chat log")
        self.setStyle()

