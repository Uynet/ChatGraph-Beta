import glob
import json
import os

from utils.util import Console


# return data from file path
class FileLoader():
    lastOpenFile = None 

    # モジュールの読み込み時に循環参照を防ぐために、読み込み中のファイルを記録しておく
    loadingFiles = []
    resources = {}
    soundPath = os.path.join("resources" , "sounds")    

    @staticmethod
    def preloadAll():
        for path in glob.glob(FileLoader.soundPath+ "/*.wav"):
            FileLoader.preload(path)

    def preload(path):
        from PyQt5.QtMultimedia import QSound
        sound_path = path 
        sound = QSound(sound_path)
        # 音声ファイルをプリロード
        sound.play()
        sound.stop()
        FileLoader.resources[sound_path] = sound

    @staticmethod
    def getResource(path):
        if path in FileLoader.resources:
            return FileLoader.resources[path]
        else:
            raise Exception(f"リソースが見つかりませんでした: {path}")


    def loadGraphData(filePath , callback= None, onerror= None):
        if filePath in FileLoader.loadingFiles:
            if onerror != None: onerror("モジュールの再帰呼び出しを検出しました:", filePath)
            return None
        FileLoader.loadingFiles.append(filePath)
        try:
            with open(filePath, "r") as file:
                graphJsonData = json.load(file)
                if callback != None: callback(graphJsonData)
                FileLoader.loadingFiles = []
                return graphJsonData 
        except FileNotFoundError as e:
            if onerror != None: onerror(e)
            Console.error(f"File not found: {filePath}")
            FileLoader.loadingFiles = []
            return None

    def write(data , fileName:str):
        try :
            with open(fileName, "w") as file:
                json.dump(data, file)
                return fileName
        except FileNotFoundError:
            Console.error(f"File not found: {fileName}")
            return None

    def read(filepath:str,encoding="utf-8"):
        try :
            with open(filepath, "r" ,encoding=encoding) as file:
                return file.read() 
        except FileNotFoundError:
            Console.error(f"File not found: {filepath}")
            return None
    
    # ファイルパス内のファイルまたはフォルダを表示
    def browse(filePath):
        files = [f for f in glob.glob(os.path.join(filePath, "*")) if os.path.isfile(f)]
        folders = [f for f in glob.glob(os.path.join(filePath, "*")) if os.path.isdir(f)]

        data = {
            "files":files,
            "folders":folders
        }
        return data 

