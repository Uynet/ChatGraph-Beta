from PyQt5.QtWidgets import QTextEdit

from utils.styles import Styles


# for history
class InspectorPropertyList(QTextEdit):
    def __init__(self,key,values:list, node):
        super().__init__()

        self.key = key
        self.node = node
        text = str(values)
        self.setPlainText(text)
        self.setReadOnly(True)
        self.setStyleSheet(Styles.className("inspectorPropertyList","inspector.scss")) 

    # 外部から値を変更されたとき
    # historyは編集不可なのでこれはresetHistroyのみ
    def onChangeProperty(self , values):
        text = str(values)
        self.setPlainText(text)
        return

    def changeNodeProperty(self):
        value = self.toPlainText()
        self.node.onChangeProperty(self.key,value , isUpdateView=True , isUpdateInspector=False)
        return