import os
from abc import ABC, abstractmethod

from utils.util import Console


class CgpDatas:
    def __init__(self, **kwargs):
        self.set(**kwargs)

    def set(self,**kwargs):
        for key, value in kwargs.items():
            self.__dict__[key] = value
    def get(self, name):
        return self.__dict__[name]

class NodeProperty():
    def __init__(self, name, value):
        self.name = name
        self.value = value
    def serialize(self):
        return {
            "name": self.name,
            "value": self.value
        }

# これはpropertiesの中身
class NodeProps():
    def __init__(self, properties): 
        # データが不正な場合のデフォルト値
        # transform
        self.positionX = 0.0
        self.positionY = 0.0
        self.width = 200.0
        self.height = 200.0
        # view
        self.icon = os.path.join("resources", "images", "chatIcons", "defaults", "TextInputNode.png")
        self.label = "Node"
        self.isSendChat = False
        self.setProps(properties)

    def setProps(self, properties:list[NodeProperty]):
        for prop in properties:
            name = prop["name"]
            value = prop["value"]  
            if name in ["isSendChat", "isMemorable"]:
                value = bool(value)
            self.set(name , value)

    def get(self, name):
        try :
            return getattr(self, name)
        except AttributeError as e:
            Console.warn("missing data",e)
            return None
    def getCustomProps(self):
        props = vars(self)
        props = {k: v for k, v in props.items() if k not in ["positionX", "positionY", "width", "height", "isSendChat","isMemorable","label","icon","script", "systemPrompt", "inputed", "output", "history"]}
        return props

    def getProps(self ,filter = None) -> list[NodeProperty]:
        props = vars(self)
        if filter == "transform" :
            props = {k: v for k, v in props.items() if k in ["positionX", "positionY", "width", "height"]}
        if filter == "base" :
            props = {k: v for k, v in props.items() if k in ["isSendChat","isMemorable","label","icon","script", "systemPrompt", "inputed", "output"]}
        if filter == "history" :
            props = {k: v for k, v in props.items() if k in ["history"]}
        if filter == "custom" :
            # どれにも属さないもの
            props = self.getCustomProps() 
        # to NodeProperty
        props = [NodeProperty(k,v) for k,v in props.items()]
        return props

    def selialize(self) -> dict:
        props = self.getProps()
        a = []
        for p in props:
            a.append(p.serialize())
        return a 

    def set(self, name, value):
        property_type_map = {
            "positionX": float,
            "positionY": float,
            "width": float,
            "height": float,
            "icon": str,
            "label": str,
            "systemPrompt": str,
            "history": list
        }
        # 必須となくてもよいものを分けたい
        if name in property_type_map:
            setattr(self, name, property_type_map[name](value))
        else:
            # custom props
            setattr(self, name,value)
            pass 

class NodeViewData(NodeProps):
    def __init__(self, properties): 
        self.positionX: float
        self.positionY: float
        self.width: float
        self.height: float
        self.output: str
        self.input:str
        self.icon: str # filepath
        self.label: str
        super().__init__(properties)
    def get(self, name):
        return super().get(name)
    def set(self, property_name, value):
        super().set(property_name, value)


class SocketData(CgpDatas):
    type: str # input or output
    propertyType : str 
    name: str
    nodeId : str
    socketId : int

class EdgeData(CgpDatas):
    output: SocketData
    input: SocketData

class ModuleNodeData(CgpDatas):
    id: str
    type: str
    properties: list[NodeProperty]
    sockets: list[SocketData]
    source : str

# property slot
class SlotData(CgpDatas):
    propName: str
    type: str # SET or CHAT
    ioType: str # input or output
    def serialize(self):
        return {
            "propName": self.propName,
            "type": self.type,
            "ioType": self.ioType
        }

class NodeData(CgpDatas):
    id: str
    type: str
    properties: list[NodeProperty]
    sockets: list[SocketData]
    slots: list[SlotData]

class ModuleNodeData:
    def __init__(self):
        self.id = ""
        self.type = "ModuleNode"
        self.properties = {}
        self.sockets = []

# JSONで保存するデータ形式
class GraphData(CgpDatas):
    nodes: list[NodeData]
    edges: list[EdgeData]