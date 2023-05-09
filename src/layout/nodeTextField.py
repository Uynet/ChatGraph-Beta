from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTextEdit

from editors.types.dataType import NodeViewData
from utils.enums import InOutType
from utils.styles import Styles


class NodeTextField(QTextEdit):
    def __init__(self, nodeModel,area,typeSet):
        super().__init__()
        from editors.models.nodes.nodeModel import NodeModel
        from editors.views.nodeWindows.propertyArea import NodePropertyArea
        from layout.TextEditorView import PythonHighlighter
        self.highlighter = PythonHighlighter(self.document())
        self.area:NodePropertyArea = area
        self.setStyleSheet(Styles.className("nodeTextFieldOutput","nodeWidget.scss"))
        # self.setStyleSheet(Styles.qClass("nodeTextFieldOutput","QScrollBar","nodeWidget.scss"))
        self.nodeModel: NodeModel = nodeModel
        self.setMinimumHeight(1)
        self.typeSet = typeSet
        self.textChanged.connect(self.onUserInput)
        # スクロールバーを非表示にする
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setAcceptRichText(False)

    # def focusOutEvent(self, event):
    #     self.clearFocus()
    #     self.textCursor().clearSelection()
    #     super().focusOutEvent(event)

    def returnPressed(self):
        from editors.models.nodes.nodeModel import NodeModel
        nodeModel:NodeModel = self.nodeModel
        # 入力フィールド上でEnterキーを押したときの処理
        if InOutType.IN in self.typeSet: 
            pass
            # nodeModel.onInput( data=self.toPlainText() , propName=self.area.propertyName)
        if InOutType.OUT in self.typeSet: 
            nodeModel.onFinished( data=self.toPlainText() , propName=self.area.propertyName)

    def onUserInput(self):
        value : str = self.toPlainText() 
        self.area.onUserInput(value)
    # 内部からの値の変更
    def onInnerTextChanged(self,value):
        self.textChanged.disconnect(self.onUserInput)
        self.setPlainText(value)
        self.area.onInnerTextChanged(value)
        self.textChanged.connect(self.onUserInput)
        pass

    def initProperties(self, nodeData:NodeViewData):
        value = nodeData.get(self.area.propertyName)
        self.onInnerTextChanged(value)

    def onInput(self, **kwargs):
        self.updateView()

    def onFinished(self, data,propName):
        pass
        self.updateView()

    def updateView(self,prop = None):
        # from editors.models.nodes.baseNode import BaseNode
        nodeModel = self.nodeModel 
        propertyName = self.area.propertyName
        value = nodeModel.getProperty(propertyName)
        self.onInnerTextChanged(value)
        pass

    def keyPressEvent(self, event):
        event.ignore()
        if event.key() == Qt.Key_Return and not event.modifiers() == Qt.ShiftModifier:
            self.returnPressed()
        else:
            super().keyPressEvent(event)

    def close(self):
        super().hide()
        # super().close()

    def show(self):
        super().show()
        self.setMinimumHeight(1)
        self.setMaximumHeight(16777215)
