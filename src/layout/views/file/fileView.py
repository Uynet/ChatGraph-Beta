from PyQt5.QtWidgets import QScrollArea, QVBoxLayout, QWidget

from editors.views.nodeWindows.nodeWindow import NodeWindow
from layout.insp.inspectingItemWidget import InspectingItemWidget
from layout.views.file.fileBrowser import FileBrowserWidget
from utils.styles import Styles
from utils.util import Util


class FileView(QWidget):
    def __init__(self , mainWindow):
        super().__init__()
        self.mainWindow = mainWindow
        self.init_ui()

    def init_ui(self):
        filepath = "./resources/nodes" 
    
        # Create a QWidget to set the layout
        self.container = FileBrowserWidget(filepath)
        self.container.setStyleSheet(Styles.className("inspectorContainer"))
        # Create a QScrollArea and set the widget
        self.scroll = QScrollArea(self)
        self.scroll.setWidget(self.container)
        self.scroll.setWidgetResizable(True)
        s = Styles.qClass("inspectorScrollArea","QScrollBar")
        self.scroll.setStyleSheet(s)

        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(self.scroll)

        self.setLayout(self.main_layout)
        self.setStyleSheet(Styles.className("inspectorWindow"))

    def update(self):
        pass

    def updateByData(self , nodeModel , name , value):
        pass