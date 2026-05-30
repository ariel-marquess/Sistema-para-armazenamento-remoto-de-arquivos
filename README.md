# Sistema de Armazenamento Remoto com Sockets TCP

Este projeto implementa um sistema de armazenamento remoto, semelhante a um Drive simples, usando a arquitetura cliente/servidor com sockets TCP. Ele foi desenvolvido como atividade avaliativa da disciplina de Redes de Computadores.

O objetivo principal é aplicar conceitos de comunicação em rede, transferência confiável de dados, autenticação básica, gerenciamento de diretórios e persistência de arquivos em disco.

## Tecnologias Utilizadas

- Python 3
- `socket` para comunicação TCP
- JSON para troca de mensagens entre cliente e servidor
- Base64 para transporte de arquivos binários
- `customtkinter` para a interface gráfica do cliente

## Funcionalidades Implementadas

- **Autenticação de Usuário:** Sistema completo de criação de conta e login.
- **Armazenamento Dedicado:** Cada usuário possui uma pasta dedicada e isolada no servidor.
- **Listagem de Arquivos e Pastas:** O cliente exibe o conteúdo do diretório atual do usuário.
- **Navegação de Pastas:** O usuário pode entrar em subpastas e retornar ao diretório anterior.
- **Upload de Arquivos:** O cliente pode enviar arquivos para o servidor.
- **Download de Arquivos:** O cliente pode baixar arquivos do servidor para sua máquina local.
- **Criação de Pastas:** O cliente pode criar novas pastas no seu espaço de armazenamento.
- **Exclusão de Arquivos:** O cliente pode apagar arquivos permanentemente do servidor.
- **Visualização de Arquivos de Texto:** O cliente pode abrir e visualizar o conteúdo de arquivos de texto.

## Execução do Projeto

### Servidor
1. Navegue até a pasta `server/`.
2. Execute o servidor: `python3 server.py`.
3. O servidor escutará na porta `65432`.

### Cliente
1. Navegue até a **raiz do projeto**.
2. Execute o cliente como um módulo: `python3 -m client.application.pages.main`.
3. A interface gráfica será iniciada.

## Estrutura do Projeto

```text
.
├── client/
│   ├── application/
│   └── protocols/
├── server/
│   ├── server.py
│   ├── user_manager.py
│   ├── file_manager.py
│   └── storage/
└── README.md
```

## Protocolo de Comunicação

A comunicação é feita com JSON sobre sockets TCP. Toda requisição possui um campo `"command"` e os dados necessários. O servidor responde com um JSON contendo `"status": "success"` ou `"status": "error"`.

### Comandos Suportados

- `create_account`
- `login`
- `list_folder`
- `create_folder`
- `read_file`
- `delete_file`
- `upload_file`
- `download_file`

<details>
<summary><b>Clique para ver a Documentação Detalhada do Protocolo</b></summary>

### Criar Conta
- **Comando:** `create_account`
- **Payload:** `{"username": "ana", "password": "123"}`

### Login
- **Comando:** `login`
- **Payload:** `{"username": "ana", "password": "123"}`

### Listar Pasta
- **Comando:** `list_folder`
- **Payload:** `{"username": "ana", "path": ""}` (path vazio para a raiz)

### Criar Pasta
- **Comando:** `create_folder`
- **Payload:** `{"username": "ana", "path": "", "folder_name": "Documentos"}`

### Ler Arquivo
- **Comando:** `read_file`
- **Payload:** `{"username": "ana", "path": "Documentos/nota.txt"}`

### Apagar Arquivo
- **Comando:** `delete_file`
- **Payload:** `{"username": "ana", "path": "Documentos/nota.txt"}`

### Upload de Arquivo
- **Comando:** `upload_file`
- **Payload:** `{"username": "ana", "path": "imagem.png", "content": "BASE64_DO_ARQUIVO", "encoding": "base64"}`

### Download de Arquivo
- **Comando:** `download_file`
- **Payload:** `{"username": "ana", "path": "Documentos/nota.txt"}`

</details>

<br>

<details>
<summary><b>Clique para ver as Instruções de Configuração do Ambiente (VirtualBox + Debian)</b></summary>

## Parte 1: Configuração da VM (Passo único por VM)

Estes passos são necessários para AMBAS as máquinas virtuais (servidor e cliente).

### 1.1. Habilitar Repositórios Adicionais do Debian

1.  Edite o arquivo `/etc/apt/sources.list` e adicione `contrib non-free non-free-firmware` ao final de cada linha `deb`.
2.  Rode `sudo apt update`.

### 1.2. Instalar o VirtualBox Guest Additions

1.  **Instale as dependências:** `sudo apt install -y build-essential dkms linux-headers-$(uname -r)`.
2.  No menu da VM, vá em **Dispositivos > Inserir imagem de CD dos Adicionais para Convidado...**.
3.  **Monte e execute:** `sudo mount /dev/cdrom /media/cdrom` e depois `sudo sh /media/cdrom/VBoxLinuxAdditions.run`.

### 1.3. Configurar Pasta Compartilhada

1.  **No VirtualBox:** Vá em **Configurações da VM > Pastas Compartilhadas** e adicione a pasta raiz do projeto, marcando "Montar Automaticamente" e "Tornar Permanente". Dê um nome simples (ex: `projeto_drive`).
2.  **Na VM:** Crie o grupo `vboxsf` (`sudo groupadd vboxsf`), adicione seu usuário a ele (`sudo adduser $USER vboxsf`) e reinicie (`sudo reboot`).

## Parte 2: Instalação de Dependências do Cliente

Estes passos são necessários **apenas na VM do Cliente**.

### 2.1. Instalar Ambiente Gráfico

Se sua VM está em modo texto, instale uma interface gráfica.
1.  **Instale o Xfce:** `sudo apt install -y xfce4 xfce4-goodies`.
2.  **Reinicie:** `sudo reboot`. A VM iniciará em modo gráfico.
3.  **Solução de Problemas:** Se a UI não abrir com erro de `no display`, use o comando `startx` para forçar o início do ambiente gráfico e abra um terminal de dentro dele.

### 2.2. Instalar Pacotes Python

1.  **Instale o `pip` e o `tkinter`:** `sudo apt install -y python3-pip python3-tk`.
2.  **Instale as bibliotecas da UI:**
    ```bash
    pip3 install Pillow --break-system-packages
    pip3 install CTkMessagebox --break-system-packages
    ```
</details>
