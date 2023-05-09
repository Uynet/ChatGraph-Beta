class GraphModel():
    from editors.models.edgeModel import EdgeModel
    from editors.models.nodes.nodeModel import NodeModel
    def __init__(self , nodes:list[NodeModel] , edges:list[EdgeModel]):
        self.nodes = nodes
        self.edges = edges