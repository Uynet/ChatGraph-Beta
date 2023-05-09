from PyQt5.QtWidgets import QTextEdit

from layout.TextEditorView import PythonHighlighter
from utils.styles import Styles


class InspectorProperty(QTextEdit):
    def __init__(self,key,value:str , node):
        super().__init__()
        self.highlighter = PythonHighlighter(self.document())
        self.textChanged.connect(self.adjust_size)
        self.textChanged.connect(self.changeNodeProperty)
        s = Styles.className("inspectorProperty","inspector.scss")

        text = value
        self.node = node
        self.key= key
        self.setTabStopWidth(80)
        self.setTabStopDistance(40)
        self.setPlainText(text)
        self.setStyleSheet(s)
        self.setReadOnly(False)

    def showEvent(self, event):
        # ウィジェットが表示される直前にadjust_sizeを呼び出す
        self.adjust_size()
        super().showEvent(event)
    
    # 外部から値を変更されたとき
    def onChangeProperty(self , value):
        # ブロックする 
        self.textChanged.disconnect(self.changeNodeProperty)
        self.setPlainText(str(value))
        # ブロック解除
        self.textChanged.connect(self.changeNodeProperty)
        return

    def changeNodeProperty(self):
        value = self.toPlainText()
        self.node.onChangeProperty(self.key,value , isUpdateView=True , isUpdateInspector=False)
        return

    def adjust_size(self):
        document_height = self.document().size().height()
        pad = 30
        self.setFixedHeight(document_height + pad)