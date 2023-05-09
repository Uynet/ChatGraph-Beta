
from __future__ import annotations
from typing import TYPE_CHECKING

from editors.models.edgeModel import EdgeModel
if TYPE_CHECKING:
    from editors.models.nodeGraph import NodeGraph

from PyQt5.QtCore import QPoint
from PyQt5.QtWidgets import QAction, QFileDialog, QMenu
from editors.controllers.actions.cgpAction import CgpAction

from editors.controllers.mainWindowController import MainWindowController
from editors.models.graphs.graphModel import GraphModel
from editors.models.nodes.execNode import ExecNode
from editors.models.nodes.gptNode import GPTNode
from editors.models.nodes.hubNode import HubNode
from editors.models.nodes.nodeModel import NodeModel
from editors.models.nodes.textInputNode import TextInputNode
from editors.models.serializer import Serializer
from editors.models.socketModel import SocketModel
from editors.views.nodeWindows.socketView import SocketBody, SocketView
from editors.views.nodeIconImage import NodeIconImage
from editors.views.nodeWindows.nodeWindow import NodeWindow
from editors.views.nodeWindows.WindowFlameLabel import WindowFlameLabel
from utils.enums import CgpViewType, InOutType
from utils.fileLoader import FileLoader
from utils.sound import CSound
from utils.styles import Styles
from utils.util import Util

def show(menu, pos):
    menu.setStyleSheet(Styles.qClass("QMenu","QMenu"))
    menu.exec_(pos)

def showContextMenu(eventScenePos:QPoint , menuPos:QPoint,scene):
    nodeGraph:NodeGraph = scene.nodeGraph
    defaultNodePath = Util.nodePath

    def addNode(nodeType):
        defaultNodeFile = defaultNodePath + f"""/defaultNodes/{nodeType}.json"""
        data = FileLoader.loadGraphData(defaultNodeFile)
        subGraph : GraphModel = Serializer.dataToGraph(data)
        node = subGraph.nodes[0]
        node.setProperty("positionX",eventScenePos.x() , isUpdateView=True)
        node.setProperty("positionY",eventScenePos.y() , isUpdateView=True)

        action = CgpAction.ADD_NODE(node)
        ngc = nodeGraph.getController() 
        ngc.onCgpAction(action)

    menu = QMenu()
    nodeNames = ["GPTNode","TextInputNode", "OutputNode", "ExecNode" ,"HubNode" , "IfNode"]

    for name in nodeNames:
        action = QAction(f"+ {name}", menu)
        menu.addAction(action)
        action.triggered.connect(lambda _, nodeType=name: addNode(nodeType))

    show(menu ,menuPos)

def getmenuesByNodeType(node:NodeModel , nodeGraph):
    nodeType = type(node)
    nodeGraph:NodeGraph
    ngc = nodeGraph.getController() 
    def delete_node():
        CSound.play("put.wav")
        ngc.onCgpAction(CgpAction.DEL_NODE(node))
    def addInputSocket():
        node.addSocket(InOutType.IN)
        CSound.play("put.wav")
    def addOutputSocket():
        node.addSocket(InOutType.OUT)
        CSound.play("put.wav")
    def resetHistory():
        node.resetHistory()
        CSound.play("reset.wav")
    def stop_node():
        node.onStop()
        CSound.play("stop.wav")
    optionalMenues = [
        # ("run", run_node),
        # ("addInput", addInputSocket),
        # ("addOutput", addOutputSocket),
        ("resetHistory (記憶を消す)", resetHistory),
        ("delete", delete_node),
        ("stop", stop_node),
    ]
    def actionFilter(action_names):
        items = optionalMenues
        return [item for item in items if item[0] in action_names]
        

    if nodeType == GPTNode:
        return optionalMenues
    if nodeType == TextInputNode:
        return actionFilter(["addOutput", "delete" ])
    if nodeType == ExecNode:
        return actionFilter(["addInput", "addOutput", "delete","stop" ])
    if nodeType == HubNode:
        return actionFilter(["delete" ])
    else :
        return actionFilter(["addInput", "delete" ] ) 

