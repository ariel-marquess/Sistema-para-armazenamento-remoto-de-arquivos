import customtkinter as ctk

import client.application.controls.ctrl as ctrl
import client.application.utils.ul as util
import client.application.pages.dashboard.menus.common.cmn as common

class CreateFolder(ctk.CTkFrame):
    def __init__(self, master, currentSession, objPath):
        # master aqui é o Dashboard
        super().__init__(master)
        self.dashboard = master 
        self.currentSession = currentSession
        self.objPath = objPath

        # Estilos do texto
        self.textColor = "white"

        self.configure(fg_color="#393939", corner_radius=10, border_width=1, width=400)
        self.columnconfigure(0, minsize=400)

        self.title = ctk.CTkLabel(self, text="Nova pasta", fg_color="transparent", font=util.font(15), text_color=self.textColor)
        self.title.grid(row=0, column=0, pady=5, sticky="ew")

        self.entry = ctk.CTkEntry(self, placeholder_text="Digite o nome da pasta...")
        self.entry.grid(row=1, column=0, padx=10, pady=5, sticky="ew")
        self.entry.bind("<Return>", lambda: self.actionClick())

        self.container_buttons = ctk.CTkFrame(self, fg_color="transparent")
        self.container_buttons.grid(row=2, column=0, pady=5)

        self.canceler = ctk.CTkButton(self.container_buttons, text="Cancelar", fg_color="#2b2f76", width=0, height=0, command=self.destroy)
        self.canceler.grid(row=0, column=0, padx=5)

        self.create = ctk.CTkButton(self.container_buttons, text="Criar pasta", fg_color="#2b2f76", width=0, height=0,
                                     command=self.actionClick)
        self.create.grid(row=0, column=1, padx=5)

        common.center_menu(self.master, self)

    def actionClick(self):
        folder_name = self.entry.get()
        username = self.dashboard.get_username() # Usa a referência correta para o Dashboard

        if folder_name != "":
            if ctrl.createFolder(username, self.objPath.get_current_path(), folder_name):
                # Se a criação for bem-sucedida, atualiza a visualização
                ctrl.openFolder(self.dashboard, self.currentSession, username, self.objPath)
            self.destroy()
        else:
            self.entry.focus()
            self.entry.configure(fg_color="#a24242")
