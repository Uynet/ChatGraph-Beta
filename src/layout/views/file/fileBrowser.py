from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (QHBoxLayout, QLabel, QListWidget, QListWidgetItem,
                             QSizePolicy, QTextEdit, QVBoxLayout, QWidget)

from editors.models.nodes.nodeModel import NodeModel
from editors.types.dataType import NodeProperty
from utils.fileLoader import FileLoader
from utils.styles import Styles


# アイコン画像とファイル名
class FileItemWidget(QListWidgetItem):
    def __init__(self , fileName:str):
        super(QWidget, self).__init__()
        layout = QHBoxLayout()
        name = QLabel( fileName )
        layout.addWidget(name)
        self.setLayout(layout)
        self.setStyleSheet(Styles.className("fileItem" , "fileBrowser.scss"))

    def genJsonItem(self):
        pass

class FileBrowserWidget(QWidget):
    def __init__(self, filePath: str):
        super(QWidget, self).__init__()
        data = FileLoader.browse(filePath)
        files = data.get("files")
        folders = data.get("folders")

        self.listWidget = QListWidget()
        # self.listWidget.setStyleSheet(Styles.className("QListWidget" , "fileBrowser.scss"))
        self.listWidget.setStyleSheet("""
            QListWidget {
                background-color: #191721;
            }
            QListWidget::item {
                padding: 5px;
                border: 1px solid #555;
                border-radius: 5px;
                color: #cccccc;
            }
            QListWidget::item:hover {
                background-color: #333344;
            }
        """)

        for folder in folders:
            filename = folder.split("\\")[-1]
            filename = " [ " + filename + " ] "
            item = QListWidgetItem(filename)
            self.listWidget.addItem(item)

        for filepath in files:
            filename = filepath.split("\\")[-1]
            item = QListWidgetItem(filename)
            self.listWidget.addItem(item)

        layout = QVBoxLayout()
        layout.addWidget(self.listWidget)
        self.setLayout(layout)

