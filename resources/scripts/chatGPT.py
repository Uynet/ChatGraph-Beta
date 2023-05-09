from api.apis import chatGPTReq
from utils.util import Util

def formatOutput(data):
    import re
    pattern = node.get("format")
    # pattern = r"```python\s+(.*?)\s+```"
    matched = re.findall(pattern, data, re.DOTALL)
    if matched:
        return matched[0]
    else:
        return "Invalid format"

systemPrompt = node.get("systemPrompt")
temp = node.get("template")
tempIn = temp.replace("{inputed}",node.input)
node.set("inputed",tempIn)
history = node.get("history") 
messages = Util.genMessages(tempIn,systemPrompt,history)
try:
    answer = ""
    for talk in chatGPTReq(messages,stream=True):
        answer += talk
        node.stream(answer , isOutput=False)
    answer = formatOutput(answer)
    print(answer)
except Exception as e:
    answer = str(e)
    raise(e)
