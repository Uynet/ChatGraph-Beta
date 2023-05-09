# GUI全体のイベントを管理する
class MainWindowController:
    __instance = None
    __mainWindow = None
    # singleton
    def __new__(cls , mainwindow):
        if cls.__instance is None:
            cls.__mainWindow = mainwindow
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def getInstance():
        return MainWindowController.__instance

    def getMainWindow():
        return MainWindowController.__mainWindow

    def onChangeNodeProperty(self,nodeModel , name,value):
        inspector = MainWindowController.__mainWindow.getInspectorView()
        inspector.updateByData(nodeModel , name , value)

    # 選択によってinspectorを変更する
    def setInspectorItem(self,nodeModel):
        inspector = MainWindowController.__mainWindow.getInspectorView()
        inspector.setItem(nodeModel)

    def onMousePress(self,event):
        MainWindowController.setInspectorItem()

    def onMouseRelease(self,event):
        MainWindowController.setInspectorItem()

    def sendToChat(self, name ,answer , icon):
        MainWindowController.__mainWindow.sendToChat( name ,answer , icon)

    def onError(self , state  , answer):
        MainWindowController.__mainWindow.onError( state , answer )

    def addThread(self, thread):
        MainWindowController.__mainWindow.addThread(thread)

    # シーンを消去して再読み込み 
    def reload(self ):
        MainWindowController.__mainWindow.reload()

    ##############
    # WINDOW DRAG
    ##############

    def onWindowDrag(self,event):
        # dummy
        pass