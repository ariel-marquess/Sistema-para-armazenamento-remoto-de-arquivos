import customtkinter as ctk

import client.application.pages.dashboard.sessions.rootFolders as rootFolder
import client.application.pages.dashboard.sessions.descriptionFolders as descriptionFolder


class Dashboard(ctk.CTkFrame):
    def __init__(self, master, content):
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

        # Criando as seções da página
        rootFolder.RootFolders(self, content)
        descriptionFolder.Folders(self, content)
