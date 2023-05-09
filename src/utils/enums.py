from enum import Enum

from PyQt5.QtWidgets import QGraphicsItem


class PropertyType(Enum):
    CHAT= "chat" 
    SET = "set"
    def fromStr(string):
        assert string in {"chat","set"}
        if string == "chat":
            return PropertyType.CHAT 
        elif string == "set":
            return PropertyType.SET 

class InOutType(Enum):
    IN = "input"
    OUT = "output"
    # 反対のやつ
    def other(self):
        if self == InOutType.IN:
            return InOutType.OUT
        else:
            return InOutType.IN
    def fromStr(string):
        assert string in {"input","output"}
        if string == "input":
            return InOutType.IN
        else:
            return InOutType.OUT

class NodeProcessState(Enum):
    WAITING = 0
    RUNNING = 1
    FINISHED = 2
    STOPPED = 3
    ERROR = 4

# get color name from state
# colorNames = ["nodeWait","nodeRunning","nodeFinished","nodeStopped","nodeError"]
 
class NodeProcessStateColor(Enum):
    WAITING = "nodeWait"
    RUNNING = "nodeRunning"
    FINISHED = "nodeFinished"
    STOPPED = "nodeStopped"
    ERROR = "nodeError"


class EventType(Enum):
    MOUSE_PRESS = 0
    MOUSE_MOVE = 1
    MOUSE_RELEASE = 2
    MOUSE_DOUBLE_CLICK = 3
    MOUSE_WHEEL = 4

class CgpViewType(Enum):
    SOCKET = "socket" 
    NODE = "node" 
    NODE_ICON = "nodeIcon" 
    EDGE = "edge" 
    BG = "none"
    HUB = "hub"

    def getRoot(item : QGraphicsItem):
        from editors.views.nodeWindows.socketView import SocketBody
        if isinstance(item, SocketBody):
            return item.parent
        else:
            return item 

    def getFrom(item : QGraphicsItem):
        from editors.views.nodeWindows.socketView import SocketBody, SocketView
        from editors.views.edgeView import EdgeView
        from editors.views.nodeWindows.hubWindow import HubWindow
        from editors.views.nodeWindows.nodeWindow import NodeWindow
        itemType = type(item)
        if itemType in{ SocketBody , SocketView}:
            return CgpViewType.SOCKET 
        if itemType  in{ NodeWindow }:
            return CgpViewType.NODE
        if itemType in{ HubWindow}:
            return CgpViewType.HUB
        if itemType in{ EdgeView}:
            return CgpViewType.EDGE
        else:
            return CgpViewType.BG 
