import customtkinter as ctk

import client.application.pages.dashboard.menus.createFolder as cfolder
import client.application.pages.dashboard.menus.common.cmn as common

class menuFolder(ctk.CTkFrame):
    def __init__(self, master, currentSession, menu, event, currentPath=None):
        # master aqui é o Dashboard
        super().__init__(master) 

        self.configure(fg_color="#393939", corner_radius=10, border_width=1, width=100)
        self.columnconfigure(0, weight=1)

        # Passa o master (Dashboard) para o comando de criação
        createFolder = ctk.CTkButton(self, text="Criar pasta", anchor="w", fg_color="transparent",
                command=lambda: self.create(master, currentSession, currentPath))
        createFolder.grid(row=0, column=0, padx=10, pady=5, sticky="w")

        canceler = ctk.CTkButton(self, text="Cancelar", anchor="w", fg_color="transparent", command=lambda: self.destroy())
        canceler.grid(row=3, column=0, padx=10, pady=5, sticky="w")

        common.center_menu(self.master, self, event)

    def create(self, dashboard, currentSession, currentPath):
        # Cria a janela CreateFolder, passando o Dashboard como master
        cfolder.CreateFolder(dashboard, currentSession, currentPath)
        self.destroy()
