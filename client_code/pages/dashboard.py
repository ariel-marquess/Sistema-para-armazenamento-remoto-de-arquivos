import os
import customtkinter as ctk

try:
    import client_code.controls.util as util
    import client_code.controls.open_data as openData
    import client_code.controls.file_handler as file
except ImportError:
    util = None
    openData = None
    file = None


class Dashboard(ctk.CTk):
    def __init__(self, data):
        super().__init__()

        # Precarregando componentes
        self.container_scrollH = None
        self.container_scrollV = None
        self.row_rootFolder = None
        self.button_downloadFile = None
        self.label_contentFile = None
        self.container_contentFile = None
        self.label_rootFolder = None
        self.button_toGoBack = None
        self.container_header = None
        self.container_rootFolder = None
        self.button_upload = None
        self.label_contentType = None
        self.label_contentSize = None
        self.label_contentName = None
        self.container_descriptionContent = None
        self.container_contentFolder = None
        self.currentPath = None
        self.containers_description = []
        self.containers_rootFolder = []

        self.geometry("800x600")
        self.title("Drive Docs")
        self.configure(fg_color="#252525")

        # Configurando as colunas da página
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1, minsize=190)
        self.grid_columnconfigure(2, weight=1, minsize=190)
        self.grid_columnconfigure(3, weight=1, minsize=190)

        # Configurando linhas da página
        self.rowconfigure(0, weight=1)

        # Criando as seções da página
        self.session_rootFolder(data)
        self.session_descriptionFolder(data)



    # O método a seguir e o próximo são utilizados para construir o container que expõe as pastas presentes na raiz do arquivo
    # reservado ao usuário.
    def session_rootFolder(self, content):
        if ((((hasattr(self, "container_rootFolder") and self.container_rootFolder) or
                (hasattr(self, "container_header") and self.container_header)) or
                (hasattr(self, "button_toGoBack") and self.button_toGoBack)) or
                (hasattr(self, "label_rootFolder") and self.label_rootFolder)):
            self.container_rootFolder.destroy()
            self.container_header.destroy()
            self.button_toGoBack.destroy()
            self.label_rootFolder.destroy()
        
        # Criando container que abrigará as pastas presentes na raiz da conta
        self.container_rootFolder = ctk.CTkFrame(self, fg_color="#4e4e4e")
        self.container_rootFolder.grid(row=0, column=0, sticky="nsew")
        self.container_rootFolder.columnconfigure(0, weight=1, minsize=230)

        # Criando o cabeçalho do container anterior
        self.container_header = ctk.CTkFrame(self.container_rootFolder, fg_color="transparent")
        self.container_header.grid(row=0, column=0, pady=5, sticky="ew")
        self.container_header.columnconfigure(0, weight=1, uniform="equal")
        self.container_header.columnconfigure(2, weight=1, uniform="equal")

        self.button_toGoBack = ctk.CTkButton(self.container_header, text="", image=util.images('tgbg'), fg_color="transparent", width=20)
        self.button_toGoBack.grid(row=0, column=0, padx=5, sticky="w")

        self.label_rootFolder = ctk.CTkLabel(self.container_header, text="Arquivos", font=("Roboto", 14, "bold"))
        self.label_rootFolder.grid(row=0, column=1)

        self.row_rootFolder = 1
        for i in range(len(content["name"])):
            if content["type"][i] == "pasta":
                self.rootFolder(content['name'][i])
                self.row_rootFolder += 1

        # Adicionando botão de "fazer upload"
        self.button_upload = ctk.CTkButton(self.container_rootFolder, text="Fazer upload", fg_color="#2b2f76")
        self.button_upload.grid(row=self.row_rootFolder, column=0, pady=20, sticky="s")
        self.container_rootFolder.rowconfigure(self.row_rootFolder, weight=1)

    def rootFolder(self, folder_name):
        container = ctk.CTkFrame(self.container_rootFolder, fg_color="transparent")
        container.grid(row=self.row_rootFolder, column=0, pady=5, padx=5, sticky="ew")
        container.columnconfigure(1, weight=1)
        container.bind("<Enter>", lambda e: container.configure(fg_color="#676767"))
        container.bind("<Leave>", lambda e: container.configure(fg_color="transparent"))

        label_image = ctk.CTkLabel(container, image=util.images("folder", 30), text="")
        label_image.grid(row=0, column=0, padx=5)

        label_text = ctk.CTkLabel(container, text=folder_name)
        label_text.grid(row=0, column=1, sticky="w")

        self.containers_rootFolder.append(container)



    # O método a seguir e os dois próximos são utilizados para estruturar o container que expõe o conteúdo das pastas.
    def session_descriptionFolder(self, content):
        if ((((hasattr(self, "container_contentFolder") and self.container_contentFolder) or
                (hasattr(self, "container_descriptionContent") and self.container_descriptionContent)) or
                (hasattr(self, "label_contentName") and self.label_contentName)) or
                (hasattr(self, "label_contentSize") and self.label_contentSize) or
                (hasattr(self, "label_contentType") and self.label_contentType)):
            self.container_contentFolder.destroy()
            self.container_descriptionContent.destroy()
            self.label_contentName.destroy()
            self.label_contentSize.destroy()
            self.label_contentType.destroy()

        if not self.button_upload:
            self.button_upload = ctk.CTkButton(self.container_rootFolder, text="Fazer upload", fg_color="#2b2f76")
            self.button_upload.grid(row=self.row_rootFolder, column=0, pady=20, sticky="s")

        # Criando o container que abrigará o conteúdo das pastas
        self.container_contentFolder = ctk.CTkFrame(self, fg_color="#252525")
        self.container_contentFolder.grid(row=0, column=1, columnspan=3, sticky="nsew")
        self.container_contentFolder.columnconfigure(0, weight=1)
        self.container_contentFolder.bind("<Button-3>")  # Adicionar o método para criar uma pasta

        # Criando container que abrigará a descrição do conteúdo de cada pasta
        self.container_descriptionContent = ctk.CTkFrame(self.container_contentFolder, fg_color="#4e4e4e")
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
        container = ctk.CTkFrame(self.container_contentFolder, fg_color="transparent")
        container.grid(row=row, column=0, padx=5, pady=5, sticky="ew")
        container.columnconfigure(0, weight=1)
        container.columnconfigure(1, minsize=100, uniform="tam")
        container.columnconfigure(2, minsize=100, uniform="tam")

        container.bind("<Button-1>", lambda e: self.actionClick(e, container))
        container.bind("<Button-3>", lambda e: self.optionMenu(e, container))
        container.bind("<Enter>", lambda e: container.configure(fg_color="#313131"))
        container.bind("<Leave>", lambda e: container.configure(fg_color="transparent"))

        contentName = ctk.CTkLabel(container, text=file_name)
        contentName.grid(row=0, column=0, padx=10, sticky="w")
        contentName.bind("<Button-1>", lambda e: self.actionClick(e, container))
        contentName.bind("<Button-1>", lambda e: self.optionMenu(e, container))

        contentSize = ctk.CTkLabel(container, text=size)
        contentSize.grid(row=0, column=1)
        contentSize.bind("<Button-1>", lambda e: self.actionClick(e, container))
        contentSize.bind("<Button-1>", lambda e: self.optionMenu(e, container))

        contentType = ctk.CTkLabel(container, text=sort)
        contentType.grid(row=0, column=2)
        contentType.bind("<Button-1>", lambda e: self.actionClick(e, container))
        contentType.bind("<Button-1>", lambda e: self.optionMenu(e, container))

        self.containers_description.append(container)

    def destroy_descriptionFolder(self):
        for component in self.containers_description:
            component.destroy()

        self.container_contentFolder.destroy()



    # O método a seguir e o próximo são utilizados para estruturar o container que expõe o conteúdo de determinado arquivo clicado.
    def session_contentFile(self, content):
        if ((((hasattr(self, "container_contentFile") and self.container_contentFile) or
                (hasattr(self, "label_contentFile") and self.label_contentFile)) or
                (hasattr(self, "button_downloadFile") and self.button_downloadFile))):
            self.container_contentFile.destroy()
            self.label_contentFile.destroy()
            self.button_downloadFile.destroy()

        self.destroy_descriptionFolder()

        if self.button_upload:
            self.button_upload.destroy()

        self.container_contentFile = ctk.CTkFrame(self, fg_color="#252525")
        self.container_contentFile.grid(row=0, column=1, columnspan=3, sticky="nsew")
        self.container_contentFile.columnconfigure(0, weight=1)
        self.container_contentFile.rowconfigure(0, weight=1)

        self.container_scrollV = ctk.CTkScrollableFrame(self.container_contentFile, orientation="vertical", fg_color="transparent")
        self.container_scrollV.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")

        self.label_contentFile = ctk.CTkLabel(self.container_scrollV, text=content, anchor="nw", justify="left")
        self.label_contentFile.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        self.button_downloadFile = ctk.CTkButton(self.container_contentFile, text="Baixar arquivo", fg_color="#2b2f76")
        self.button_downloadFile.grid(row=1, column=0, padx=20, pady=20, sticky="e")

    def destroy_contentFile(self):
        if self.container_contentFile and self.label_contentFile and self.button_downloadFile:
            self.container_contentFile.destroy()
            self.label_contentFile.destroy()
            self.button_downloadFile.destroy()



    # O seguinte método e os dois póximos são utilizados para realizar as interações de abertura tanto de pastas como de arquivos
    # (na sessão reservada para mostrar o conteúdo das pastas).
    def actionClick(self, event, forced_widget=None):
        target = forced_widget if forced_widget else event.widget

        if isinstance(target, ctk.CTkLabel):
            target = target.master

        childrens = target.winfo_children()

        try:
            name = childrens[0].cget('text')
            sort = childrens[2].cget('text')

            if sort == "pasta":
                self.openFolder(name)
            elif sort == "arquivo":
                self.openFile(name)
        except Exception as e:
            util.MessageBox(
                title="Problema de execussão",
                message=f"ERRO: {e}",
                icon="warning"
            )

    def openFolder(self, folder_name):
        if self.currentPath:
            self.currentPath = os.path.join(self.currentPath, folder_name)
            content_descriptionPath = openData.openFolder(self.currentPath)

            self.destroy_contentFile()
            self.session_descriptionFolder(content_descriptionPath)
        else:
            print(f'Abrindo pasta: {folder_name}')

    def openFile(self, file_name):
        if self.currentPath:
            self.currentPath = os.path.join(self.currentPath, file_name)
            content_file = openData.openFile(self.currentPath)

            self.destroy_descriptionFolder()
            self.session_contentFile(content_file)
        else:
            currentDirectory = os.path.dirname(__file__)
            filePath = os.path.join(currentDirectory, "texto.txt")

            with open(filePath, 'r', encoding="utf-8") as f:
                content = f.read()

            self.destroy_descriptionFolder()
            self.session_contentFile(content)



    # O seguinte método e os dois próximos são utilizados para abrir e gerenciar o menu aberto ao clicar com o botão direito do mouse em um arquivo
    def optionMenu(self, event, forced_widget=None):
        target = forced_widget if forced_widget else event.widget

        if isinstance(target, ctk.CTkLabel):
            target = target.master

        childrens = target.winfo_children()

        try:
            name = childrens[0].cget('text')
            sort = childrens[2].cget('text')

            if sort == "arquivo":
                if hasattr(self, "menu") and self.menu:
                    self.menu.destroy()

                self.menu = ctk.CTkFrame(self, fg_color="#393939", corner_radius=10, border_width=1, width=100)
                self.menu.columnconfigure(0, weight=1)
                self.menu.rowconfigure(2, minsize=10)

                button_baixar = ctk.CTkButton(self.menu, text="Baixar", anchor="w", fg_color="transparent", command=lambda: self.download(name))
                button_baixar.grid(row=0, column=0, padx=10, pady=(5, 0), sticky="w")

                button_apagar = ctk.CTkButton(self.menu, text="Apagar", anchor="w", fg_color="transparent", command=lambda: self.delete(name))
                button_apagar.grid(row=1, column=0, padx=10, sticky="w")

                button_cancelar = ctk.CTkButton(self.menu, text="Cancelar", anchor="w", fg_color="transparent", command=lambda: self.menu.destroy())
                button_cancelar.grid(row=3, column=0, padx=10, pady=5, sticky="w")

                x = event.x_root - self.winfo_rootx()
                y = event.y_root - self.winfo_rooty()
                self.menu.place(x=x + 20, y=y + 20)
                self.menu.lift()
        except Exception as e:
            util.MessageBox(
                title="Problema de execussão",
                message=f"ERRO: {e}",
                icon="warning"
            )

    def download(self, file_name):
        file_clicked = os.path.join(self.currentPath, file_name)
        file.downloadFile(file_clicked)

    def delete(self, file_name):
        file_clicked = os.path.join(self.currentPath, file_name)
        file.deleteFile(file_clicked)