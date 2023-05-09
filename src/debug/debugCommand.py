import queue
import sys
from io import StringIO

from editors.models.nodes.nodeModel import NodeModel
from editors.views.nodeWindows.nodeWindow import NodeWindow


class DebuggerCommand():
    # implemet REPL shell
    shell = "REPL"
    pref = "python >>"
    cmdqueue = queue.Queue( maxsize=100 )
    def parce(text):
        if DebuggerCommand.shell == "EDITOR":
            return text
        else:
            classNameText = "DebuggerCommand"
            f"""{classNameText}.{text}""" 
            return text

    # このnodeはNode自身の参照をローカル変数として渡すために使っている
    def execute(text, node):
        DebuggerCommand.cmdqueue.put(text)
        try:
            stdout = sys.stdout
            sys.stdout = StringIO()

            exec(text,locals(),globals())
            output = sys.stdout.getvalue()
            # 標準出力を元に戻す
            sys.stdout = stdout
            print(output)
            return output
        except Exception as e:
            sys.stdout = stdout
            raise e 




    def shell():
        return DebuggerCommand.shell 
    def exec(text):
        return DebuggerCommand.execute(text,DebuggerCommand)
    def mainWindow():
        from graph import qtApp
        return qtApp.mainwindow
    def n():
        nodes = DebuggerCommand.nodes()
        return nodes[0]
    def nodes():
        # get basenode
        items = DebuggerCommand.items()
        nodes = [item for item in items if isinstance(item, NodeWindow)]
        return nodes
    def focus():
        return DebuggerCommand.scene().focusItem()
    def items():
        return DebuggerCommand.scene().items()
    def scene():
        scene = DebuggerCommand.mainWindow().nodeScene
        return scene
    def app():
        from graph import qtApp
        return qtApp
    def help():
        return "help"
    def edit():
        DebuggerCommand.shell = "EDITOR"
        return "edit >>"
    def vim():
        DebuggerCommand.shell = "VIM"
        return "vim >>"
    def repl(text,self):
        try:
            DebuggerCommand.shell = "REPL"
            text = "DebuggerCommand" + "." + text
            value = eval(text, locals(), globals())
            return value
        except Exception as e:
            return e