def showSocketMenu(socketView:SocketView, position, scene):
    nodeGraph = scene.nodeGraph
    socketModel : SocketModel =  socketView.getModel()
    name = socketModel.getName()

    #cant delete
    if  name != "":
        return
    def add():
        node = socketModel.getParent()
        ioType = socketModel.inOutType
        propName = socketModel.propName
        name = socketModel.getName() 
        node.addSocket(ioType , propName,name)

    def remove():
        nodeGraph.removeSocketChain(socketModel)

    menu = QMenu()
    actions = [
        {"label": "remove", "func": remove},
        {"label": "add", "func": add},
        # {"label": "rename", "func": rename},
        # {"label": "swap side", "func": swapSide}
    ]

    for action_dict in actions:
        action = QAction(action_dict["label"], menu)
        action.triggered.connect(action_dict["func"])
        menu.addAction(action)

    menu.setStyleSheet(Styles.qClass("QMenu","QMenu"))
    menu.exec_(position)

# プロパティ名を右クリックしたときの
def showNodePropertyMenu(nodeModel , propName,gpos):
    mainwindow = MainWindowController.getMainWindow()
    graphView = mainwindow.getGraphView()
    def loadFile():
        path = QFileDialog.getOpenFileName(graphView, 'Open file', './', 'prompt files (*.txt *.py)')[0]
        # キャンセル時
        if path == "":
            return
        data = FileLoader.read(path) 
        nodeModel.onChangeProperty(propName, data , isUpdateView = True)
    menu = QMenu()
    menu.addAction(QAction("load file", menu))
    menu.actions()[0].triggered.connect(loadFile)
    show(menu ,gpos)

def showIconMenu(nodeIcon,pos,scene):
    nodeIcon : NodeIconImage 
    nodeModel: NodeModel = nodeIcon.nodeModel

    mainwindow = MainWindowController.getMainWindow()
    graphView = mainwindow.getGraphView()

    def changeIcon():
        path = QFileDialog.getOpenFileName(graphView, 'Open file', './', 'Image files (*.jpg *.gif *.png)')[0]
        if path == "":
            return
        nodeModel.onChangeProperty("icon", path , isUpdateView = True)

    menu = QMenu()
    menu.addAction(QAction("change Icon", menu))
    menu.actions()[0].triggered.connect(changeIcon)
    show(menu ,pos)

def showNodeMenu(node, pos, scene):
    nodeGraph = scene.nodeGraph
    actions = getmenuesByNodeType(node, nodeGraph)
    menu = QMenu()
    for action_text, action_func in actions:
        action = QAction(action_text, menu)
        action.triggered.connect(action_func)
        menu.addAction(action)
    show(menu ,pos)


def showEdgeMenu(edge:EdgeModel , gpos , scene):
    menu = QMenu()
    qAction = QAction("delete edge", menu)

    def deleteEdge():
        nodeGraph = scene.nodeGraph
        ngc = nodeGraph.getController()
        ngc.onCgpAction(CgpAction.DEL_EDGE(edge))
    qAction.triggered.connect(deleteEdge)
    menu.addAction(qAction)
    show(menu ,gpos)


def showMenu(scene, eventScenePos, item):
    # ????
    graphView = scene.views()[0]
    vpos= graphView.mapFromScene(eventScenePos)
    gpos = graphView.viewport().mapToGlobal(vpos)
    # ちょっと被るので右に
    gpos.setX(gpos.x()+20)
    cgpViewType = CgpViewType.getFrom(item)

    # if cgpViewType == CgpViewType.EDGE:
    #     edgeModel:EdgeModel = item.getModel()
    #     showEdgeMenu(edgeModel,gpos,scene)
    if cgpViewType == CgpViewType.HUB:
        node:NodeModel = item.getModel()
        showNodeMenu(node,gpos,scene)
    # must fix
    if(isinstance(item, NodeWindow) or isinstance(item, WindowFlameLabel) ):
        node:NodeModel = item.nodeModel
        showNodeMenu(node,gpos,scene)
    elif(isinstance(item, SocketBody) ):
        # must fix
        nodeSocket = item.parent
        showSocketMenu(nodeSocket,gpos,scene)
    elif (isinstance(item,NodeIconImage) ):
        # アイコン画像を変更
        showIconMenu(item,gpos,scene)
    elif item is None : showContextMenu(eventScenePos,gpos,scene)
    else :
        return