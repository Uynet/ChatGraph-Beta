from editors.models.nodes.execNode import ExecNode

class IfNode(ExecNode):
    def setOutSocket(self , name):
        pass

    def onChatResult(self, data:str):
        flag = self.getProperty("flag")
        sockets = self.sockets.outputs
        # outsocketsと同じ名前のflag
        outSockets = [socket for socket in sockets if socket.getName() == flag]
        super().onFinished(data , propName="output" , outSockets=outSockets)
