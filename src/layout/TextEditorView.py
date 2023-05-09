

from PyQt5.QtWidgets import QScrollArea, QTextEdit, QVBoxLayout, QWidget

from layout.components.pythonHilighter import PythonHighlighter
from utils.styles import Styles

green = "#899965"
pink = "#ad5e82"
blue = "#35a18f"
string = "#7d485e"
comment_color = "#555555"


class TextEditorField(QTextEdit):
    def __init__(self):
        super().__init__()
        self.setStyleSheet(Styles.className("textEditor" , "textEditor.scss"))
        self.setAcceptRichText(False)
        self.highlighter = PythonHighlighter(self.document())

class TextEditorView(QWidget):
    def __init__(self , mainWindow):
        super().__init__()
        self.mainWindow = mainWindow
        self.init_ui()

    def init_ui(self):
        # Create layout and widgets
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.contentWidget = TextEditorField() 
        # text 
        layout.addWidget(self.contentWidget)
    
        # Create a QWidget to set the layout
        self.container = QWidget(self)
        self.container.setLayout(layout)
        self.container.setStyleSheet(Styles.className("inspectorContainer"))
        # Create a QScrollArea and set the widget
        self.scroll = QScrollArea(self)
        self.scroll.setWidget(self.container)
        self.scroll.setWidgetResizable(True)
        s = Styles.qClass("chatScrollArea","QScrollBar","chat.scss")
        self.scroll.setStyleSheet(s)

        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(self.scroll)

        self.setLayout(self.main_layout)
        self.setStyleSheet(Styles.className("inspectorWindow"))

    def setItem(self ,nodeModel ):
        self.contentWidget.setItem(nodeModel)
        return
    def getItem(self):
        return self.contentWidget.getItem()

    def update(self):
        self.contentWidget.update()

    def updateByData(self , nodeModel , name , value):
        self.contentWidget.updateByData(nodeModel , name , value)