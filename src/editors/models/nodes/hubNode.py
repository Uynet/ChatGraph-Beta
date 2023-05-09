from editors.models.nodes.nodeModel import NodeModel
from editors.views.nodeView import NodeView
from editors.views.nodeWindows.hubWindow import HubWindow
from utils.enums import InOutType, NodeProcessState, PropertyType

class HubNode(NodeModel):
    def __init__(self):
        nodeType = type(self).__name__
        super().__init__(nodeType)
        self.nodeView= NodeView(self , Window = HubWindow)

    def onReleaseWip(self):
        self.clearSockets()
        socks = self.getUnConnectedScokets()
        
        if len(socks) == 0: 
            self.addSocket(InOutType.IN,propName="none")

    def getUnConnectedScokets(self):
        socks = self.getAllSockets()
        unConnectedSocks = []
        for soc in socks:
            if not soc.hasEdge():
                unConnectedSocks.append(soc)
        return unConnectedSocks

    # 接続のないソケットを削除
    def clearSockets(self):
        socks = self.getUnConnectedScokets()
        for soc in socks:
            nodeGraph = self.getNodeGraph() 
            nodeGraph.removeSocketChain(soc) 


    def onInput(self,data,propName:str,socket= None):
        super().onFinished(data=data,propName=propName)