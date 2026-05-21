import customtkinter as ctk

import client.application.util.ul as util
import client.application.pages.dashboard.menus.forFiles as mfile
import client.application.pages.dashboard.menus.forFolders as mfolder
import client.application.controls.ctrl as ctrl

class Folders(ctk.CTkScrollableFrame):
    def __init__(self, master, content):
        self.master = master
        super().__init__(self.master)

        self.menu = None
        self.containers_description = []

        # Criar uma algum método que cria e destroi o botão do rootFolder

        # Métodos que serão utilizados posteriormente
        self.menuFile = mfile.menuFile
        self.menuFolder = mfolder.menuFolder
        self.change_background = util.change_background

        # Configurando características do container principal
        self.configure(fg_color="#252525")
        self.grid(row=0, column=1, columnspan=3, sticky="nsew")
        self.columnconfigure(0, weight=1)
        self.bind("<Button-3>", lambda e: self.open_menuFolder(e))

        # Criando container que abrigará a descrição do conteúdo de cada pasta
        self.container_descriptionContent = ctk.CTkFrame(self, fg_color="#4e4e4e")
        self.container_descriptionContent.grid(row=0, column=0, pady=5, padx=5, sticky="ew")
        self.container_descriptionContent.columnconfigure(0, weight=1)
        self.container_descriptionContent.columnconfigure(1, minsize=100, uniform="tam")
        self.container_descriptionContent.columnconfigure(2, minsize=100, uniform="tam")

        self.label_contentName = ctk.CTkLabel(self.container_descriptionContent, text="Nome")
        self.label_contentName.grid(row=0, column=0, padx=10, sticky="w")

        self.label_contentSize = ctk.CTkLabel(self.container_descriptionContent, text="Tamanho")
        self.label_contentSize.grid(row=0, column=1)

        self.label_contentType = ctk.CTkLabel(self.container_descriptionContent, text="Tipo")
        self.label_contentType.grid(row=0, column=2)

        for i in range(len(content["name"])):
            self.descriptionFolder(content["name"][i], content["size"][i], content["type"][i], i + 1)


    def descriptionFolder(self, file_name, size, sort, row):  # 'Sort' é o equivalente a 'type' (tipo)
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.grid(row=row, column=0, padx=5, pady=5, sticky="ew")
        container.columnconfigure(0, weight=1)
        container.columnconfigure(1, minsize=100, uniform="tam")
        container.columnconfigure(2, minsize=100, uniform="tam")

        contentName = ctk.CTkLabel(container, text=file_name)
        contentName.grid(row=0, column=0, padx=10, sticky="w")

        contentSize = ctk.CTkLabel(container, text=size)
        contentSize.grid(row=0, column=1)

        contentType = ctk.CTkLabel(container, text=sort)
        contentType.grid(row=0, column=2)

        array = [container, contentName, contentSize, contentType]
        for component in array:
            component.bind("<Button-1>", lambda e, c=container: self.actionClick(e, c))
            component.bind("<Button-3>", lambda e, c=container: self.open_menuFile(e, c))
            component.bind("<Enter>", lambda e, c=container: self.change_background(e, c, "#313131"))
            component.bind("<Leave>", lambda e, c=container: self.change_background(e, c, "transparent"))

        self.containers_description.append(container)

    def actionClick(self, event, forced_widget=None):
        target = forced_widget if forced_widget else event.widget

        if isinstance(target, ctk.CTkLabel):
            target = target.master

        childrens = target.winfo_children()

        try:
            name = childrens[0].cget('text')
            sort = childrens[2].cget('text')

            if sort == "pasta":
                ctrl.openFolder(self.master, self, name)     # Tenho que adiv=cionar o caminho da pasta
            elif sort == "arquivo":
                ctrl.openFile(self.master, self, name)
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

        self.menu = self.menuFolder(self.master, event)

    def open_menuFile(self, event, forced_widget=None):
        if self.menu is not None and self.menu.winfo_exists():
            self.menu.destroy()

        self.menu = self.menuFile(self.master, event, forced_widget)
