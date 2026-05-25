import customtkinter as ctk

import client.application.utils.ul as util
import client.application.controls.ctrl as ctrl

class RootFolders(ctk.CTkFrame):
    def __init__(self, master, content, objPath):
        super().__init__(master)
        self.objPath = objPath

        # Declarando variáveis que serão utilizadas posteriormente
        self.containers_rootFolder = []

        # Declarando métodos que serão utilizados posteriormente
        self.change_background = util.change_background

        self.configure(fg_color="#4e4e4e")
        self.grid(row=0, column=0, sticky="nsew")
        self.columnconfigure(0, weight=1, minsize=230)

        # Criando o cabeçalho do container anterior
        self.container_header = ctk.CTkFrame(self, fg_color="transparent")
        self.container_header.grid(row=0, column=0, pady=5, sticky="ew")
        self.container_header.columnconfigure(0, weight=1, uniform="equal")
        self.container_header.columnconfigure(2, weight=1, uniform="equal")

        self.button_toGoBack = ctk.CTkButton(self.container_header, text="", image=util.images('tgbg'), fg_color="transparent", width=20,
                    command=lambda: self.toGoBack())
        self.button_toGoBack.grid(row=0, column=0, padx=5, sticky="w")

        self.label_rootFolder = ctk.CTkLabel(self.container_header, text="Arquivos", font=("Roboto", 14, "bold"))
        self.label_rootFolder.grid(row=0, column=1)

        self.row_rootFolder = 1
        for i in range(len(content["name"])):
            if content["type"][i] == "pasta":
                self.rootFolder(content['name'][i])
                self.row_rootFolder += 1

        # Adicionando botão de "fazer upload"
        self.button_upload = ctk.CTkButton(self, text="Fazer upload", fg_color="#2b2f76")
        self.button_upload.grid(row=self.row_rootFolder, column=0, pady=20, sticky="s")
        self.rowconfigure(self.row_rootFolder, weight=1)


    def rootFolder(self, folder_name):
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.grid(row=self.row_rootFolder, column=0, pady=5, padx=5, sticky="ew")
        container.columnconfigure(1, weight=1)

        label_image = ctk.CTkLabel(container, image=util.images("folder", 30), text="")
        label_image.grid(row=0, column=0, padx=5)

        label_text = ctk.CTkLabel(container, text=folder_name)
        label_text.grid(row=0, column=1, sticky="w")

        array = [container, label_image, label_text]
        for component in array:
            component.bind("<Button-1>", lambda e, c=container: self.actionClick(e, c))
            component.bind("<Enter>",
                        lambda e, comp=component, c=container: self.change_background(event=e, forced_widget=(None if isinstance(comp, ctk.CTkFrame) else c), color="#676767"))
            component.bind("<Leave>",
                        lambda e, comp=component, c=container: self.change_background(event=e, forced_widget=(None if isinstance(comp, ctk.CTkFrame) else c), color="transparent"))

        self.containers_rootFolder.append(container)


    def actionClick(self, event, forced_widget=None):
        try:
            target = forced_widget if forced_widget else event.widget

            if isinstance(target, ctk.CTkLabel):
                target = target.master

            name = target.winfo_children()[1].cget('text')

            self.objPath.joinRoot(name)
            self.objPath.addLastPath(self.objPath.getPath())
            ctrl.openFolder(self.master, self, self.objPath.getPath())
        except Exception as e:
            util.MessageBox(
                title="Não foi possível abrir a pasta",
                message=f"ERRO: {e}",
                icon="warning"
            )


    def toGoBack(self):
        try:
            path = None  # Tenho que faxer um mevanismo para voltar para a pasta anterior

            descriptionFolder = self.master.winfo_childrens()[1]  # Retorna a segunda sessão da página Dashboard
            ctrl.openFolder(self.master, descriptionFolder, path)
        except Exception as e:
            util.MessageBox(
                title="Não foi possível retornar à pasta anterior",
                message=f"ERRO: {e}",
                icon="warning"
            )