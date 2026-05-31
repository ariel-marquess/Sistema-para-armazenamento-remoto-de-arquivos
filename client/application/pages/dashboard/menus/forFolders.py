import customtkinter as ctk

import client.application.utils.ul as util
import client.application.pages.dashboard.menus.createFolder as cfolder
import client.application.pages.dashboard.menus.common.cmn as common

class menuFolder(ctk.CTkFrame):
    def __init__(self, master, currentSession, menu, event, currentPath=None):
        super().__init__(master)

        # Estilos do texto
        self.textFont = util.font(14)
        self.textColor = "white"

        # Métodos que serão utilizados posteriormente
        self.createFolder = cfolder.CreateFolder

        self.configure(fg_color="#393939", corner_radius=10, border_width=1, width=100)
        self.columnconfigure(0, weight=1)

        createFolder = ctk.CTkButton(self, text="Criar pasta", anchor="w", fg_color="transparent", font=self.textFont, text_color=self.textColor,
                command=lambda m=self.master, cs=currentSession, p=currentPath: self.create(menu, [m, cs, p]))
        createFolder.grid(row=0, column=0, padx=10, pady=5, sticky="w")

        canceler = ctk.CTkButton(self, text="Cancelar", anchor="w", fg_color="transparent", font=self.textFont, text_color=self.textColor, command=lambda: self.destroy())
        canceler.grid(row=3, column=0, padx=10, pady=5, sticky="w")

        common.center_menu(self.master, self, event)

    def create(self, dashboard, currentSession, currentPath):
        # Cria a janela CreateFolder, passando o Dashboard como master
        cfolder.CreateFolder(dashboard, currentSession, currentPath)
        self.destroy()
