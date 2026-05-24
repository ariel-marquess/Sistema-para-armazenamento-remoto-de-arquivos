import customtkinter as ctk

import client.application.utils.ul as util
import client.application.controls.ctrl as ctrl
import client.application.pages.dashboard.menus.createFolder as cfolder
import client.application.pages.dashboard.menus.common.cmn as common

class menuFolder(ctk.CTkFrame):
    def __init__(self, master, currentSession, menu, event, path=None):
        super().__init__(master)

        # Métodos que serão utilizados posteriormente
        self.createFolder = cfolder.CreateFolder

        self.configure(fg_color="#393939", corner_radius=10, border_width=1, width=100)
        self.columnconfigure(0, weight=1)

        createFolder = ctk.CTkButton(self, text="Criar pasta", anchor="w", fg_color="transparent",
                command=lambda m=self.master, cs=currentSession, p=path: self.create(menu, [m, cs, p]))
        createFolder.grid(row=0, column=0, padx=10, pady=5, sticky="w")

        canceler = ctk.CTkButton(self, text="Cancelar", anchor="w", fg_color="transparent", command=lambda: self.destroy())
        canceler.grid(row=3, column=0, padx=10, pady=5, sticky="w")

        common.center_menu(self.master, self, event)

    def create(self, menu, args):
        menu = self.createFolder(*args)
        self.destroy()