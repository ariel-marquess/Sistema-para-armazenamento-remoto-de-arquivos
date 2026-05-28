# Sistema de Armazenamento Remoto com Sockets TCP

Este projeto implementa um sistema de armazenamento remoto, semelhante a um Drive simples, usando a arquitetura cliente/servidor com sockets TCP. Ele foi desenvolvido como atividade avaliativa da disciplina de Redes de Computadores.

O objetivo principal é aplicar conceitos de comunicação em rede, transferência confiável de dados, autenticação básica, gerenciamento de diretórios e persistência de arquivos em disco.

## Contexto da Atividade

A atividade propõe o desenvolvimento de um sistema de Drive usando sockets TCP, com cliente e servidor executando em máquinas virtuais diferentes, preferencialmente usando Debian no VirtualBox.

O projeto explora:

- programação de aplicações em rede;
- modelo cliente-servidor;
- gerenciamento de conexões TCP;
- criação de um protocolo simples de aplicação;
- autenticação básica;
- listagem de arquivos;
- upload e download;
- persistência dos dados no disco da VM do servidor.

## Tecnologias Utilizadas

- Python 3
- `socket` para comunicação TCP
- JSON para troca de mensagens entre cliente e servidor
- Base64 para transporte de arquivos binários
- `customtkinter` para a interface gráfica do cliente
- `Pillow` para carregar imagens da interface
- `CTkMessagebox` para mensagens gráficas
- VirtualBox para executar cliente e servidor em VMs diferentes
- Debian/Linux como ambiente recomendado

## Estrutura do Projeto

```text
.
├── client/
│   ├── application/
│   │   ├── controls/
│   │   │   └── ctrl.py
│   │   ├── pages/
│   │   │   ├── account/
│   │   │   ├── dashboard/
│   │   │   ├── login/
│   │   │   └── main.py
│   │   └── util/
│   │       └── ul.py
│   ├── images/
│   └── protocols/
│       ├── check_user.py
│       ├── record_data.py
│       ├── open_data.py
│       ├── file_handler.py
│       └── creators/
│           └── mkdir.py
├── server/
│   ├── server.py
│   ├── data/
│   └── storage/
├── shell/
├── README-HEITOR.md
└── README.md
```

## Visão Geral

O sistema é dividido em duas partes:

- **Servidor:** recebe conexões TCP, processa comandos em JSON, gerencia usuários e manipula arquivos no disco.
- **Cliente:** fornece uma interface gráfica para login, criação de conta e navegação pelos arquivos.

O servidor escuta na porta `65432` e usa o host `0.0.0.0`, permitindo conexões vindas de outras máquinas da rede.

## Servidor

O arquivo principal do servidor é:

```text
server/server.py
```

Ele é responsável por:

- abrir o socket TCP;
- aceitar conexões de clientes;
- receber mensagens JSON;
- identificar o comando solicitado;
- executar operações de autenticação e armazenamento;
- responder ao cliente em JSON.

Os dados persistentes ficam em:

```text
server/storage/
```

O arquivo de usuários fica em:

```text
server/storage/users.json
```

Cada usuário possui uma pasta própria:

```text
server/storage/
├── users.json
├── ana/
│   ├── nota.txt
│   └── Documentos/
└── joao/
    └── imagem.png
```

## Cliente

O arquivo principal do cliente gráfico é:

```text
client/application/pages/main.py
```

Ele cria a janela principal e alterna entre:

- tela de login;
- tela de criação de conta;
- dashboard de arquivos.

Os arquivos de protocolo do cliente ficam em:

```text
client/protocols/
```

Eles representam a camada que deve conversar com o servidor:

- `check_user.py`: login;
- `record_data.py`: criação de conta;
- `open_data.py`: listagem e abertura de dados;
- `file_handler.py`: upload, download e exclusão;
- `creators/mkdir.py`: criação de pastas.

## Protocolo de Comunicação

A comunicação entre cliente e servidor é feita com JSON sobre sockets TCP.

Toda requisição possui o campo `command`:

```json
{
  "command": "nome_do_comando"
}
```

Resposta de sucesso:

```json
{
  "status": "success"
}
```

Resposta de erro:

```json
{
  "status": "error",
  "message": "Descrição do erro."
}
```

## Comandos Implementados no Servidor

