from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QFont, QTextCursor
from PyQt5.QtWidgets import QGraphicsTextItem

from editors.types.dataType import NodeViewData
from utils.styles import Styles


# QGraphicsItemではCSSが使えないため、それっぽくしているだけ
class WindowFlameLabel(QGraphicsTextItem):
    def __init__(self, text , nodeModel ,nodeWindow):
        super().__init__(text , nodeWindow)
        self.nodeModel = nodeModel 
        left = Styles.getNodeWindowStyle("left")
        top = Styles.getNodeWindowStyle("top")
        self.setPos(int(left) , int(top))
        color = QColor(Styles.getColor("windowFlameLabel"))
        self.setDefaultTextColor(color)
        self.setParentItem(nodeWindow)
        font = QFont(Styles.getNodeWindowStyle("font-family"))
        font.setPointSize( float(Styles.getNodeWindowStyle("font-size")))
        font.setLetterSpacing(QFont.AbsoluteSpacing , float(Styles.getNodeWindowStyle("letter-spacing")))
        font.setBold(True)
        # color
        # font css
        self.setFont(font)

    def initProperties(self , nodeData:NodeViewData):
        text = nodeData.get("label")
        self.setPlainText(text)

    def updateView(self):
        self.setPlainText(self.nodeModel.getProperty("label"))

    def keyPressEvent(self, event):
        cursor = self.textCursor()

        if event.key() == Qt.Key_Left:
            cursor.movePosition(QTextCursor.Left)
        elif event.key() == Qt.Key_Right:
            cursor.movePosition(QTextCursor.Right)
        else:
            super().keyPressEvent(event)

        self.setTextCursor(cursor)
    
    def getCgpView(self):
        return self.parent()