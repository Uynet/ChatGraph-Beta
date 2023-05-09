from editors.models.edgeModel import EdgeModel
from editors.models.graphs.graphModel import GraphModel
from editors.models.migrate import Migrator
from editors.models.nodeFactory import NodeFactory
from editors.models.nodes.nodeModel import NodeModel
from editors.models.socketModel import SocketModel
from editors.types.dataType import (EdgeData, GraphData, NodeData, NodeProps, SlotData,
                                    SocketData)
from editors.views.nodeView import NodeView
from utils.util import Console


# Get JSON from Scene
class Serializer:
    @staticmethod
    def dataToEdge(edgeData:EdgeData,nodes:list[NodeModel]):
        outNode = None 
        inNode = None 

        outSocketData:SocketData = edgeData.get("output")
        inSocketData:SocketData = edgeData.get("input")
        outNodeId:str = outSocketData.get("nodeId")
        inNodeId:str = inSocketData.get("nodeId")

        for node in nodes:
            if node.id == outNodeId: outNode = node
            if node.id == inNodeId:  inNode = node   
        if outNode == None or inNode == None:
            Console.error("missing connection:" + f"""{outNode} -> {inNode}""" )
            return None

        oId:str = outSocketData.get("socketId") 
        iId:str = inSocketData.get("socketId") 
        startSocket = outNode.getSocket("output" , oId)
        endSocket = inNode.getSocket("input" ,iId)
        return NodeFactory.createEdge(endSocket,startSocket) 

    @staticmethod
    def createNodeOrModule(graphData:GraphData):
        nodes = []
        nodeDatas:list[NodeData] =  graphData.get("nodes")
        for nodeData in nodeDatas:
            if nodeData.get("type") == "ModuleNode":
                node = NodeFactory.createModuleFromData(nodeData)
            else :
                node = NodeFactory.createNodeFromData(nodeData)
            nodes.append(node)
        return nodes

    @staticmethod
    def dataToGraph( graphData:GraphData) -> GraphModel:
        # legacy対応
        graphData = Migrator.convertFromLegacy(graphData)

        # 配列の型
        nodes : list[NodeModel] = Serializer.createNodeOrModule(graphData)
        # 初期化時はedge情報がないためdataから生成する必要がある
        edgeDatas = graphData.get("edges") or []
        edges : list[EdgeModel] = []
        for edgeData in edgeDatas:
            edge : EdgeModel = Serializer.dataToEdge(edgeData,nodes)
            edges.append(edge)
        return GraphModel(nodes,edges)
        
    @staticmethod 
    def graphToData(subGraph : GraphModel) -> GraphData:
        graphData = {}
        graphData["nodes"] = []
        graphData["edges"] = []
        nodes = subGraph.nodes
        edges = subGraph.edges
        for node in nodes:
            graphData["nodes"].append(Serializer.nodeToJson(node))
        for edge in edges:
            graphData["edges"].append(Serializer.edgeToJson(edge))
        return graphData

    @staticmethod
    def getEdgesFromNodes(nodes):
        edges = []
        for node in nodes:
            node:NodeModel
            for edge in node.getEdges():
                if edge not in edges:
                    edges.append(edge)
        return edges

    @staticmethod
    def nodeToJson(node:NodeModel):
        # 座標、ノードの種類、接続情報をjsonで返す
        data = {}
        data["id"] = node.getId()
        data["type"] = node.nodeType
        data["sockets"] = []
        
        sockets = node.getAllSockets() 
        for socket in sockets :
            data["sockets"].append( Serializer.socketToJson(socket)) 
        nodeData = node.nodeData
        props :list[NodeProps]=  nodeData.selialize()
        data["properties"] = props 

        slots :list[SlotData]= node.slots
        slotDatas = []
        for slot in slots:
            slotDatas.append(slot.serialize())
        data["slots"] = slotDatas
        return data


    @staticmethod
    def socketToJson(socket:SocketModel):
        node : NodeModel = socket.parentNodeModel
        nodeId = node.getId()
        socketId = node.getSocketId(socket)
        propName:str = socket.propName
        ioType:str = socket.inOutType.value
        return {"type":ioType,"propName": propName,"name" : socket.getName(),
                "nodeId":nodeId,"socketId":socketId }
    @staticmethod
    def edgeToJson(edge:EdgeModel):
        return {
            "output": Serializer.socketToJson(edge.outSocket),
            "input": Serializer.socketToJson(edge.inSocket)
        }
