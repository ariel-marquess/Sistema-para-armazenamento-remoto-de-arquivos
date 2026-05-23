import os, sys
import customtkinter as ctk

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import client.application.util.ul as util
from client.application.pages.login.log import Login
from client.application.pages.account.cac import Create
from client.application.pages.dashboard.db import Dashboard


class Main(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Drive Docs")
        self.configure(fg_color="#252525")
        self.center_window(800, 600)

        # Configurando linhas e colunas da janela
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.container = None
        self.start_login()


    def start_login(self):
        if self.container is not None:
            self.container.destroy()

        self.container = Login(
            master=self,
            open_create=self.start_create,
            open_dashboard=self.start_dashboard)

    def start_create(self):
        if self.container is not None:
            self.container.destroy()

        self.container = Create(
            master=self,
            open_login=self.start_login)

    def start_dashboard(self, data):
        if self.container is not None:
            self.container.destroy()

        self.container = Dashboard(
            master=self,
            content=data)

    def center_window(self, width, heigth):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x = (screen_width - width) / 2
        y = (screen_height - heigth) / 2

        self.geometry(f"{width}x{heigth}+{int(x)}+{int(y)}")



if __name__ == "__main__":
    app = Main()
    app.mainloop()