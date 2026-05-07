import os
import customtkinter as ctk
from PIL import Image
from CTkMessagebox import CTkMessagebox


def MessageBox(title, message, icon):    # Método que cria uma caixa de mensagem quando executado
    CTkMessagebox(title=title, message=message, icon=icon)


def images(command):    # Método que retorna uma imagem quando chamado
    try:
        current = {
            'f': os.path.join(os.path.dirname(os.path.relpath(__file__)), "..", "images", "folder.png"),
            'tgg': os.path.join(os.path.dirname(os.path.relpath(__file__)), "..", "images", "toGo-gray.png"),
            'tgw': os.path.join(os.path.dirname(os.path.relpath(__file__)), "..", "images", "toGo-white.png"),
            'tgbg': os.path.join(os.path.dirname(os.path.relpath(__file__)), "..", "images", "toGoBack-gray.png"),
            'tgbw': os.path.join(os.path.dirname(os.path.relpath(__file__)), "..", "images", "toGoBack-white.png")
        }

        return ctk.CTkImage(
            light_image=Image.open(current[command]),
            dark_image=Image.open(current[command]),
            size=(20, 20)
        )
    except Exception as e:
        MessageBox(
            title="Problema ao carregar as imagens",
            message=f"ERRO: {e}",
            icon="warning"
        )

    return None


class Dashboard(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.containers = []
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

        # Criando container que abrigará as pastas presentes na raiz da conta
        self.container_rootFolder = ctk.CTkFrame(self, fg_color="#343434")
        self.container_rootFolder.grid(row=0, column=0, sticky="nsew")
        self.container_rootFolder.columnconfigure(0, weight=1, minsize=230)

        # Criando o cabeçalho do container anterior
        self.container_header = ctk.CTkFrame(self.container_rootFolder, fg_color="#343434")
        self.container_header.grid(row=0, column=0, pady=5, sticky="ew")
        self.container_header.columnconfigure(0, weight=1, uniform="equal")
        self.container_header.columnconfigure(2, weight=1, uniform="equal")

        self.container_buttonsHeader = ctk.CTkFrame(self.container_header, fg_color="#343434")
        self.container_buttonsHeader.grid(row=0, column=0, sticky="nsew")
        self.container_buttonsHeader.rowconfigure(0, weight=1)

        self.button_toGoBack = ctk.CTkButton(self.container_buttonsHeader, text="", image=images('tgbg'), fg_color="transparent", width=20)
        self.button_toGoBack.grid(row=0, column=0)

        self.button_toGo = ctk.CTkButton(self.container_buttonsHeader, text="", image=images('tgg'), fg_color="transparent", width=20)
        self.button_toGo.grid(row=0, column=1)

        self.label_rootFolder = ctk.CTkLabel(self.container_header, text="Arquivos", font=("Roboto", 14, "bold"))
        self.label_rootFolder.grid(row=0, column=1)

        # Criando o container que abrigará o conteúdo das pastas
        self.container_contentFolder = ctk.CTkFrame(self, fg_color="#252525")
        self.container_contentFolder.grid(row=0, column=1, columnspan=3, sticky="nsew")
        self.container_contentFolder.columnconfigure(0, weight=1)

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

        # Abaixo estão dispostos os meios que utilizamos para criação dos componetes dinâmicos da página
        dic = {
            'name': ['Downloads', 'Documentos', 'Imagens', 'curriculo.txt'],
            'size': ['3 itens', '2 itens', '5 itens', '23 kB'],
            'type': ['pasta', 'pasta', 'pasta', 'arquivo']
        }

        for i in range(len(dic["name"])):
            self.descriptionPath(dic["name"][i], dic["size"][i], dic["type"][i], i+1)



    def descriptionPath(self, name, size, sort, row):    # 'Sort' é o equivalente a 'type' (tipo)
        container = ctk.CTkFrame(self.container_contentFolder, fg_color="transparent")
        container.grid(row=row, column=0, padx=5, pady=5, sticky="ew")
        container.columnconfigure(0, weight=1)
        container.columnconfigure(1, minsize=100, uniform="tam")
        container.columnconfigure(2, minsize=100, uniform="tam")
        container.bind("<Button-1>", self.optionMenu)
        container.bind("<Button-3>", self.optionMenu)
        container.bind("<Enter>", lambda e, c=container: container.configure(fg_color="#313131") if c.cget("fg_color") == "transparent" else container.configure(fg_color="transparent"))
        container.bind("<Leave>", lambda e, c=container: container.configure(fg_color="#313131") if c.cget("fg_color") == "transparent" else container.configure(fg_color="transparent"))

        contentName = ctk.CTkLabel(container, text=name)
        contentName.grid(row=0, column=0, padx=10, sticky="w")

        contentSize = ctk.CTkLabel(container, text=size)
        contentSize.grid(row=0, column=1)

        contentType = ctk.CTkLabel(container, text=sort)
        contentType.grid(row=0, column=2)

        self.containers.append(container)


    def optionMenu(self, event):
        if hasattr(self, "menu"):
            self.menu.destroy()

        self.menu = ctk.CTkFrame(self, fg_color="#393939", corner_radius=10, border_width=1, width=100)
        self.menu.columnconfigure(0, weight=1)
        self.menu.rowconfigure(2, minsize=10)

        button_baixar = ctk.CTkButton(self.menu, text="Baixar", anchor="w", fg_color="transparent")
        button_baixar.grid(row=0, column=0, padx=10, pady=(5, 0), sticky="w")

        button_apagar = ctk.CTkButton(self.menu, text="Apagar", anchor="w", fg_color="transparent")
        button_apagar.grid(row=1, column=0, padx=10, sticky="w")

        button_cancelar = ctk.CTkButton(self.menu, text="Cancelar", anchor="w", fg_color="transparent", command=lambda: self.menu.destroy())
        button_cancelar.grid(row=3, column=0, padx=10, pady=5, sticky="w")

        x = event.x_root - self.winfo_rootx()
        y = event.y_root - self.winfo_rooty()
        self.menu.place(x=x + 20, y=y + 20)
        self.menu.lift()


    def download(self, name, currentPath):
        return False

    def delete(self, name, currentPath):
        return False

