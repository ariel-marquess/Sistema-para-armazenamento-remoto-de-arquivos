import customtkinter as ctk

import client.application.utils.ul as util
import client.application.controls.ctrl as ctrl
import client.application.pages.dashboard.menus.common.cmn as common

class menuFile(ctk.CTkFrame):
    def __init__(self, master, event, objPath, forced_widget=None):
        super().__init__(master)
        self.objPath = objPath

        target = forced_widget if forced_widget else event.widget
        if isinstance(target, ctk.CTkLabel):
            target = target.master

        childrens = target.winfo_children()
        name = childrens[0].cget('text')
        sort = childrens[2].cget('text')

        if sort == "arquivo":
            # Declarando métodos que serão utilizados posteriormente
            self.download = ctrl.download
            self.delete = ctrl.delete

            # Apontando o caminho do arquivo clicado
            self.objPath.join(name)
            pathCliked = self.objPath.getPath()

            self.configure(fg_color="#393939", corner_radius=10, border_width=1, width=100)
            self.columnconfigure(0, weight=1)
            self.rowconfigure(2, minsize=10)

            download = ctk.CTkButton(self, text="Baixar", anchor="w", fg_color="transparent",
                        command=lambda s=self, download=ctrl.download, p=pathCliked: util.execute(s, download, [p]))  # Tenho que estabelecer qual será o diretório do arquivo
            download.grid(row=0, column=0, padx=10, pady=(5, 0), sticky="w")

            delete = ctk.CTkButton(self, text="Apagar", anchor="w", fg_color="transparent",
                        command=lambda s=self, delete=ctrl.delete, t=target, p=pathCliked: util.execute(s, delete, [t, p]))
            delete.grid(row=1, column=0, padx=10, sticky="w")

            canceler = ctk.CTkButton(self, text="Cancelar", anchor="w", fg_color="transparent", command=lambda: self.destroy())
            canceler.grid(row=3, column=0, padx=10, pady=5, sticky="w")

            common.center_menu(self.master, self, event)