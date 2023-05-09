import os

from utils.fileLoader import FileLoader


class CSound:
    isMute = False
    resourcepath = FileLoader.soundPath
    def play(src):
        if(CSound.isMute): return 
        soundpath = os.path.join(CSound.resourcepath , src)
        sound = FileLoader.getResource(soundpath)

        try : sound.play()
        except : pass