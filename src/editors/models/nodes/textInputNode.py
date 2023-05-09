from editors.models.nodes.nodeModel import NodeModel
from editors.views.nodeView import NodeView
from utils.enums import PropertyType


class TextInputNode(NodeModel):
    def __init__(self):
        nodeType = type(self).__name__
        super().__init__(nodeType)
        self.nodeView = NodeView(self)

    # 実際には入力ソケットは無いがchat欄の入力を受け取る
    def onInput(self,data, socket = None , propName = "output") :
        super().onInput( data=data, socket=socket ,propName =propName)

        self.setProperty("output", str(data))

        super().onFinished(data=data,propName="output")