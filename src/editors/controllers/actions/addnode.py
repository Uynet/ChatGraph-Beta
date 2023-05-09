from editors.models.nodes.nodeModel import NodeModel
from utils.sound import CSound
from editors.controllers.actions.cgpAction import CgpAction


class ADD_NODE(CgpAction):
    def __init__(self,node:NodeModel):
        self.node = node
        # data = Selializer.nodeToData(node) 
        super().__init__("ADD_NODE")

    def getNode(self):
        return self.node

    def doAction(self,ngc):
        self.node.resetId()
        ngc.addToScene(self.node)
        self.node.addToGraph(ngc.nodeGraph)
        CSound.play("put.wav")
        pass