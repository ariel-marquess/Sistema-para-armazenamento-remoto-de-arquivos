import customtkinter as ctk

import client.application.controls.ctrl as ctrl

class File(ctk.CTkFrame):
    def __init__(self, master, content, currentPath):
        super().__init__(master)

        self.configure(fg_color="#252525")
        self.grid(row=0, column=1, columnspan=3, sticky="nsew")
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.container_scrollV = ctk.CTkScrollableFrame(self, orientation="vertical", fg_color="transparent")
        self.container_scrollV.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")

        self.label_contentFile = ctk.CTkLabel(self.container_scrollV, text=content, anchor="nw", justify="left")
        self.label_contentFile.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        self.button_downloadFile = ctk.CTkButton(self, text="Baixar arquivo", fg_color="#2b2f76", command=lambda p=currentPath: ctrl.download(p))
        self.button_downloadFile.grid(row=1, column=0, padx=20, pady=20, sticky="e")


    def destroy(self):
        self.destroy()