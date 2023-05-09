
import configparser
import math
import os
import random
import string

from editors.controllers.mainWindowController import MainWindowController


class Console:
    COLOR_RED = "\033[31m"
    COLOR_YELLOW = "\033[33m"
    COLOR_END = "\033[0m"

    def writeLog(*args,filename:str):
        with open(filename, "a" , encoding="utf-8") as f:
            # args to string
            text = Console.argToStr(*args)
            f.write(text + "\n")
    def argToStr(*args):
        # args to string
        text = ""
        for arg in args:
            text += str(arg)
        return text
    def log(*args):
        # onry dev and no write file
        if os.environ.get('ENV') == 'DEV': print(*args)
    def warn(*args):
        if os.environ.get('ENV') == 'DEV': print(*args)
        else : Console.writeLog(*args, filename="warn_log.txt")
    def error(*args):
        text = Console.argToStr(*args)
        MainWindowController.getInstance().onError("ERROR", text)
        if os.environ.get('ENV') == 'DEV': print(*args)
        else : Console.writeLog(*args, filename="error_log.txt")
    def supper_error(*args):
        print(Console.COLOR_RED, "***** SUPER ERROR *****", *args, "***** SUPER ERROR *****", Console.COLOR_END)

class Util:
    # 現在のディレクトリを取得
    currentPath = os.getcwd()
    dataPath = os.path.join(currentPath, "resources")
    userPath = os.path.join(dataPath, "user")
    configPath = "config.ini"
    nodePath = os.path.join(dataPath, "nodes")
    defaultFilename = os.path.join(nodePath, "default.json")
    def getDefaultIconPath(nodename: str):
        return os.path.join(Util.dataPath, "images", "chatIcons", nodename)

    def getDefaultFilePath():
        return Util.defaultFilename

    def getImageFilePath(filename):
        return os.path.join(Util.dataPath, "images", filename)

    def getCustomStylePath(filename):
        return os.path.join(Util.dataPath, "user", filename)

    def validateConfig():
        datapath = Util.dataPath
        configPath = Util.configPath

        # データパスが存在しない場合は、データパスを作成する
        if not os.path.exists(datapath):
            os.mkdir(datapath)
        if not os.path.exists(Util.nodePath):
            os.mkdir(Util.nodePath)

        # iniファイルが存在しない場合は、iniファイルを作成する
        if not os.path.exists(configPath):
            config = configparser.ConfigParser()
            config['Initial'] = {}
            config['Initial']['isInitialBoot'] = 'True'
            config['APIKEY'] = {}
            config['APIKEY']['openaiKey'] = ''
            with open(configPath, 'w') as f:
                config.write(f)

        # iniファイルからopanaiKeyを取得する
        config = Util.readConfig()
        key=config.get('APIKEY', 'openaiKey')
        # APIキーのバリデーション
        from api.apis import validateAPIKey
        response, error = validateAPIKey(key)
        if response:return True
        if error:return False
         
    def readConfig():
        config = configparser.ConfigParser()
        config.read(Util.configPath)
        return config
    def writeConfig(config):
        with open(Util.configPath, 'w') as f:
            config.write(f)

    # math
    # [0,1,-1,2,-2...]           
    def sequence(n):
        return (-1)**n * math.ceil(n/2)

    def getGoodMergin(min , max , height ):
        # lerp
        return min + (max - min) * height / 1000

    def genRandomhash():
        return ''.join(random.choices(string.ascii_letters + string.digits, k=8))

    def apply_properties_diff(base_properties, diff_properties):
        base_property_dict = {prop["name"]: prop for prop in base_properties}
        for diff_prop in diff_properties:
            prop_name = diff_prop["name"]
            if prop_name in base_property_dict:
                base_property_dict[prop_name]["value"] = diff_prop["value"][1]

    def diffJson(dict1, dict2):
        def list_diff(list1, list2):
            if len(list1) != len(list2):
                return True

            for item1, item2 in zip(list1, list2):
                if isinstance(item1, dict) and isinstance(item2, dict):
                    if Util.diffJson(item1, item2):
                        return True
                elif item1 != item2:
                    return True

            return False

        diff = {}

        # 全てのキーを取得
        keys1 = set(dict1.keys())
        keys2 = set(dict2.keys())
        all_keys = keys1 | keys2

        for key in all_keys:
            if key not in dict1:
                diff[key] = [None, dict2[key]]
            elif key not in dict2:
                diff[key] = [dict1[key], None]
            else:
                val1 = dict1[key]
                val2 = dict2[key]

                # ネストされたディクショナリの場合
                if isinstance(val1, dict) and isinstance(val2, dict):
                    nested_diff = diffJson(val1, val2)
                    if nested_diff:
                        diff[key] = nested_diff
                # リストの場合
                elif isinstance(val1, list) and isinstance(val2, list):
                    if list_diff(val1, val2):
                        diff[key] = [val1, val2]
                # 値が異なる場合
                elif val1 != val2:
                    diff[key] = [val1, val2]

        return diff

    def genMessages(prompt,systemPrompt,histories):
        messages = []
        if (systemPrompt is not None) :
            messages.append({"role": "user", "content": systemPrompt})
        for history in histories:
            messages.append(history) 

        messages.append( {"role": "user", "content": prompt})
        return messages