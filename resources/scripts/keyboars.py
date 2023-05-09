import json
import re

string = node.input

match = re.search(r'({"write":".+?"})', string)

if match:
    parsed = json.loads(match.group(1))
    print(parsed['write'])
else :
    s = f"""ERROR : 入力に失敗しました。{{"write":"command"}}の形式で入力してください。"""
    raise Exception(s)
