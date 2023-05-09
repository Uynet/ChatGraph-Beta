from PyQt5.QtWidgets import QScrollArea, QVBoxLayout, QWidget

from layout.views.insp.inspectingItemWidget import InspectingItemWidget
from utils.styles import Styles


class InspectorView(QWidget):
    def __init__(self , mainWindow):
        super().__init__()
        self.mainWindow = mainWindow
        self.init_ui()

    def init_ui(self):
        # Create layout and widgets
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        self.inspectingItemWidget = InspectingItemWidget(self.mainWindow)
        # text 
        layout.addWidget(self.inspectingItemWidget)
    
        # Create a QWidget to set the layout
        self.container = QWidget(self)
        self.container.setLayout(layout)
        self.container.setStyleSheet(Styles.className("inspectorContainer","inspector.scss"))
        # Create a QScrollArea and set the widget
        self.scroll = QScrollArea(self)
        self.scroll.setWidget(self.container)
        self.scroll.setWidgetResizable(True)
        s = Styles.qClass("chatScrollArea","QScrollBar","chat.scss")
        self.scroll.setStyleSheet(s)

        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(self.scroll)

        self.setLayout(self.main_layout)
        self.setStyleSheet(Styles.className("inspectorWindow","inspector.scss"))

    def setItem(self ,nodeModel ):
        self.inspectingItemWidget.setItem(nodeModel)
        return
    def getItem(self):
        return self.inspectingItemWidget.getItem()

    def update(self):
        self.inspectingItemWidget.update()

    def updateByData(self , nodeModel , name , value):
        self.inspectingItemWidget.updateByData(nodeModel , name , value)