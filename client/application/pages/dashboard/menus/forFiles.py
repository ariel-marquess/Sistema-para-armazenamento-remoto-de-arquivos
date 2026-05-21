import customtkinter as ctk

import client.application.util.ul as util
import client.application.controls.ctrl as ctrl

class menuFile(ctk.CTkFrame):
    def __init__(self, master, event, forced_widget=None):
        super().__init__(master)

        target = forced_widget if forced_widget else event.widget
        if isinstance(target, ctk.CTkLabel):
            target = target.master

        childrens = target.winfo_children()

        try:
            name = childrens[0].cget('text')
            sort = childrens[2].cget('text')

            if sort == "arquivo":
                # Declarando métodos que serão utilizados posteriormente
                self.download = ctrl.download
                self.delete = ctrl.delete

                self.configure(fg_color="#393939", corner_radius=10, border_width=1, width=100)
                self.columnconfigure(0, weight=1)
                self.rowconfigure(2, minsize=10)

                download = ctk.CTkButton(self, text="Baixar", anchor="w", fg_color="transparent", command=lambda: self.download(name))    # Tenho que estabelecer qual será o diretório do arquivo
                download.grid(row=0, column=0, padx=10, pady=(5, 0), sticky="w")

                delete = ctk.CTkButton(self, text="Apagar", anchor="w", fg_color="transparent", command=lambda: self.delete(name))
                delete.grid(row=1, column=0, padx=10, sticky="w")

                canceler = ctk.CTkButton(self, text="Cancelar", anchor="w", fg_color="transparent", command=lambda: self.destroy())
                canceler.grid(row=3, column=0, padx=10, pady=5, sticky="w")

                x = event.x_root - self.winfo_rootx()
                y = event.y_root - self.winfo_rooty()
                self.place(x=x + 20, y=y + 20)
                self.lift()
        except Exception as e:
            util.MessageBox(
                title="Problema de execussão",
                message=f"ERRO: {e}",
                icon="warning"
            )