import customtkinter as ctk
import os

import client.application.utils.ul as util
import client.application.controls.ctrl as ctrl
import client.application.pages.dashboard.menus.common.cmn as common

class menuFile(ctk.CTkFrame):
    def __init__(self, master, event, objPath, forced_widget=None):
        super().__init__(master)
        self.objPath = objPath
        self.master = master # master -> descriptionFolders

        # Estilos do texto
        self.textFont = util.font(14)
        self.textColor = "white"

        target = forced_widget if forced_widget else event.widget
        if isinstance(target, ctk.CTkLabel):
            target = target.master

        childrens = target.winfo_children()
        name = childrens[0].cget('text')
        sort = childrens[2].cget('text')

        if sort == "arquivo":
            # Constrói o caminho completo para o arquivo sem alterar o histórico de navegação
            current_folder_path = self.objPath.get_current_path()
            pathClicked = os.path.join(current_folder_path, name)
            
            # Obtendo o username a partir da instância do Dashboard de forma segura
            dashboard = self.master.master
            username = dashboard.get_username()

            self.configure(fg_color="#393939", corner_radius=10, border_width=1, width=100)
            self.columnconfigure(0, weight=1)
            self.rowconfigure(2, minsize=10)

            download_button = ctk.CTkButton(self, text="Baixar", anchor="w", fg_color="transparent",
                                            command=lambda: self.execute_and_destroy(ctrl.download, [username, pathClicked]))
            download_button.grid(row=0, column=0, padx=10, pady=(5, 0), sticky="w")

            delete_button = ctk.CTkButton(self, text="Apagar", anchor="w", fg_color="transparent",
                                          command=lambda: self.execute_and_destroy(ctrl.delete, [username, pathClicked], target))
            delete_button.grid(row=1, column=0, padx=10, sticky="w")

            canceler = ctk.CTkButton(self, text="Cancelar", anchor="w", fg_color="transparent", font=self.textFont, text_color=self.textColor, command=lambda: self.destroy())
            canceler.grid(row=3, column=0, padx=10, pady=5, sticky="w")

            common.center_menu(self.master, self, event)

    def execute_and_destroy(self, func, args, widget_to_delete=None):
        """Executa a função de controle e depois destrói o menu e o widget do arquivo, se aplicável."""
        dashboard = self.master.master
        if func(*args):
            dashboard.navigate_to_current_path()
        self.destroy()
