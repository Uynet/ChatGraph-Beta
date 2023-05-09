from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import (QHBoxLayout, QLabel, QPushButton, QScrollArea,
                             QSizePolicy, QTextEdit, QVBoxLayout, QWidget)

from debug.debugCommand import DebuggerCommand
from utils.styles import Styles
from utils.util import Util


class DebuggerMessageArea(QTextEdit):
    def __init__(self,message,maxwidth):
        super().__init__(message)
        self.textChanged.connect(self.adjust_size)
        s = Styles.className("messageLabel")
        s = s.replace('"$maxWidth"',str(maxwidth)+"px")
        
        self.setStyleSheet(s)
        self.setReadOnly(True)
        self.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Minimum)

    def showEvent(self, event):
        super().showEvent(event)
        # ウィジェットが表示される直前にadjust_sizeを呼び出す
        self.adjust_size()

    def adjust_size(self):
        document_height = self.document().size().height()
        pad = 30
        self.setFixedHeight(document_height + pad)


        

class DebuggerNameWidget(QLabel):
    def __init__(self, name ):
        super(DebuggerNameWidget, self).__init__(name)
        self.setFixedHeight(24)
        self.setStyleSheet(Styles.className("nameLabel"))

class DebuggerIconWidget(QLabel) :
    def __init__(self, iconpath):
        super(DebuggerIconWidget, self).__init__()
        # icon widget
        size = 48 

        img = QPixmap(iconpath)
        img = QPixmap(iconpath).scaled(size,size,Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.setPixmap(img)
        s = Styles.className("iconLabel", "chat.scss")
        self.setStyleSheet(s)
    

class DebuggerNameAndMessageWidget(QWidget):
    def __init__(self, name,message):
        super(QWidget, self).__init__()
        maxwidth = str(self.width() )
        layout = QVBoxLayout()
        nameLabel = DebuggerNameWidget(name)
        messageLabel = DebuggerMessageArea(message , maxwidth)
        layout.addWidget(nameLabel)
        layout.addWidget(messageLabel)
        layout.addStretch()
        self.setLayout(layout)

class DebuggerMessageWidget(QWidget):
    def __init__(self, name,message,iconPath):
        super(DebuggerMessageWidget, self).__init__()
        chatLine = QHBoxLayout()
        chatIcon  = DebuggerIconWidget(iconPath)

        iconLayout = QVBoxLayout()
        iconLayout.addWidget(chatIcon)
        iconLayout.addStretch()

        nameAndMessage = DebuggerNameAndMessageWidget(name , message)
        chatLine.addLayout(iconLayout)
        chatLine.addWidget(nameAndMessage)
        chatLine.addStretch()
        self.setLayout(chatLine)

class TokenCountDisplayWidget(QWidget):
    def __init__(self):
        super(TokenCountDisplayWidget, self).__init__()
        layout = QHBoxLayout()
        self.label = QLabel("")
        self.setTokenCount(0)
        self.label.setStyleSheet(Styles.className("tokenCountLabel"))
        layout.addWidget(self.label)
        layout.addStretch()
        self.setLayout(layout)
    def setTokenCount(self,count):
        text = "TokenCount : " + str(count)
        self.label.setText(text)

class DebuggerView(QWidget):
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
        from utils.util import Util
        garbageIcon = Util.getImageFilePath("garbage-icon-white.png")
        img = QPixmap(garbageIcon).scaled(48,48,Qt.KeepAspectRatio, Qt.SmoothTransformation)
        logDeleteButton.setIcon(QIcon(img))
        logDeleteButton.setStyleSheet(Styles.className("logDeleteButton"))
        # align left
        logDeleteButton.setFixedWidth(100)

        self.tokenCountDisplay =  TokenCountDisplayWidget()
        layout.addLayout(self.chat_history)
    
        # from PyQt5.uic import loadUi
        # testUI = loadUi("resources/widgets/2.ui")
        # layout.addWidget(testUI)
        # layout.addStretch()

        # Create a QWidget to set the layout
        self.container = QWidget(self)
        self.container.setLayout(layout)
        self.container.setStyleSheet(Styles.className("chatContainer"))

        # Create a QScrollArea and set the widget
        self.scroll = QScrollArea(self)
        self.scroll.setWidget(self.container)
        self.scroll.setWidgetResizable(True)
        s = Styles.classNameAndGizyoso("chatScrollArea")
        self.scroll.setStyleSheet(s)
        
        # スクロールエリアにウィジェットが追加されたとき、一番下にスクロールする
        self.scroll.verticalScrollBar().rangeChanged.connect(
            lambda min, max: self.scroll.verticalScrollBar().setValue(max))
         

        # Create a layout and add the scroll area
        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(self.scroll)
        
        # send buttonなど
        controllerLayout = QVBoxLayout()
        sendFormLayout = QHBoxLayout()
        from PyQt5.QtWidgets import QLineEdit
        self.chatSendFormWidget = QLineEdit()
        self.chatSendFormWidget.setStyleSheet(Styles.className("chatSendFormWidget"))
        self.chatSendButton = QPushButton('Send')
        self.chatSendButton.clicked.connect(
            self.onEnterPressed
        )
        self.chatSendButton.setStyleSheet(Styles.className("chatSendButton"))
        sendFormLayout.addWidget(self.chatSendFormWidget)
        sendFormLayout.addWidget(self.chatSendButton)
        # send on enter but shift + enter is new line
        self.chatSendFormWidget.returnPressed.connect(self.onEnterPressed)
         
        
        controllerButtonLayout = QHBoxLayout()
        controllerButtonLayout.addWidget(logDeleteButton)
        controllerButtonLayout.addWidget(self.tokenCountDisplay)
        controllerLayout.addLayout(sendFormLayout)
        controllerLayout.addLayout(controllerButtonLayout)
        self.main_layout.addLayout(controllerLayout)

        self.setLayout(self.main_layout)


        # backgrround 0
        self.setStyleSheet(Styles.className("chatWindow"))
        
    
    def setTotalTokenCount(self , count):
        self.tokenCountDisplay.setTokenCount(count)
        

    def send_message(self , name , message , iconpath):
        from api.apis import tokenCount
        self.setTotalTokenCount(tokenCount)
        if message:
            chatLinewidget = DebuggerMessageWidget(name,message,iconpath)
            chatLinewidget.setStyleSheet( Styles.className("chatLineWidget"))
            self.chat_history.addWidget(chatLinewidget)

    def onEnterPressed(self):
        # if shift + enter is pressed , new line
        from graph import qtApp
        if qtApp.keyboardModifiers() == Qt.ShiftModifier:
            return
        # send message
        message = self.chatSendFormWidget.text()
        value = DebuggerCommand.repl(message,self)
        sysIcon= Util.getImageFilePath("GPTGraph.png") 
        self.send_message("system" , str(value) ,sysIcon) 
        self.chatSendFormWidget.setText("")

    def deleteLog(self):
        # delete all chat history
        while self.chat_history.count():
            item = self.chat_history.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()