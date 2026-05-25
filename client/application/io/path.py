import os

class Path:
    def __init__(self, path):
        setPath(path)
        setRootPath(path)

        self.lastPath = []
        self.lastPath.append(path)

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

    def addLastPath(self, path):
        if len(self.lastPath) >= 5:
            self.lastPath.pop(0)

        self.lastPath.append(path)