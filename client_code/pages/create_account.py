import customtkinter as ctk
from CTkMessagebox import CTkMessagebox

from client_code.controls.check_user import isUsername
from client_code.controls.record_data import record


def MessageBox(title, message, icon):   # Método que cria uma caixa de mensagem quando executado
    box = CTkMessagebox(title=title, message=message, icon=icon)


class Create(ctk.CTk):
    def __init__(self, page_login):
        super().__init__()

        self.geometry("800x600")
        self.title("Drive Docs")

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

        # Container para inserção dos componetes para incerção do endereço da máquina atual (a que se conectará ao servidor)
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


    def create(self):
        infos = {
            'full name': self.entry_fullName.get(),
            'username': self.entry_userName.get(),
            'address': self.entry_IP.get(),
            'port': self.entry_port.get(),
            'password': self.entry_password.get(),
            'confirmation password': self.entry_confirmPassword.get()
        }

        if infos.get('full name') != "" and infos.get('username') != "" and infos.get('address') != "" and infos.get('port') != "" and infos.get('password') != "" and infos.get('confirmation password') != "":   # Verifica se todos os campos da página foram preenchidos
            if infos.get('username').isalnum():
                if not isUsername(infos.get('username')):
                    if infos.get('password') == infos.get('confirmation password'):
                        del infos['full name'], infos['address'], infos['port'], infos['confirmation password']   # Essas informações foram utilizadas somente para verificação ou para o processo chamado "encher linguiça" (não são necessárias no servidor).

                        try:
                            record(infos)   # Registrando informações no servidor

                            self.destroy()
                            self.open_login()   # Abrindo novamente a página de login
                        except Exception as e:
                            MessageBox(
                                title="Ocorreu um erro inesperado",
                                message=f'ERRO: {e}',
                                icon="warning"
                            )
                else:
                    MessageBox(
                        title="Nome de usuário já existente",
                        message="ERRO: o nome de usuário digitado já está registrado no servidor.",
                        icon="warning"
                    )
            else:
                MessageBox(
                    title="Nome de usuário inválido",
                    message="ERRO: o nome de usuário não pode conter coracteres especiais, pontuações, letras acentuadas ou espaços.",
                    icon="warning"
                )
        else:
            MessageBox(
                title="Informações faltantes",
                message="ERRO: você não preencheu todos os campos apontados na página.",
                icon="warning"
            )

