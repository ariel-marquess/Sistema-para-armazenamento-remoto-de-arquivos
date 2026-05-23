import customtkinter as ctk

import client.application.controls.ctrl as ctrl
import client.application.pages.dashboard.menus.common.cmn as common

class CreateFolder(ctk.CTkFrame):
    def __init__(self, master, currentSession, path):
        super().__init__(master)

        self.configure(fg_color="#393939", corner_radius=10, border_width=1, width=400)
        self.columnconfigure(0, minsize=400)

        self.title = ctk.CTkLabel(self, text="Nova pasta", fg_color="transparent")
        self.title.grid(row=0, column=0, pady=5, sticky="ew")

        self.entry = ctk.CTkEntry(self, placeholder_text="Digite o nome da pasta...")
        self.entry.grid(row=1, column=0, padx=10, pady=5, sticky="ew")

        self.container_buttons = ctk.CTkFrame(self, fg_color="transparent")
        self.container_buttons.grid(row=2, column=0, pady=5)

        self.canceler = ctk.CTkButton(self.container_buttons, text="Cancelar", fg_color="#2b2f76", width=0, height=0, command=lambda: self.destroy())
        self.canceler.grid(row=0, column=0, padx=5)

        self.create = ctk.CTkButton(self.container_buttons, text="Criar pasta", fg_color="#2b2f76", width=0, height=0,
                    command=lambda cs=currentSession, p=path: self.actionClick(cs, p))
        self.create.grid(row=0, column=1, padx=5)

        common.center_menu(self.master, self)    # Centraliza o frame em relação à página

    def actionClick(self, currentSession, path):
        name_folder = self.entry.get()

        if name_folder != "":
            ctrl.createFolder(path, name_folder, self.master, currentSession)
            self.destroy()
        else:
            self.entry.focus()
            self.entry.configure(fg_color="#a24242")
