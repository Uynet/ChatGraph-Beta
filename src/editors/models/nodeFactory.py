import sys

from editors.models.edgeModel import EdgeModel
from editors.models.nodes.execNode import ExecNode
from editors.models.nodes.gptNode import GPTNode
from editors.models.nodes.hubNode import HubNode
from editors.models.nodes.ifNode import IfNode
from editors.models.nodes.nodeModel import NodeModel
from editors.models.nodes.outputNode import OutputNode
from editors.models.nodes.textInputNode import TextInputNode
from editors.models.socketModel import SocketModel
from editors.types.dataType import ModuleNodeData, NodeViewData, SlotData, SocketData
from utils.enums import InOutType
from utils.util import Console


class NodeFactory:
    @staticmethod
    def createNode( typeString):
        if type == "ModuleNode":
            Console.error("Invalid type : ModuleNode")
            return None
        # string to type
        # 型名から型を取得
        NodeType = getattr(sys.modules[__name__], typeString)
        assert NodeType in {HubNode, ExecNode, GPTNode, IfNode, OutputNode, TextInputNode}
        NodeType : NodeModel
        node = NodeType()
        return node

    # シーンをモジュールノードとして開く場合
    def nodesToModule(nodes):
        from editors.models.nodes.moduleNode import ModuleNode
        moduleNode = ModuleNode() 
        # dummy view props
        defaultViewProps = NodeViewData([
            {"name":"icon" , "value":"./resources/images/chatIcons/defaults/ModuleNode.png"}
        ])

        moduleNode.initProperties(defaultViewProps)
        moduleNode.nodeView.initProperties(defaultViewProps)
        moduleNode.addSocketsByNodes(nodes)
        moduleNode.resetId()
        return moduleNode

    # モジュールノードのあるシーンを開く場合
    def createModuleFromData(moduleNodeData:ModuleNodeData):
        from editors.models.nodes.moduleNode import ModuleNode
        moduleNode = ModuleNode() 
        nodeViewData = NodeViewData(moduleNodeData["properties"])
        moduleNode.initProperties(nodeViewData )
        sockets = moduleNodeData["sockets"]
        moduleNode.addSockets(sockets)
        moduleNode.setId(moduleNodeData["id"])
        moduleNode.nodeView.initProperties(nodeViewData)
        moduleNode.setProperty("isPacked" , True)
        # この時点ではファイルが読み込まれておらず、実態はない

        moduleNode.loadFile()
        moduleNode.connectToInnerNodes()
        return moduleNode

    # ノード単体
    def createNodeFromData(nodeJsonData):
        node :NodeModel= NodeFactory.createNode( nodeJsonData["type"])
        socketDatas:list[SocketData]= nodeJsonData["sockets"]
        nodeViewData = NodeViewData(nodeJsonData["properties"])
        slotDatas:list[SlotData] = nodeJsonData["slots"]
        node.initProperties(nodeViewData )
        node.addSlots(slotDatas)
        node.addSockets(socketDatas)
        node.setId(nodeJsonData["id"])
        node.nodeView.initProperties(nodeViewData)
        return node

    def createEdge(s1:SocketModel, s2:SocketModel):
        assert(s1.inOutType != s2.inOutType)
        if s1.inOutType == InOutType.OUT:
            outSocket = s1
            inSocket = s2
        else:
            outSocket = s2
            inSocket = s1
        edge = EdgeModel(inSocket, outSocket)
        return edge
    
    def createSocketFromData(socketData):
        socket = SocketModel(socketData["socketType"], socketData["socketId"])
        return socket