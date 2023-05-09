from editors.models.nodes.moduleNode import ModuleNode
from editors.models.nodes.nodeModel import NodeModel
from editors.views.nodeView import NodeView

class OutputNode(NodeModel):
    def __init__(self):
        nodeType = type(self).__name__
        super().__init__( nodeType)
        self.moduleNode = None
        self.nodeView = NodeView(self)

    def onInput(self,data:str ,propName, **kwords):
        super().onInput(data=data, **kwords)
        self.setProperty("inputed", data)
        self.setProperty("output",data)
        connectedModule:ModuleNode = self.getConnectedModule()

        if connectedModule is None: 
            super().onFinished(data=data,propName="output",outSockets=[])
            return
        else: 
            nodeName:str = self.getProperty("label")
            connectedModule.onOutput(data, nodeName=nodeName)
    
    # out module must be Single        
    def connectModule(self, moduleNode):
        self.moduleNode = moduleNode

    def getConnectedModule(self):
        return self.moduleNode
        