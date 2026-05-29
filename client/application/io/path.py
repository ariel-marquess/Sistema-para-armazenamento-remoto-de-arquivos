import os

import client.application.utils.ul as util

class Path:
    def __init__(self, path):
        setPath(path)
        setRootPath(path)

    def getPath(self):
        return self.currentPath

    def setPath(self, path):
        self.currentPath = path

    def getRootPath(self):
        return self.rootPath

    def setRootPath(self, path):
        self.rootPath = path

    def join(self, args: str):
        for arg in args:
            setPath(os.path.join(getPath(), arg))

    def joinRoot(self, args: str):
        for arg in args:
            setPath(os.path.join(getRootPath(), arg))

    def splitext(self):
        base, ext = os.path.splitext(getPath())
        return False if ext == "" else True

    def back(self):
        if getPath() != getRootPath():
            currentPath, lastDiretory = os.path.split(getPath())
            setPath(currentPath)
        else:
            util.MessageBox(
                title="Você está na pasta raiz",
                message="ERRO: você está no diretório inicial do seu repositório, a partir daqui não há mais como voltar.",
                icon="warning"
            )