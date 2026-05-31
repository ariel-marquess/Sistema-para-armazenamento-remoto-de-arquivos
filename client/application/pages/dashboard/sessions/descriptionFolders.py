import customtkinter as ctk
import os

import client.application.utils.ul as util
import client.application.pages.dashboard.menus.forFiles as mfile
import client.application.pages.dashboard.menus.forFolders as mfolder
import client.application.controls.ctrl as ctrl

class Folders(ctk.CTkScrollableFrame):
    def __init__(self, master, content, objPath):
        super().__init__(master)
        self.master = master # Dashboard
        self.objPath = objPath

        self.menu = None
        self.containers_description = []

        # Estilos do texto
        self.textFont = util.font(13)
        self.textColor = "white"

        # Métodos que serão utilizados posteriormente
        self.menuFile = mfile.menuFile
        self.menuFolder = mfolder.menuFolder
        self.change_background = util.change_background

        # Configurando o frame
        self.configure(fg_color="#252525")
        self.grid(row=0, column=1, columnspan=3, sticky="nsew")
        self.columnconfigure(0, weight=1)
        self.bind_background_menu()

        # Cabeçalho da lista de arquivos
        self.container_descriptionContent = ctk.CTkFrame(self, fg_color="#4e4e4e")
        self.container_descriptionContent.grid(row=0, column=0, pady=5, padx=5, sticky="ew")
        self.container_descriptionContent.columnconfigure(0, weight=1)
        self.container_descriptionContent.columnconfigure(1, minsize=100, uniform="tam")
        self.container_descriptionContent.columnconfigure(2, minsize=100, uniform="tam")

        self.label_contentName = ctk.CTkLabel(self.container_descriptionContent, text="Nome", font=self.textFont, text_color=self.textColor)
        self.label_contentName.grid(row=0, column=0, padx=10, sticky="w")

        self.label_contentSize = ctk.CTkLabel(self.container_descriptionContent, text="Tamanho", font=self.textFont, text_color=self.textColor)
        self.label_contentSize.grid(row=0, column=1)

        self.label_contentType = ctk.CTkLabel(self.container_descriptionContent, text="Tipo", font=self.textFont, text_color=self.textColor)
        self.label_contentType.grid(row=0, column=2)

        # Renderiza os itens da pasta
        if content and content.get("name"):
            for i in range(len(content["name"])):
                self.descriptionFolder(content["name"][i], content["size"][i], content["type"][i], i + 1)

    def descriptionFolder(self, file_name, size, sort, row):  # 'Sort' é o equivalente a 'type' (tipo)
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.grid(row=row, column=0, padx=5, pady=5, sticky="ew")
        container.columnconfigure(0, weight=1)
        container.columnconfigure(1, minsize=100, uniform="tam")
        container.columnconfigure(2, minsize=100, uniform="tam")

        contentName = ctk.CTkLabel(container, text=file_name, font=self.textFont, text_color=self.textColor)
        contentName.grid(row=0, column=0, padx=10, sticky="w")

        contentSize = ctk.CTkLabel(container, text=size, font=self.textFont, text_color=self.textColor)
        contentSize.grid(row=0, column=1)

        contentType = ctk.CTkLabel(container, text=sort, font=self.textFont, text_color=self.textColor)
        contentType.grid(row=0, column=2)

        # --- CORREÇÃO APLICADA AQUI ---
        # Associa os eventos de clique a todos os componentes para garantir a captura
        # O 'forced_widget=container' garante que a função sempre receba o container principal
        for component in container.winfo_children():
            component.bind("<Button-1>", lambda e, c=container: self.actionClick(e, forced_widget=c))
            if sort == "pasta":
                component.bind("<Button-3>", lambda e: self.open_menuFolder(e))
            else:
                component.bind("<Button-3>", lambda e, c=container: self.open_menuFile(e, forced_widget=c))
            component.bind("<Enter>", lambda e, c=container: self.change_background(e, c, "#313131"))
            component.bind("<Leave>", lambda e, c=container: self.change_background(e, c, "transparent"))

        if sort == "pasta":
            container.bind("<Button-3>", lambda e: self.open_menuFolder(e))
        else:
            container.bind("<Button-3>", lambda e, c=container: self.open_menuFile(e, forced_widget=c))

        self.containers_description.append(container)

    def actionClick(self, event, forced_widget=None):
        target = forced_widget if forced_widget else event.widget

        if isinstance(target, ctk.CTkLabel):
            target = target.master

        childrens = target.winfo_children()

        try:
            name = childrens[0].cget('text')
            sort = childrens[2].cget('text')

            self.objPath.join(name)
            username = self.master.get_username()

            if sort == "pasta":
                self.master.navigate_to_current_path()
            else:
                ctrl.openFile(self.master, self, username, self.objPath)
        except Exception as e:
            util.MessageBox(
                title="Problema de execussão",
                message=f"ERRO: {e}",
                icon="warning"
            )

    def destroy(self):
        for component in self.containers_description:
            component.destroy()

        self.containers_description.clear()
        super().destroy()

    def open_menuFolder(self, event):
        if self.menu is not None and self.menu.winfo_exists():
            self.menu.destroy()

        self.menu = self.menuFolder(
            self.master,   # Será a referência para criação do menu
            self,   # É a referência do descriptionFolder
            self.menu,    # Indica o local (na máquina) onde o menu será criado
            event,    # Indica o evento que disparou o método
            self.objPath)

    def open_menuFile(self, event, forced_widget=None):
        if self.menu is not None and self.menu.winfo_exists():
            self.menu.destroy()

        self.menu = self.menuFile(self.master, event, self.objPath, forced_widget)

    def bind_background_menu(self):
        self.bind("<Button-3>", self.open_menuFolder)

        if hasattr(self, "_parent_canvas"):
            self._parent_canvas.bind("<Button-3>", self.open_menuFolder)
