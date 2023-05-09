import json

from editors.models.nodes.execNode import ExecNode

class GPTNode(ExecNode):
    def resetHistory(self):
        self.setProperty("history",[] , isUpdateInspector=True)
        self.setProperty("output","", isUpdateInspector=True)
        self.setProperty("inputed","", isUpdateInspector=True)

    def onChatResult(self, data:str):
        # str to json
        isMemorable = self.getProperty("isMemorable")
        if isMemorable:
            # success
            history = self.getProperty("history")
            prompt = self.getProperty("inputed")
            result = json.loads(data)
            answer = result["answer"]
            history.append({"role":"user","content":prompt})
            history.append({"role":"assistant","content":answer})
            self.setProperty("history",history,isUpdateInspector=True)
        super().onChatResult(data)