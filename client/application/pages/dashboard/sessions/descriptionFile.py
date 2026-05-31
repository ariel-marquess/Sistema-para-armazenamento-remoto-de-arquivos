import customtkinter as ctk

import client.application.controls.ctrl as ctrl
import client.application.utils.ul as util

class File(ctk.CTkFrame):
    def __init__(self, master, content, currentPath, username):
        # O 'master' que esta classe recebe já é a instância do Dashboard
        super().__init__(master)
        self.username = username
        self.currentPath = currentPath

        # Estilos do texto
        self.textColor = "white"

        self.configure(fg_color="#252525")
        self.grid(row=0, column=1, columnspan=3, sticky="nsew")
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.container_scrollV = ctk.CTkScrollableFrame(self, orientation="vertical", fg_color="transparent")
        self.container_scrollV.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")

        self.label_contentFile = ctk.CTkLabel(self.container_scrollV, text=content, anchor="nw", justify="left", font=util.font(14), text_color=self.textColor)
        self.label_contentFile.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        self.button_downloadFile = ctk.CTkButton(
            self, text="Baixar arquivo", fg_color="#2b2f76", text_color=self.textColor,
            command=lambda: ctrl.download(self.username, self.currentPath))
        self.button_downloadFile.grid(row=1, column=0, padx=20, pady=20, sticky="e")
