import customtkinter as ctk

import client.application.util.ul as util
from client.application.pages.login.log import Login
from client.application.pages.account.cac import Create
from client.application.pages.dashboard.db import Dashboard


class Main(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.overrideredirect(True)
        self.configure(fg_color="#252525")
        self.center_window(800, 650)

        # Configurando linhas e colunas da janela
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Barramento superior da janela
        self.top_bar = ctk.CTkFrame(self, fg_color="#2d2d2e", height=70)
        self.top_bar.grid(row=0, column=0, pady=0, sticky="ew")
        self.top_bar.grid_columnconfigure(0, weight=1, uniform="equal")
        self.top_bar.grid_columnconfigure(2, weight=1, uniform="equal")

        self.label_title = ctk.CTkLabel(self.top_bar, text="Drive Docs", font=("Roboto", 20, "bold"))
        self.label_title.grid(row=0, column=1, pady=5)

        self.button_close = ctk.CTkButton(self.top_bar, text="", fg_color="transparent", anchor="e", width=0, height=0, image=util.images("close"), command=lambda: self.destroy())
        self.button_close.grid(row=0, column=2, pady=5, padx=10, sticky="e")

        self.container = None
        self.start_login()

    def start_login(self):
        self.container = Login(
            master=self,
            open_create=self.start_create,
            open_dashboard=self.start_dashboard)

    def start_create(self):
        self.container = Create(
            master=self,
            page_login=self.start_login)
        self.container.mainloop()

    def start_dashboard(self, data):
        self.container = Dashboard(
            master=self,
            content=data)
        self.container.mainloop()

    def center_window(self, width, heigth):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x = (screen_width - width) / 2
        y = (screen_height - heigth) / 2

        self.geometry(f"{width}x{heigth}+{int(x)}+{int(y)}")



if __name__ == "__main__":
    app = Main()
    app.mainloop()