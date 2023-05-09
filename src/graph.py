import os
import sys
from editors.controllers.actions.cgpAction import CgpAction

from editors.models.serializer import Serializer

# プロジェクトのsrcフォルダへのパスを取得
src_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src')

# srcフォルダをsys.pathに追加
if src_dir not in sys.path:
    sys.path.append(src_dir)

block_cipher = None
import hupper
import PyQt5.QtGui
from dotenv import load_dotenv
from PyQt5.QtWidgets import QApplication

from layout.mainWindow import MainWindow
from layout.splashScreen import SplashScreen
from utils.fileLoader import FileLoader
from utils.util import Util

if getattr(sys, 'frozen', False):
    # PyInstallerでビルドされた実行可能ファイルの場合
    base_dir = sys._MEIPASS
else:
    # 開発環境の場合
    base_dir = os.path.dirname(os.path.abspath(__file__))

src_dir = os.path.join(base_dir, "src")
sys.path.insert(0, src_dir)

qtApp = QApplication(sys.argv)
# 初回起動時にAPIキーを入力させる
def initialSetup(mainwindow):
    # open settings-tab
    mainwindow.goAPIKeySetting()

    # set-config
    config = Util.readConfig()
    config.set('Initial', 'isInitialBoot', 'False')
    config.set('APIKEY', 'openaiKey', '')
    Util.writeConfig(config)

def preLoad():
    # 初期設定ファイルを読み込む
    Util.validateConfig()
    FileLoader.preloadAll()

def openDefaultGraph(mainwindow):
    if os.environ.get('ENV') == 'DEV':
        filePath = "resources/nodes/debug.json"
    else: filePath = Util.getDefaultFilePath()
    data = FileLoader.loadGraphData(filePath)
    if data == None:
        mainwindow.onError("ERROR", f"File not found: {filePath}")
        return
    ngc = mainwindow.nodeScene.nodeGraph.getController()
    graph = Serializer.dataToGraph(data)
    addGraphAction = CgpAction.ADD_GRAPH(graph)
    ngc.onCgpAction(addGraphAction)

def main():
    # ロード時のロゴを表示
    splash = SplashScreen()
    splash.show()
    qtApp.processEvents()

    preLoad()
    config = Util.readConfig()
    mainwindow= MainWindow()
    openDefaultGraph(mainwindow)
    splash.close()

    # set-title
    mainwindow.setWindowTitle("ChatGraph")
    # set icon
    icon = PyQt5.QtGui.QIcon()
    iconPath = Util.getImageFilePath("ChatGraph.png")
    icon.addPixmap(PyQt5.QtGui.QPixmap(iconPath), PyQt5.QtGui.QIcon.Normal, PyQt5.QtGui.QIcon.Off)
    mainwindow.setWindowIcon(icon)
    # フレームを消す
    # mainwindow.setWindowFlags(PyQt5.QtCore.Qt.FramelessWindowHint)
    mainwindow.show()

    # アプリのアイコンを指定
    qtApp.setWindowIcon(PyQt5.QtGui.QIcon(iconPath))
                    
    isInitialBoot = config.get('Initial', 'isInitialBoot')
    if isInitialBoot == "True" :
        initialSetup(mainwindow)
    isApiKeyValid = Util.validateConfig()
    if isApiKeyValid == False : 
        initialSetup(mainwindow)
    # apiキーを環境変数にセット
    apikey = config.get("APIKEY", "openaiKey")
    os.environ["OPENAI_API_KEY"] = apikey

    try:
        sys.exit(qtApp.exec_())
    except KeyboardInterrupt:
        print("KeyboardInterrupt")
        sys.exit(0)

if __name__ == "__main__":
    load_dotenv()
    if os.environ.get('ENV') == 'DEV':
        reloader = hupper.start_reloader('graph.main')
        pass
    # 本番
    elif os.environ.get('ENV') == 'PROD':
        pass
    else: 
        from utils.util import Console
        Console.warn("unknown ENV:", os.environ.get('ENV'))
    main()