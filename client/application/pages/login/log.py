import customtkinter as ctk

import client.application.utils.ul as util
import client.application.controls.ctrl as ctrl 
import client.protocols.open_data as openData # Importa o protocolo para buscar os dados iniciais

class Login(ctk.CTkFrame):
    def __init__(self, master, open_create, open_dashboard):
        super().__init__(master)

        self.configure(fg_color="#252525")
        self.grid(row=1, column=0, sticky="nsew")

        # Configurando as colunas da página
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=3)
        self.grid_columnconfigure(2, weight=1)

        # Configurando as linhas da página
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(4, weight=1)

        self.open_create = open_create
        self.open_dashboard = open_dashboard

        # Estilos do texto
        self.textFont = util.font(14)
        self.textColor = "white"

        # Adicionando a imagem da página
        self.label_image = ctk.CTkLabel(self, image=util.images("file", 150), text="")
        self.label_image.grid(row=1, column=0, padx=20, pady=10, columnspan=3, sticky="nsew")

        # Vamos colocar todos os labels e entrys (além do botão de entrar) em um container, isso deixará os componentes centralizados em relação à página
        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.grid(row=3, column=0, padx=200, pady=10, columnspan=3, sticky="ew")
        self.container.grid_columnconfigure(0, weight=1)

        # Adicionando os componentes para inserção da identificação de usuário
        self.label_login = ctk.CTkLabel(self.container, text="Login", font=self.textFont, text_color=self.textColor)
        self.label_login.grid(row=0, column=0, pady=0, sticky="w")
        self.entry_username = ctk.CTkEntry(self.container, placeholder_text="Digite seu nome de usuário")
        self.entry_username.grid(row=1, column=0, pady=5, sticky="ew")
        self.entry_username.bind("<Return>", lambda e: self.enter())

        # Adicionando os componentes para inserção da senha
        self.label_password = ctk.CTkLabel(self.container, text="Senha", font=self.textFont, text_color=self.textColor)
        self.label_password.grid(row=3, column=0, pady=(10, 0), sticky="w")

        self.container_password = ctk.CTkFrame(self.container, fg_color="transparent")
        self.container_password.grid(row=4, column=0, pady=5, sticky="nsew")
        self.container_password.grid_columnconfigure(0, weight=1)
        self.container_password.grid_columnconfigure(1, weight=0)

        self.entry_password = ctk.CTkEntry(self.container_password, show="*", placeholder_text="Digite sua senha")
        self.entry_password.grid(row=0, column=0, padx=(0, 5), sticky="ew")
        self.entry_password.bind("<Return>", lambda e: self.enter())

        self.button_password = ctk.CTkButton(self.container_password, text="", fg_color="#2b2f76", image=util.images("eclosed"), width=50, command=self.reveal_password)
        self.button_password.grid(row=0, column=1)

        # Adicionando botões
        self.button_enter = ctk.CTkButton(self.container, text="Entrar", fg_color="#2b2f76", text_color=self.textColor, command=self.enter)    # Botão de 'entrar'
        self.button_enter.grid(row=6, column=0, pady=20)

        self.button_create = ctk.CTkButton(self, text="Não tem conta?", fg_color="#2b2f76", text_color=self.textColor, command=self.create_account)    # Botão de 'criar conta'
        self.button_create.grid(row=5, column=2, padx=20, pady=20, sticky="se")

    def reveal_password(self):
        if self.entry_password.cget("show") == "*":
            self.entry_password.configure(show="")
            self.button_password.configure(image=util.images("eopen"))
        else:
            self.entry_password.configure(show="*")
            self.button_password.configure(image=util.images("eclosed"))

    def create_account(self):
        self.destroy()
        self.open_create()

    def dashboard(self, session_data):
        self.destroy()
        self.open_dashboard(session_data)

    def enter(self):
        username = self.entry_username.get()
        password = self.entry_password.get()

        if username != "" and password != "":
            if ctrl.isUser(username, password):
                # Login bem-sucedido, busca os dados da pasta raiz do usuário
                root_content = openData.openFolder(username, "") # "" para a raiz
                
                if root_content is not None:
                    session_data = {
                        "username": username,
                        "content": root_content
                    }
                    self.dashboard(session_data)
                else:
                    util.MessageBox(
                        title="Erro ao Carregar Dados",
                        message="ERRO: Não foi possível carregar os arquivos do usuário após o login.",
                        icon="warning"
                    )
            else:
                util.MessageBox(
                    title="Inconsistência de Dados",
                    message="ERRO: usuário ou senha incorretos.",
                    icon="warning"
                )
        else:
            util.MessageBox(
                title="Informações faltantes",
                message="ERRO: preencha o login e a senha para entrar.",
                icon="warning"
            )
