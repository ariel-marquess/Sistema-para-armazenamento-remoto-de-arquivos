import os
import customtkinter as ctk
from PIL import Image
from CTkMessagebox import CTkMessagebox


def show_messagebox():  # Método que abre um alerta informando que as informações disponibilizadas estão incorretas
    message = CTkMessagebox(title="Inconsistência de dados", message="ERRO: usuário ou senha incorretos.", icon="warning")


class Login(ctk.CTk):
    def __init__(self, open_create, open_dashboard, **kwargs):
        super().__init__(**kwargs)

        self.geometry("800x600")
        self.title("Drive Docs")

        # Adicionando a imagem da página
        try:
            current_path = os.path.join(os.path.dirname(os.path.relpath(__file__)), "..", "images", "file.png")

            self.image = ctk.CTkImage(
                light_image=Image.open(current_path),
                dark_image=Image.open(current_path),
                size=(150, 150)
            )

            self.label_image = ctk.CTkLabel(self, image=self.image, text="")
        except Exception as e:
            self.label_image = ctk.CTkLabel(self, text="ERRO: Não foi possível encontrar a imagem.")
        finally:
            self.label_image.grid(row=1, column=0, padx=20, pady=10, columnspan=3, sticky="nsew")

        # Configurando as colunas da página
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=3)
        self.grid_columnconfigure(2, weight=1)

        # Configurando as linhas da página
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(4, weight=1)

        # Vamos colocar todos os labels e entrys (além do botão de entrar) em um container, isso deixará os componentes centralizados em relação à página
        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.grid(row=3, column=0, padx=200, pady=10, columnspan=3, sticky="ew")
        self.container.grid_columnconfigure(0, weight=1)

        # Adicionando os componentes para inserção da identificação de usuário
        self.label_login = ctk.CTkLabel(self.container, text="Login")
        self.label_login.grid(row=0, column=0, pady=0, sticky="w")

        self.entry_login = ctk.CTkEntry(self.container)
        self.entry_login.grid(row=1, column=0, pady=5, sticky="ew")

        # Adicionando os componentes para inserção da senha
        self.label_password = ctk.CTkLabel(self.container, text="Senha")
        self.label_password.grid(row=3, column=0, pady=(10, 0), sticky="w")

        self.container_password = ctk.CTkFrame(self.container, fg_color="transparent")
        self.container_password.grid(row=4, column=0, pady=5, sticky="nsew")

        self.container_password.grid_columnconfigure(0, weight=1)
        self.container_password.grid_columnconfigure(1, weight=0)

        self.entry_password = ctk.CTkEntry(self.container_password, show="*")
        self.entry_password.grid(row=0, column=0, padx=(0, 5), sticky="ew")

        self.button_password = ctk.CTkButton(self.container_password, text="", fg_color="#2b2f76", width=50, command=self.reveal_password)
        self.button_password.grid(row=0, column=1)

        # Adicionando botões
        self.open_create = open_create  # Guardando função para abrir a página de 'criar conta'
        self.open_dashboard = open_dashboard  # Guardando metodo para abrir a página principal do programa

        self.button_enter = ctk.CTkButton(self.container, text="Entrar", fg_color="#2b2f76", command=self.enter) # Botão de 'entrar'
        self.button_enter.grid(row=6, column=0, pady=20)

        self.button_create = ctk.CTkButton(self, text="Não tem conta?", fg_color="#2b2f76", command=self.create_account) # Botão de 'criar conta'
        self.button_create.grid(row=5, column=2, padx=20, pady=20, sticky="se")


    def reveal_password(self):  # Método para revelar ou esconder a senha digitada
        if self.entry_password.cget("show") == "*":
            self.entry_password.configure(show="")
        else:
            self.entry_password.configure(show="*")


    def create_account(self):  # Método para abrir a página de "Criar conta"
        self.destroy()
        self.open_create()


    def enter(self):
        login = self.entry_login.get()
        password = self.entry_password.get()

        if login == "admin" and password == "1234":
            self.destroy()
            self.open_dashboard()
        # elif isUser(login, password):

        else:
            show_messagebox()

