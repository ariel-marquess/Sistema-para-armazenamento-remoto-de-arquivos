import customtkinter as ctk

import client.application.controls.ctrl as ctrl

class menuFolder(ctk.CTkFrame):
    def __init__(self, master, event):
        super().__init__(master)

        self.configure(fg_color="#393939", corner_radius=10, border_width=1, width=100)
        self.columnconfigure(0, weight=1)

        createFolder = ctk.CTkButton(self, text="Criar pasta", anchor="w", fg_color="transparent", command=lambda: self.execute(ctrl.createFolder))
        createFolder.grid(row=0, column=0, padx=10, pady=5, sticky="w")

        canceler = ctk.CTkButton(self, text="Cancelar", anchor="w", fg_color="transparent", command=lambda: self.destroy())
        canceler.grid(row=3, column=0, padx=10, pady=5, sticky="w")

        x = event.x_root - master.winfo_rootx()
        y = event.y_root - master.winfo_rooty()
        self.place(x=x + 20, y=y + 20)
        self.lift()

    def execute(self, function):
        function()
        self.destroy()