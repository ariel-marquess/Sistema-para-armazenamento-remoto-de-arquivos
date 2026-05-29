import customtkinter as ctk

from client.application.io.path import Path
import client.application.controls.ctrl as ctrl
import client.application.pages.dashboard.sessions.rootFolders as rfolder


class Dashboard(ctk.CTkFrame):
    def __init__(self, master, content, rootPath):
        super().__init__(master)

        self.configure(fg_color="#252525")
        self.grid(row=1, column=0, sticky="nsew")

        # Configurando as colunas da página
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1, minsize=190)
        self.grid_columnconfigure(2, weight=1, minsize=190)
        self.grid_columnconfigure(3, weight=1, minsize=190)

        # Configurando linhas da página
        self.rowconfigure(0, weight=1)

        # Iniciando instancia para manipulação dos caminhos do servidor
        self.objPath = Path(rootPath)

        # Criando as seções da página
        ctrl.openFolder(self, self.objPath)
        rfolder.RootFolders(self, content, self.objPath)