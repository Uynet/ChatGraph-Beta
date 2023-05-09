from PyQt5.QtWidgets import QCheckBox

from editors.models.nodes.nodeModel import NodeModel
from utils.styles import Styles


class InspectorPropertyCheckBox(QCheckBox):
    def __init__(self,key,value:bool, node:NodeModel):
        super().__init__(str(value))

        self.key = key
        self.node = node
        self.setChecked(value)
        self.setText(str(value))
        self.setStyleSheet(Styles.qClass("checkBox","QCheckBox","inspector.scss")) 
        # connect
        self.stateChanged.connect(self.changeNodeProperty)

    def changeNodeProperty(self):
        value = self.isChecked()
        #標示を変更
        self.setText(str(value))
        self.node.onChangeProperty(self.key,value , isUpdateView=True , isUpdateInspector=False)
        return

    # 外部から値を変更されたとき
    def onChangeProperty(self , value):
        # ブロックする 
        self.stateChanged.disconnect(self.changeNodeProperty)
        self.setText(value)
        # ブロック解除
        self.stateChanged.connect(self.changeNodeProperty)
        return