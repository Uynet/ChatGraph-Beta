import json
import threading

from PyQt5.QtCore import QThread, pyqtSignal

from debug.debugCommand import DebuggerCommand
from utils.util import Console


class NodeThread(QThread):
    result = pyqtSignal(str)
    stream = pyqtSignal(str)
    running = pyqtSignal(str)
    task = pyqtSignal(str)
    def __init__(self,script,nodeModel,input):
        self.stopped_event = threading.Event()   
        self.node = nodeModel
        self.script=script 
        self.input = input 
        super().__init__()

    def onInputRunning(self,data):
        self.running.emit(data)

    def run(self):
        try:
            self.state = "SUCCESS" 
            self.answer = DebuggerCommand.execute(self.script,self.node)
        except Exception as e:
            self.state = "ERROR" 
            self.answer = str(e) 

        finally:
            if not self.stopped_event.is_set():
                r = {
                    "state": self.state,
                    "answer": str(self.answer)
                }
                # dictをjsonに変換
                r = json.dumps(r)
                self.result.emit(r)
            else :
                Console.log("stopped!", self.answer)
    def stop(self):
        r= ({
            "state": "STOPPED",
            "answer": "STOPPED"
        })
        r= json.dumps(r)
        self.result.emit(r)
        self.stopped_event.set()