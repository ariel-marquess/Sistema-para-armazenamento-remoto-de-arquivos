import customtkinter as ctk

import client.application.utils.ul as util
import client.application.controls.ctrl as ctrl 
import client.protocols.open_data as openData # Importa o protocolo para buscar os dados iniciais

class Login(ctk.CTkFrame):
    def __init__(self, master, open_create, open_dashboard):
        super().__init__(master)

        self.configure(fg_color="#252525")
        self.grid(row=1, column=0, sticky="nsew")

        # Adicionando a imagem da página
        self.label_image = ctk.CTkLabel(self, image=util.images("file", 150), text="")
        self.label_image.grid(row=1, column=0, padx=20, pady=10, columnspan=3, sticky="nsew")

        # Configurando as colunas da página
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=3)
        self.grid_columnconfigure(2, weight=1)

        # Configurando as linhas da página
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(4, weight=1)

        self.open_create = open_create
        self.open_dashboard = open_dashboard

        # Container para os componentes de login
        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.grid(row=3, column=0, padx=200, pady=10, columnspan=3, sticky="ew")
        self.container.grid_columnconfigure(0, weight=1)

        # Componentes de usuário e senha
        self.label_login = ctk.CTkLabel(self.container, text="Login")
        self.label_login.grid(row=0, column=0, pady=0, sticky="w")
        self.entry_username = ctk.CTkEntry(self.container, placeholder_text="Se estiver testando os gráficos, deixe em branco.")
        self.entry_username.grid(row=1, column=0, pady=5, sticky="ew")
        self.label_password = ctk.CTkLabel(self.container, text="Senha")
        self.label_password.grid(row=3, column=0, pady=(10, 0), sticky="w")
        self.entry_password = ctk.CTkEntry(self.container, show="*", placeholder_text="Se estiver testando os gráficos, deixe em branco.")
        self.entry_password.grid(row=4, column=0, pady=5, sticky="ew")

        # Botões
        self.button_enter = ctk.CTkButton(self.container, text="Entrar", fg_color="#2b2f76", command=self.enter)
        self.button_enter.grid(row=6, column=0, pady=20)
        self.button_create = ctk.CTkButton(self, text="Não tem conta?", fg_color="#2b2f76", command=self.create_account)
        self.button_create.grid(row=5, column=2, padx=20, pady=20, sticky="se")

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
            # Mantém a lógica de teste se os campos estiverem vazios
            mock_data = {
                'name': ['Downloads', 'Documentos', 'Imagens', 'curriculo.txt'],
                'size': ['3 itens', '2 itens', '5 itens', '23 kB'],
                'type': ['pasta', 'pasta', 'pasta', 'arquivo']
            }
            session_data = {
                "username": "tester",
                "content": mock_data
            }
            self.dashboard(session_data)
