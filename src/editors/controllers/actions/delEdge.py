
from editors.controllers.actions.cgpAction import CgpAction
from editors.models.edgeModel import EdgeModel


class DEL_EDGE(CgpAction):
    def __init__(self,edge:EdgeModel):
        self.edge = edge
        super().__init__("DELETE_EDGE")

    def doAction(self ,ngc):
        scene = ngc.nodeGraph.scene
        self.edge.detachSockets()
        self.edge.removeFromScene(scene)