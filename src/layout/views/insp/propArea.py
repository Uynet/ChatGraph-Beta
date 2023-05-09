from PyQt5.QtWidgets import QLabel, QVBoxLayout, QWidget

from editors.types.dataType import NodeProperty
from layout.views.insp.checkBox import InspectorPropertyCheckBox
from layout.views.insp.inepectorPropertyList import InspectorPropertyList
from layout.views.insp.inspectorProperty import InspectorProperty
from utils.util import Console


#　1行文
class propArea(QWidget):
    def __init__(self , prop:NodeProperty,node,isList =False):
        super(QWidget, self).__init__()
        self.name = prop.name 
        nameLabel = QLabel(self.name)
        layout = QVBoxLayout()
        value = prop.value
        if value == None: value = ""
        valueType = type(value)
        if not valueType in { str , list , bool , float ,int}:
            value = str(value)

        if(valueType == str):self.textField = InspectorProperty(self.name,value,node)
        elif valueType == float: self.textField = InspectorProperty(self.name,str(value),node)
        elif valueType == int : self.textField = InspectorProperty(self.name,str(value),node)
        elif valueType == list: self.textField = InspectorPropertyList(self.name,value,node)
        elif valueType == bool: self.textField = InspectorPropertyCheckBox(self.name,value,node)
        else :Console.error("not supported type",valueType)
        layout.addWidget(nameLabel)
        layout.addWidget(self.textField)
        self.setLayout(layout)

    def update(self , value):
        self.value = value
        self.textField.onChangeProperty(value)
        return