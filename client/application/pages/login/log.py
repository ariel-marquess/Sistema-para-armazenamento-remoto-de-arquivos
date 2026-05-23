import customtkinter as ctk

import client.application.util.ul as util
import client.application.controls.ctrl as ctrl # Importando os controles

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

        self.open_create = open_create  # Guardando função para abrir a página de 'criar conta'
        self.open_dashboard = open_dashboard  # Guardando metodo para abrir a página principal do programa

        # Vamos colocar todos os labels e entrys (além do botão de entrar) em um container, isso deixará os componentes centralizados em relação à página
        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.grid(row=3, column=0, padx=200, pady=10, columnspan=3, sticky="ew")
        self.container.grid_columnconfigure(0, weight=1)

        # Adicionando os componentes para inserção da identificação de usuário
        self.label_login = ctk.CTkLabel(self.container, text="Login")
        self.label_login.grid(row=0, column=0, pady=0, sticky="w")

        self.entry_username = ctk.CTkEntry(self.container, placeholder_text="Se estiver testando os gráficos, deixe em branco.")
        self.entry_username.grid(row=1, column=0, pady=5, sticky="ew")

        # Adicionando os componentes para inserção da senha
        self.label_password = ctk.CTkLabel(self.container, text="Senha")
        self.label_password.grid(row=3, column=0, pady=(10, 0), sticky="w")

        self.container_password = ctk.CTkFrame(self.container, fg_color="transparent")
        self.container_password.grid(row=4, column=0, pady=5, sticky="nsew")
        self.container_password.grid_columnconfigure(0, weight=1)
        self.container_password.grid_columnconfigure(1, weight=0)

        self.entry_password = ctk.CTkEntry(self.container_password, show="*", placeholder_text="Se estiver testando os gráficos, deixe em branco.")
        self.entry_password.grid(row=0, column=0, padx=(0, 5), sticky="ew")

        self.button_password = ctk.CTkButton(self.container_password, text="", fg_color="#2b2f76", image=util.images("eclosed"), width=50, command=self.reveal_password)
        self.button_password.grid(row=0, column=1)

        # Adicionando botões
        self.button_enter = ctk.CTkButton(self.container, text="Entrar", fg_color="#2b2f76", command=self.enter)    # Botão de 'entrar'
        self.button_enter.grid(row=6, column=0, pady=20)

        self.button_create = ctk.CTkButton(self, text="Não tem conta?", fg_color="#2b2f76", command=self.create_account)    # Botão de 'criar conta'
        self.button_create.grid(row=5, column=2, padx=20, pady=20, sticky="se")


    def reveal_password(self):  # Método para revelar ou esconder a senha digitada
        if self.entry_password.cget("show") == "*":
            self.button_password.configure(image=util.images("eclosed"))
            self.entry_password.configure(show="")
        else:
            self.button_password.configure(image=util.images("eopen"))
            self.entry_password.configure(show="*")


    def create_account(self):  # Método para abrir a página de "Criar conta"
        self.destroy()
        self.open_create()


    def dashboard(self, data):
        self.destroy()
        self.open_dashboard(data)


    def enter(self):
        username = self.entry_username.get()
        password = self.entry_password.get()

        if username != "" and password != "":
            if ctrl.isUser(username, password):
                # A lógica para buscar os dados do dashboard ainda precisa ser implementada
                # Por enquanto, passamos dados de exemplo.
                mock_data = {
                    'name': ['Downloads', 'Documentos', 'Imagens', 'curriculo.txt'],
                    'size': ['3 itens', '2 itens', '5 itens', '23 kB'],
                    'type': ['pasta', 'pasta', 'pasta', 'arquivo']
                }
                self.dashboard(mock_data)
            else:
                util.MessageBox(
                    title="Inconsistência de dados",
                    message="ERRO: usuário ou senha incorretos.",
                    icon="warning"
                )
        else:
            mock_data = {
                'name': ['Downloads', 'Documentos', 'Imagens', 'curriculo.txt'],
                'size': ['3 itens', '2 itens', '5 itens', '23 kB'],
                'type': ['pasta', 'pasta', 'pasta', 'arquivo']
            }
            self.dashboard(mock_data)
            """
            Ao finalizar o programa este bloco ficará com o seguinte código:
            
            util.MessageBox(
                title="Campos vazios",
                message="ERRO: Preencha todos os campos.",
                icon="warning"
            )
            """