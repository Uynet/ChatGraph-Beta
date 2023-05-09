from editors.types.dataType import GraphData, SlotData


class SlotLib:
    systemPrompt = SlotData(propName="systemPrompt",type="set",ioType="input")
    script = SlotData(propName="script",type="set",ioType="input")
    flag = SlotData(propName="flag",type="set",ioType="input")
    chatIn = SlotData(propName="inputed",type="chat",ioType="input")
    chatOut = SlotData(propName="output",type="chat",ioType="output")
    
    @staticmethod
    def maps():
        return {
            "GptNode": [SlotLib.systemPrompt, SlotLib.script, SlotLib.chatIn],
            "TextInputNode": [SlotLib.chatOut],
            "OutputNode": [SlotLib.chatIn],
            "ExecNode": [SlotLib.script, SlotLib.chatIn, SlotLib.chatOut],
            "IfNode": [SlotLib.flag, SlotLib.script, SlotLib.chatIn, SlotLib.chatOut],
            "ModuleNode": [SlotLib.chatIn, SlotLib.chatOut],
            "HubNode": [],
        }

    @staticmethod
    def getSlots(nodeTypeString):
        return SlotLib.maps().get(nodeTypeString, [])


class Migrator:


    @staticmethod
    def convertFromLegacy(data : GraphData):
        nodes = data.get("nodes")
        for node in nodes:
            if not Migrator.validateNodeData(node):
                Migrator.migrateNodeData(node)

            sockets = node.get("sockets")
            for socket in sockets:
                if Migrator.validateSocletData(socket):continue
                Migrator.migrateSocketData(socket)
        return data
    @staticmethod
    def validateSocletData(socketData):
        return "propName" in socketData

    @staticmethod
    def validateNodeData(nodeData):
        return "slots" in nodeData
    
    @staticmethod
    def migrateNodeData(nodeData):
        nodeType = nodeData["type"]
        # assert nodeType in {HubNode, ExecNode, GPTNode, IfNode, OutputNode, TextInputNode}
        assert nodeType in {"HubNode", "ExecNode", "GPTNode", "IfNode", "OutputNode", "TextInputNode" , "ModuleNode"}
        slots = SlotLib.getSlots(nodeType) 
        nodeData["slots"] = slots 
        pass

    @staticmethod
    def migrateSocketData(socket):
        property_type_to_prop_name = {
            "FLAG": "flag",
            "SCRIPT": "script",
            "CHAT": "chat",
            "ROLE": "systemPrompt"
        }

        if socket["propertyType"] in property_type_to_prop_name:
            pn = property_type_to_prop_name[socket["propertyType"]]
            if pn == "chat":
                io = socket["type"]
                if io == "input": pn = "inputed"
                elif io == "output": pn = "output"
            socket["propName"] = pn
            del socket["propertyType"]
        pass