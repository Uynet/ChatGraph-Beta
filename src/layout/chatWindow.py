from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import (QHBoxLayout, QLabel, QLineEdit, QPushButton,
                             QScrollArea, QTextEdit, QVBoxLayout, QWidget)

from editors.views.nodeScene import NodeScene
from utils.styles import Styles
from utils.util import Util


class ChatMessageArea(QTextEdit):
    def __init__(self,message):
        super().__init__(message)
        self.textChanged.connect(self.adjust_size)
        s = Styles.className("messageLabel" , "chat.scss")
        self.setStyleSheet(s)
        self.setReadOnly(True)
        # self.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Minimum)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setAcceptRichText(True)

    def showEvent(self, event):
        self.adjust_size()
        super().showEvent(event)

    def adjust_size(self):
        document_height = self.document().size().height()
        pad = 30
        self.setFixedHeight(document_height + pad)


        

class ChatNameWidget(QLabel):
    def __init__(self, name ):
        super().__init__(name)
        self.setFixedHeight(24)
        self.setStyleSheet(Styles.className("nameLabel" , "chat.scss"))

class ChatIconWidget(QLabel) :
    def __init__(self, iconpath):
        super().__init__()
        # icon widget
        size = 48 

        img = QPixmap(iconpath)
        img = QPixmap(iconpath).scaled(size,size,Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.setPixmap(img)
        s = Styles.className("iconLabel" , "chat.scss")
        self.setStyleSheet(s)
    

class ChatNameAndMessageWidget(QWidget):
    def __init__(self, name,message):
        super().__init__()
        layout = QVBoxLayout()
        nameLabel = ChatNameWidget(name)
        messageLabel = ChatMessageArea(message )
        layout.addWidget(nameLabel)
        layout.addWidget(messageLabel)
        layout.addStretch()
        self.setLayout(layout)

class ChatMessageWidget(QWidget):
    def __init__(self, name,message,iconPath):
        super(ChatMessageWidget,self).__init__()
        chatLine = QHBoxLayout()
        chatIcon  = ChatIconWidget(iconPath)

        iconLayout = QVBoxLayout()
        iconLayout.addWidget(chatIcon)
        iconLayout.addStretch()

        nameAndMessage = ChatNameAndMessageWidget(name , message)
        chatLine.addLayout(iconLayout)
        chatLine.addWidget(nameAndMessage)
        self.setLayout(chatLine)


class TokenCountDisplayWidget(QWidget):
    def __init__(self):
        super(TokenCountDisplayWidget, self).__init__()
        layout = QHBoxLayout()
        self.label = QLabel("")
        self.setTokenCount(0)
        self.label.setStyleSheet(Styles.className("tokenCountLabel" , "chat.scss"))
        layout.addWidget(self.label)
        layout.addStretch()
        self.setLayout(layout)
    def setTokenCount(self,count):
        text = "TokenCount : " + str(count)
        self.label.setText(text)

class ChatView(QWidget):
    def __init__(self , nodescene):
        super().__init__()
        self.nodeScene = nodescene
        self.init_ui()

    def init_ui(self):
        # Create layout and widgets
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        self.chat_history = QVBoxLayout()

        logDeleteButton = QPushButton('clear log')
        logDeleteButton.clicked.connect(self.deleteLog)
        # set image
        garbageIcon = Util.getImageFilePath("garbage-icon-white.png")
        img = QPixmap(garbageIcon).scaled(48,48,Qt.KeepAspectRatio, Qt.SmoothTransformation)
        logDeleteButton.setIcon(QIcon(img))
        logDeleteButton.setStyleSheet(Styles.className("logDeleteButton" , "chat.scss"))
        # align left
        logDeleteButton.setFixedWidth(100)

        self.tokenCountDisplay =  TokenCountDisplayWidget()
        layout.addStretch()
        layout.addStretch()
        layout.addStretch()
        layout.addLayout(self.chat_history)

        # Create a QWidget to set the layout
        self.container = QWidget(self)
        self.container.setLayout(layout)
        self.container.setStyleSheet(Styles.className("chatContainer","chat.scss"))
        # Create a QScrollArea and set the widget
        self.scroll = QScrollArea(self)
        self.scroll.setWidget(self.container)
        self.scroll.setWidgetResizable(True)
        s = Styles.qClass("chatScrollArea","QScrollBar","chat.scss")
        self.scroll.setStyleSheet(s)
        # align top
        
        # スクロールエリアにウィジェットが追加されたとき、一番下にスクロールする
        self.scroll.verticalScrollBar().rangeChanged.connect(
            lambda min, max: self.scroll.verticalScrollBar().setValue(max))

        # Create a layout and add the scroll area
        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(self.scroll)
        
        # send buttonなど
        controllerLayout = QVBoxLayout()
        sendFormLayout = QHBoxLayout()
        self.chatSendFormWidget = QLineEdit()
        self.chatSendFormWidget.setStyleSheet(Styles.className("chatSendFormWidget","chat.scss"))
        self.chatSendButton = QPushButton('')
        # icon 
        sendIcon = Util.getImageFilePath("paperclaft.png")
        img = QPixmap(sendIcon).scaled(48,48,Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.chatSendButton.setIcon(QIcon(img))

        self.chatSendButton.clicked.connect(
            self.runTextInputNodes
        )
        self.chatSendButton.setStyleSheet(Styles.className("chatSendButton","chat.scss"))
        sendFormLayout.addWidget(self.chatSendFormWidget)
        sendFormLayout.addWidget(self.chatSendButton)
        # send on enter
        self.chatSendFormWidget.returnPressed.connect(
            self.runTextInputNodes
        )
        
        controllerButtonLayout = QHBoxLayout()
        controllerButtonLayout.addWidget(logDeleteButton)
        # controllerButtonLayout.addWidget(self.tokenCountDisplay)
        controllerLayout.addLayout(sendFormLayout)
        controllerLayout.addLayout(controllerButtonLayout)
        self.main_layout.addLayout(controllerLayout)

        self.setLayout(self.main_layout)


        # backgrround 0
        self.setStyleSheet(Styles.className("chatWindow","chat.scss"))
        
    
    def setTotalTokenCount(self , count):
        self.tokenCountDisplay.setTokenCount(count)
        

    def send_message(self , name , message , iconpath):
        from api.apis import tokenCount
        self.setTotalTokenCount(tokenCount)

        if not message:message = " "
        # max 100
        if self.chat_history.count() > 100:
            item = self.chat_history.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
        chatLinewidget = ChatMessageWidget(name,message,iconpath)
        chatLinewidget.setStyleSheet( Styles.className("chatLineWidget" , "chat.scss"))
        self.chat_history.addWidget(chatLinewidget)

    def runTextInputNodes(self):
        # textInputNodeを実行する
        nodescene :NodeScene= self.nodeScene
        nodeGraph = nodescene.nodeGraph

        textInputNodes = nodeGraph.findNodesByType("TextInputNode")
        if len(textInputNodes) == 0:
            return
        message = self.chatSendFormWidget.text()
        textInputNodes[0].onInput(data=message)
        # clear text
        self.chatSendFormWidget.setText("")

    def deleteLog(self):
        # delete all chat history
        while self.chat_history.count():
            item = self.chat_history.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()