import customtkinter as ctk

import client.application.pages.dashboard.sessions.rootFolders as rfolder
import client.application.pages.dashboard.sessions.descriptionFolders as dfolder
from client.application.io.path import Path
import client.protocols.open_data as open_data

class Dashboard(ctk.CTkFrame):
    def __init__(self, master, session_data):
        super().__init__(master)

        self.username = session_data.get("username")
        initial_content = session_data.get("content")

        self.configure(fg_color="#252525")
        self.grid(row=1, column=0, sticky="nsew")
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1, minsize=190)
        self.grid_columnconfigure(2, weight=1, minsize=190)
        self.grid_columnconfigure(3, weight=1, minsize=190)
        self.rowconfigure(0, weight=1)

        self.objPath = Path("")
        
        # Armazena referências às sessões para poder destruí-las
        self.root_folder_session = None
        self.description_session = None

        self.create_sessions(initial_content)

    def create_sessions(self, content):
        """Destrói as sessões antigas e cria novas com o conteúdo atualizado."""
        if self.root_folder_session:
            self.root_folder_session.destroy()
        if self.description_session:
            self.description_session.destroy()
            
        self.root_folder_session = rfolder.RootFolders(self, content, self.objPath)
        self.description_session = dfolder.Folders(self, content, self.objPath)

    def navigate_to_current_path(self):
        """
        Método central para navegação. Busca o conteúdo do caminho atual no objPath
        e recria as sessões da interface para exibir o novo conteúdo.
        """
        path = self.objPath.get_current_path()
        content = open_data.openFolder(self.username, path)
        if content:
            self.create_sessions(content)

    def get_username(self):
        """Método para que outras partes da UI possam acessar o username logado."""
        return self.username
