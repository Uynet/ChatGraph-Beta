import os

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import (QFormLayout, QGraphicsScene, QGraphicsView,
                             QHBoxLayout, QLabel, QLineEdit, QPushButton,
                             QSizePolicy, QVBoxLayout, QWidget)

from api.apis import validateAPIKey
from utils.styles import Styles
from utils.util import Util


class Style:
    title = """
        .QLabel {
            margin:32px;
            font-size: 33px;
            font-weight: bold;
            font-family:Inter;
            letter-spacing: 1.5px;
            color:white;
        }
        """
    note = """
        .QLabel {
            margin:24px;
            font-size: 14px;
            font-family:Inter;
            letter-spacing: 1.5px;
            color:white;
        }
        """
    button = """   
        .QPushButton {
            height: 30px;
            font-size: 14px;
            font-weight: bold;
            font-family:"Inter";
            letter-spacing: 1.5px;
            border-radius: 50%;
            border: 1px solid #333344;
            background-color: #000000;
            color: white;
        }"""
    form = """
        .QLineEdit {
            padding-left: 15px;
            height: 30px;
            font-size: 14px;
            font-family:"Inter";
            letter-spacing: 1.5px;
            border-radius: 5px;
            border: 1px solid #333344;
            background-color: #333344;
            color: #d2d2d2;
        }"""

    def statusLogStyle( color):
        return """
            .QLabel {
                font-size: 13px;
                margin:48px;
                color: """ + color + """;
                font-family:"Inter";
                letter-spacing: 1.5px;
            }
            """


class SettingView(QGraphicsView):
    def setState(self, state):
        # 0: default
        if state == "0":
            self.statusLog.setText("key is not set ")
            self.statusLog.setStyleSheet(Style.statusLogStyle("#ffff00"))

        # 1: success
        elif state == "1":
            self.statusLog.setText("OK")
            self.statusLog.setStyleSheet(Style.statusLogStyle("#00ff00"))

        # 2: error
        elif state == "2":
            self.statusLog.setText("ERORR: INVALID API KEY")
            self.statusLog.setStyleSheet(Style.statusLogStyle("#ff0000"))


    def __init__(self , mainWindow) :
        super().__init__()

        self.mainWindow = mainWindow
        self.resize(800, 600)
        self.setRenderHint(QPainter.Antialiasing)
        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
        self.settingScene = QGraphicsScene()
        self.setScene(self.settingScene)

        self.contentWidget = QWidget()
        self.contentWidget.setStyleSheet("background-color: #232228;")

        self.content = QVBoxLayout()
        self.title = QLabel("API Settings")
        self.title.setStyleSheet(Style.title)
        self.title.setAlignment(Qt.AlignCenter)
        self.note = QLabel("Please enter your API key for OpenAI GPT-3.")
        self.note.setStyleSheet(Style.note)
        self.note.setAlignment(Qt.AlignCenter)

        self.statusLog = QLabel("") 
        self.statusLog.setStyleSheet(Style.statusLogStyle("#d2d2d2"))
        self.statusLog.setAlignment(Qt.AlignCenter)

        self.formlayout = QHBoxLayout()
        self.apiform = QLineEdit("")
        self.setbutton = QPushButton("set")
        self.setbutton.setStyleSheet(Style.button)
        self.setbutton.setFixedWidth(70)
        self.apiform.setStyleSheet(Style.form)
        self.setAPIKeyForm()
        # self.apiform.setFixedWidth(300)
        self.formlayout.addWidget(self.apiform)
        self.formlayout.addWidget(self.setbutton)

        self.content.addWidget(self.title)
        self.content.addWidget(self.note)
        # self.content.addWidget(self.formWidget)
        self.content.addLayout(self.formlayout)
        self.content.addWidget(self.statusLog)
        nextButton = QPushButton("go Editor")
        nextButton.setStyleSheet(Styles.className("nextButton"))
        nextButton.setFixedWidth(100)
        nextButton.clicked.connect(mainWindow.goEditor)
        self.content.addWidget(nextButton)

        self.contentWidget.setLayout(self.content)
        self.settingScene.addWidget(self.contentWidget)
        self.setbutton.clicked.connect(self.setKey)


        font = self.font()
        font.setPointSize(13)
        font.setBold(True)
        font.setFamily("courier")
        # font color
        self.setStyleSheet("color: #ffffff;")
        self.setFont(font)

    def setAPIKeyForm(self ):
        config = Util.readConfig() 
        apikey = config.get("APIKEY", "openaiKey")
        self.apiform.setText(apikey)
        self.setKey()

    def setKey(self):
        key = self.apiform.text()
        if (key == ""):
            self.statusLog.setText("key is not set ")
            self.statusLog.setStyleSheet(Style.statusLogStyle("#ffff00"))
            return
        response, error = validateAPIKey(key)
        if response:
            config = Util.readConfig()
            config.set('APIKEY', 'openaiKey', key)
            os.environ["OPENAI_API_KEY"] = key
            Util.writeConfig(config)
            self.statusLog.setText("OK")
            self.statusLog.setStyleSheet(Style.statusLogStyle("#00ff00"))
            # statulLogの描画から1秒後にメイン画面に戻る
            mainWindow = self.mainWindow
            self.statusLog.objectNameChanged.connect(mainWindow.goEditor)
            

        else:
            self.statusLog.setText("ERORR: INVALID API KEY")
            self.statusLog.setStyleSheet(Style.statusLogStyle("#ff0000"))