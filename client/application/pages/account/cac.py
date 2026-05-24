import customtkinter as ctk

import client.application.controls.ctrl as ctrl # Importando o novo controle unificado
import client.application.utils.ul as util


class Create(ctk.CTkFrame):
    def __init__(self, master, open_login):
        super().__init__(master)

        self.configure(fg_color="#252525")
        self.grid(row=1, column=0, sticky="nsew")

        # Configurando colunas da página
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)

        # Configurando as linhas da página
        self.grid_rowconfigure(3, weight=1)
        self.grid_rowconfigure(9, weight=1)
        self.grid_rowconfigure(10, weight=1)

        # Adicionando o título da página
        self.label_title = ctk.CTkLabel(self, text="Criando uma nova conta", font=("Roboto", 24, "bold"))
        self.label_title.grid(row=0, column=0, pady=30, columnspan=3)

        # Optamos por colocar os componentes label e entry da parte de "nome completo" e "nome de usuário" em um container próprio.
        # Isso foi feito somente para fins de formatação da página.
        self.container_info = ctk.CTkFrame(self, fg_color="transparent")
        self.container_info.grid(row=1, column=0, padx=10, columnspan=3, sticky="ew")
        self.container_info.grid_columnconfigure(0, weight=1)
        self.container_info.grid_columnconfigure(1, weight=1)
        self.container_info.grid_columnconfigure(2, weight=1)

        self.label_fullName = ctk.CTkLabel(self.container_info, text="Nome completo")
        self.label_fullName.grid(row=0, column=0, pady=5, padx=10, sticky="w")

        self.entry_fullName = ctk.CTkEntry(self.container_info)
        self.entry_fullName.grid(row=1, column=0, padx=10, columnspan=2, sticky="ew")

        self.label_userName = ctk.CTkLabel(self.container_info, text="Nome de usuário")
        self.label_userName.grid(row=0, column=2, pady=5, padx=10, sticky="w")

        self.entry_userName = ctk.CTkEntry(self.container_info)
        self.entry_userName.grid(row=1, column=2, padx=10, sticky="ew")

        # Os campos de IP e Porta não são mais necessários no front-end,
        # pois estão centralizados no ctrl.py, mas os mantemos por enquanto para não quebrar o layout.
        # Em uma futura refatoração, podem ser removidos.
        self.container_address = ctk.CTkFrame(self, fg_color="transparent")
        self.container_address.grid(row=2, column=0, padx=20, pady=10, columnspan=3, sticky="ew")
        self.container_address.grid_columnconfigure(0, weight=1)
        self.container_address.grid_columnconfigure(1, weight=1)
        self.container_address.grid_columnconfigure(2, weight=1)
        self.container_address.grid_columnconfigure(3, weight=1)

        self.label_IP = ctk.CTkLabel(self.container_address, text="Endereço IP da máquina")
        self.label_IP.grid(row=0, column=0, sticky="w")

        self.entry_IP = ctk.CTkEntry(self.container_address)
        self.entry_IP.grid(row=1, column=0, sticky="ew")

        self.label_port = ctk.CTkLabel(self.container_address, text="Porta")
        self.label_port.grid(row=0, column=1, padx=10, sticky="w")

        self.entry_port = ctk.CTkEntry(self.container_address)
        self.entry_port.grid(row=1, column=1, padx=10, sticky="ew")

        # Parte para definição da senha
        self.label_password = ctk.CTkLabel(self, text="Senha")
        self.label_password.grid(row=4, column=0, padx=20, sticky="w")

        self.entry_password = ctk.CTkEntry(self, show="*")
        self.entry_password.grid(row=5, column=0, padx=20, sticky="ew")

        self.label_confirmPassword = ctk.CTkLabel(self, text="Confirmar senha")
        self.label_confirmPassword.grid(row=6, column=0, padx=20, sticky="w")

        self.entry_confirmPassword = ctk.CTkEntry(self, show="*")
        self.entry_confirmPassword.grid(row=7, column=0, padx=20, sticky="ew")

        self.checkBox_seePassword = ctk.CTkCheckBox(self, text="Mostrar senha", command=self.reveal_password)
        self.checkBox_seePassword.grid(row=8, column=0, padx=20, pady=10)

        self.open_login = page_login   # Método que abrirá a página de login

        # Botão para submissão das informações
        self.button_createAccount = ctk.CTkButton(self, fg_color="#2b2f76", text="Criar conta", command=self.create)
        self.button_createAccount.grid(row=11, column=2, padx=20, pady=20, sticky="e")


    def reveal_password(self):
        if self.entry_password.cget("show") == "*":
            self.entry_password.configure(show="")
            self.entry_confirmPassword.configure(show="")
        else:
            self.entry_password.configure(show="*")
            self.entry_confirmPassword.configure(show="*")


    def login(self):
        self.destroy()
        self.open_login()


    def create(self):
        infos = {
            'username': self.entry_userName.get(),
            'password': self.entry_password.get(),
            'confirmation_password': self.entry_confirmPassword.get()
        }

        if infos.get('username') != "" and infos.get('password') != "" and infos.get('confirmation_password') != "":
            if infos.get('username').isalnum():
                if infos.get('password') == infos.get('confirmation_password'):
                    # A verificação de usuário existente é feita no servidor
                    if ctrl.record(infos):   # Registrando informações no servidor
                        self.login()
                    else:
                        # A função record() já imprime a falha, mas podemos mostrar uma msg pro usuário
                        util.MessageBox(
                            title="Falha na Criação",
                            message="ERRO: Não foi possível criar a conta. O nome de usuário pode já existir.",
                            icon="warning"
                        )
                else:
                    util.MessageBox(
                        title="Senhas não coincidem",
                        message="ERRO: A senha e a confirmação de senha não são iguais.",
                        icon="warning"
                    )
            else:
                util.MessageBox(
                    title="Nome de usuário inválido",
                    message="ERRO: o nome de usuário não pode conter caracteres especiais, pontuações, letras acentuadas ou espaços.",
                    icon="warning"
                )
        else:
            util.MessageBox(
                title="Informações faltantes",
                message="ERRO: você não preencheu todos os campos apontados na página.",
                icon="warning"
            )