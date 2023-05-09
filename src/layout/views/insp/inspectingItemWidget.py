from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QVBoxLayout, QWidget

from editors.models.nodes.nodeModel import NodeModel
from editors.types.dataType import NodeProperty
from layout.views.insp.propArea import propArea
from utils.styles import Styles


class InspectorIconWidget(QLabel) :
    def __init__(self, iconpath):
        super(InspectorIconWidget, self).__init__()
        size = 48 

        img = QPixmap(iconpath)
        img = QPixmap(iconpath).scaled(size,size,Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.setPixmap(img)
        s = Styles.className("iconLabel","chat.scss")
        self.setStyleSheet(s)
    def resetIcon(self, iconpath):
        size = 48 
        img = QPixmap(iconpath)
        img = QPixmap(iconpath).scaled(size,size,Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.setPixmap(img)


# 表示中のやつ
class InspectingItemWidget(QWidget):
    def __init__(self , scene):
        super(QWidget, self).__init__()
        self.nodeScene = scene
        self.inspectingItem = None
        layout = QVBoxLayout()
        nameAndIconLayout = QHBoxLayout()
        nameAndIconLayout.setContentsMargins(0, 0, 0, 0)
        # text
        self.text = QLabel("No Selected")
        self.text.setStyleSheet(Styles.className("inspectingItemLabel","inspector.scss"))
        self.icon = InspectorIconWidget("resources/icons/default.png")
        nameAndIconLayout.addWidget(self.icon)
        nameAndIconLayout.addWidget(self.text)
        nameAndIconLayout.addStretch()
        nameWidget = QWidget()
        nameWidget.setLayout(nameAndIconLayout)
        nameWidget.setFixedHeight(48)
        
        layout.addWidget(nameWidget)
        self.propertiesLayout = QVBoxLayout()
        self.propertyWidgets = []
        layout.addLayout(self.propertiesLayout)
        self.setStyleSheet(Styles.className("inspectingItemWidget","inspector.scss"))
        self.setLayout(layout)

    def setPropertyView(self,nodeData : NodeProperty):
        widgets:list[QWidget] = []
        customProps = nodeData.getProps("custom")
        baseProps:list[NodeProperty] = nodeData.getProps("base")
        tranforms :list[NodeProperty] = nodeData.getProps("transform")
        historyProps:list[NodeProperty] = nodeData.getProps("history")
        node = self.inspectingItem

        for prop in baseProps:
            widgets.append(propArea(prop,node))

        # for prop in tranforms:
        #     widgets.append(propArea(prop,node))

        for prop in customProps:
            widgets.append(propArea(prop,node))

        for prop in historyProps:
            widgets.append(propArea(prop,node,isList=True))
        return widgets

    def clearLayout(self, layout):
        # clear props
        for widget in self.propertyWidgets:
            widget : QWidget
            widget.deleteLater()
        self.propertyWidgets = []
        self.layout().removeItem(self.propertiesLayout)
        self.propertiesLayout = QVBoxLayout()
        self.layout().addLayout(self.propertiesLayout)

    # 現在表示中のアイテムを更新するのみで、変更はしない
    def update(self):
        item  = self.inspectingItem 
        self.setItem(item)


    # 更新されたpropertyのみを通知する
    def updateByData( self , nodeModel , name , value):
        if self.inspectingItem is not nodeModel: return

        # self.propertyWidgets から name と一致するものを探す
        for widget in self.propertyWidgets:
            widget : propArea
            if widget.name == name:
                widget.update(value)
                return

    def getItem(self):
        return self.inspectingItem

    def setItemData(self , nodeData : NodeProperty):
        self.clearLayout(self.propertiesLayout)
        self.text.setText(nodeData.get("label"))
        self.icon.resetIcon( nodeData.get("icon") )
        self.propertyWidgets = self.setPropertyView(nodeData)
        for widget in self.propertyWidgets:
            # 上揃えに
            self.propertiesLayout.addWidget(widget) 
        self.propertiesLayout.addStretch()    
        self.propertiesLayout.addStretch()    

    def setItem(self , item : NodeModel):
        if self.inspectingItem == item : return
        self.inspectingItem = item 
        if item is None :return
        nodeData:NodeProperty = item.nodeData
        self.setItemData(nodeData)