### Criar Conta

Cria um novo usuário e uma pasta exclusiva para ele.

```json
{
  "command": "create_account",
  "username": "ana",
  "password": "123"
}
```

Resposta:

```json
{
  "status": "success",
  "message": "Conta criada com sucesso."
}
```

### Login

Verifica usuário e senha.

```json
{
  "command": "login",
  "username": "ana",
  "password": "123"
}
```

Resposta:

```json
{
  "status": "success",
  "message": "Login bem-sucedido."
}
```

### Listar Pasta

Lista arquivos e pastas dentro do espaço do usuário.

```json
{
  "command": "list_folder",
  "username": "ana",
  "path": ""
}
```

Resposta:

```json
{
  "status": "success",
  "data": {
    "name": ["Documentos", "nota.txt"],
    "size": ["0 itens", "12 bytes"],
    "type": ["pasta", "arquivo"]
  }
}
```

O campo `path` é relativo à pasta do usuário. Para listar a raiz, use `""`.

### Criar Pasta

Cria uma pasta dentro do espaço do usuário.

```json
{
  "command": "create_folder",
  "username": "ana",
  "path": "",
  "folder_name": "Documentos"
}
```

Também são aceitos `folderName` ou `name` no lugar de `folder_name`.

Resposta:

```json
{
  "status": "success",
  "message": "Pasta criada com sucesso."
}
```

### Ler Arquivo

Lê o conteúdo textual de um arquivo UTF-8.

```json
{
  "command": "read_file",
  "username": "ana",
  "path": "Documentos/nota.txt"
}
```

Resposta:

```json
{
  "status": "success",
  "data": "Conteúdo do arquivo"
}
```

Esse comando é indicado para visualizar arquivos de texto. Para baixar qualquer tipo de arquivo, use `download_file`.

### Apagar Arquivo

Remove um arquivo do usuário.

```json
{
  "command": "delete_file",
  "username": "ana",
  "path": "Documentos/nota.txt"
}
```

Resposta:

```json
{
  "status": "success",
  "message": "Arquivo apagado com sucesso."
}
```

Esse comando apaga apenas arquivos. Ele não remove pastas.

### Upload de Arquivo

Salva no servidor um arquivo enviado pelo cliente.

Upload de texto:

```json
{
  "command": "upload_file",
  "username": "ana",
  "path": "Documentos/nota.txt",
  "content": "Conteúdo do arquivo"
}
```

Upload binário usando Base64:

```json
{
  "command": "upload_file",
  "username": "ana",
  "path": "imagem.png",
  "content": "BASE64_DO_ARQUIVO",
  "encoding": "base64"
}
```

Também é possível informar pasta e nome separadamente:

```json
{
  "command": "upload_file",
  "username": "ana",
  "path": "Documentos",
  "file_name": "nota.txt",
  "content": "Texto"
}
```

Também são aceitos `fileName` ou `name` no lugar de `file_name`.

Por padrão, o servidor não sobrescreve arquivos existentes. Para permitir sobrescrita:

```json
{
  "command": "upload_file",
  "username": "ana",
  "path": "Documentos/nota.txt",
  "content": "Novo conteúdo",
  "overwrite": true
}
```

Resposta:

```json
{
  "status": "success",
  "message": "Arquivo enviado com sucesso.",
  "size": 13
}
```

### Download de Arquivo

Retorna um arquivo do servidor codificado em Base64.

```json
{
  "command": "download_file",
  "username": "ana",
  "path": "Documentos/nota.txt"
}
```

Resposta:

```json
{
  "status": "success",
  "file_name": "nota.txt",
  "size": 13,
  "encoding": "base64",
  "data": "Q29udGV1ZG8="
}
```

O cliente deve decodificar `data` de Base64 e salvar os bytes no disco da VM cliente.

## Segurança de Caminhos

Todas as operações de arquivo usam caminhos relativos à pasta do usuário.

O servidor bloqueia tentativas de acessar arquivos fora dessa pasta, como:

```json
{
  "command": "read_file",
  "username": "ana",
  "path": "../users.json"
}
```

Resposta esperada:

```json
{
  "status": "error",
  "message": "Caminho inválido."
}
```

Essa validação impede que o cliente acesse arquivos internos do servidor ou arquivos de outros usuários.

