import socket
import json
import os
import base64
import binascii

# --- Constantes ---
# O diretório base do servidor é o diretório onde este script está localizado.
SERVER_BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Tudo que for persistente no servidor fica dentro de "storage".
# dentro dessa pasta também ficam as pastas individuais dos usuários.
STORAGE_DIR = os.path.join(SERVER_BASE_DIR, "storage")
USERS_FILE = os.path.join(STORAGE_DIR, "users.json")

# Tamanho máximo de uma mensagem recebida pelo socket.
# Foi aumentado porque upload/download em JSON com Base64 gera mensagens maiores
# do que comandos simples como login e criação de conta.
BUFFER_SIZE = 10 * 1024 * 1024

# --- Funções de Gerenciamento de Usuários ---

def load_users():
    """Carrega os usuários do arquivo JSON. Retorna um dicionário de usuários."""
    if not os.path.exists(USERS_FILE):
        return {}
    try:
        with open(USERS_FILE, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return {}

def save_users(users):
    """Salva o dicionário de usuários no arquivo JSON."""
    os.makedirs(STORAGE_DIR, exist_ok=True) #Garante que o diretório de storage exista
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=4)

# --- Funções de Gerenciamento de Arquivos ---

def get_safe_user_path(username, relative_path=""):
    """
    Essa função transforma todos os caminhos em um caminho absoluto
    dentro de server/storage/<user>/.
    A checagem com startswith bloqueia tentativas como "../users.json",que poderiam acessar arquivos fora da pasta do usuário.
    """
    if not username:
        return None

    user_dir = os.path.abspath(os.path.join(STORAGE_DIR, username))
    requested_path = os.path.abspath(os.path.join(user_dir, relative_path or ""))

    if requested_path != user_dir and not requested_path.startswith(user_dir + os.sep):
        return None

    return requested_path

def format_folder_size(path):
    """Retorna a quantidade de itens dentro de uma pasta para exibir no cliente."""
    try:
        total_items = len(os.listdir(path))
    except OSError:
        total_items = 0

    return f"{total_items} itens"

def format_file_size(path):
    """Retorna o tamanho de um arquivo em bytes para exibir no cliente."""
    try:
        total_bytes = os.path.getsize(path)
    except OSError:
        total_bytes = 0

    return f"{total_bytes} bytes"

def is_valid_folder_name(folder_name):
    """
    Aqui o servidor aceita apenas o nome da pasta, não um caminho completo. Importante para evitar eventuais bugs.
    """
    if not isinstance(folder_name, str):
        return False

    folder_name = folder_name.strip()
    if not folder_name or folder_name in (".", ".."):
        return False

    return os.sep not in folder_name and (os.altsep is None or os.altsep not in folder_name)

def list_folder(username, relative_path=""):
    """
    Lista arquivos e pastas de um diretório do usuário.
    O retorno foi montado no formato que a interface gráfica espera: listas separadas para nome, tamanho e tipo.
    """
    users = load_users()
    if username not in users:
        return {"status": "error", "message": "Usuário não encontrado."}

    folder_path = get_safe_user_path(username, relative_path)
    if folder_path is None:
        return {"status": "error", "message": "Caminho inválido."}

    if not os.path.exists(folder_path):
        return {"status": "error", "message": "Pasta não encontrada."}

    if not os.path.isdir(folder_path):
        return {"status": "error", "message": "O caminho informado não é uma pasta."}

    folder_data = {
        "name": [],
        "size": [],
        "type": []
    }

    try:
        #Pastas aparecem antes dos arquivos, e ambos ficam em ordem alfabética.
        entries = sorted(os.scandir(folder_path), key=lambda entry: (not entry.is_dir(), entry.name.lower()))
        for entry in entries:
            folder_data["name"].append(entry.name)

            if entry.is_dir():
                folder_data["size"].append(format_folder_size(entry.path))
                folder_data["type"].append("pasta")
            else:
                folder_data["size"].append(format_file_size(entry.path))
                folder_data["type"].append("arquivo")
    except OSError as e:
        return {"status": "error", "message": f"Não foi possível listar a pasta: {e}"}

    return {"status": "success", "data": folder_data}

def create_folder(username, relative_path, folder_name):
    """
    Cria uma nova pasta dentro de um diretório do usuário, relative_path indica a pasta pai. folder_name indica
    somente o nome da nova pasta.
    """
    users = load_users()
    if username not in users:
        return {"status": "error", "message": "Usuário não encontrado."}

    if not is_valid_folder_name(folder_name):
        return {"status": "error", "message": "Nome de pasta inválido."}

    parent_path = get_safe_user_path(username, relative_path)
    if parent_path is None:
        return {"status": "error", "message": "Caminho inválido."}

    if not os.path.exists(parent_path):
        return {"status": "error", "message": "Pasta pai não encontrada."}

    if not os.path.isdir(parent_path):
        return {"status": "error", "message": "O caminho informado não é uma pasta."}

    new_folder_path = get_safe_user_path(username, os.path.join(relative_path or "", folder_name.strip()))
    if new_folder_path is None:
        return {"status": "error", "message": "Caminho inválido."}

    if os.path.exists(new_folder_path):
        return {"status": "error", "message": "Já existe um arquivo ou pasta com esse nome."}

    try:
        os.mkdir(new_folder_path)
    except OSError as e:
        return {"status": "error", "message": f"Não foi possível criar a pasta: {e}"}

    return {"status": "success", "message": "Pasta criada com sucesso."}

def read_file(username, relative_path):
    """
    Lê o conteúdo textual de um arquivo do usuário.
    Essa função é voltada para visualização de arquivos de texto no cliente.
    """
    users = load_users()
    if username not in users:
        return {"status": "error", "message": "Usuário não encontrado."}

    file_path = get_safe_user_path(username, relative_path)
    if file_path is None:
        return {"status": "error", "message": "Caminho inválido."}

    if not os.path.exists(file_path):
        return {"status": "error", "message": "Arquivo não encontrado."}

    if not os.path.isfile(file_path):
        return {"status": "error", "message": "O caminho informado não é um arquivo."}

    try:
        # Para visualização de texto, usamos o padrão UTF-8. Se o arquivo for binário
        # ou estiver em outra codificação, o servidor retorna erro controlado.
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
    except UnicodeDecodeError:
        return {"status": "error", "message": "O arquivo não é um texto UTF-8 válido."}
    except OSError as e:
        return {"status": "error", "message": f"Não foi possível ler o arquivo: {e}"}

    return {"status": "success", "data": content}

def delete_file(username, relative_path):
    """
    Apaga um arquivo do usuário.
    Por segurança, este comando não apaga pastas.
    """
    users = load_users()
    if username not in users:
        return {"status": "error", "message": "Usuário não encontrado."}

    file_path = get_safe_user_path(username, relative_path)
    if file_path is None:
        return {"status": "error", "message": "Caminho inválido."}

    if not os.path.exists(file_path):
        return {"status": "error", "message": "Arquivo não encontrado."}

    if not os.path.isfile(file_path):
        return {"status": "error", "message": "O caminho informado não é um arquivo."}

    try:
        os.remove(file_path)
    except OSError as e:
        return {"status": "error", "message": f"Não foi possível apagar o arquivo: {e}"}

    return {"status": "success", "message": "Arquivo apagado com sucesso."}

def upload_file(username, relative_path, content, encoding="text", overwrite=False):
    """
    Salva um arquivo enviado pelo cliente dentro da pasta do usuário. O protocolo aceita dois formatos:
    - encoding="text": o conteúdo vem como texto e é salvo em UTF-8;
    - encoding="base64": o conteúdo vem em Base64 e é salvo como bytes.

    Base64 foi usado porque a comunicação entre cliente e servidor está sendo
    feita com JSON, e JSON não transporta bytes binários diretamente.
    """
    users = load_users()
    if username not in users:
        return {"status": "error", "message": "Usuário não encontrado."}

    if not isinstance(relative_path, str) or not relative_path.strip():
        return {"status": "error", "message": "Caminho do arquivo inválido."}

    file_path = get_safe_user_path(username, relative_path)
    if file_path is None:
        return {"status": "error", "message": "Caminho inválido."}

    parent_path = os.path.dirname(file_path)
    if not os.path.exists(parent_path):
        return {"status": "error", "message": "Pasta de destino não encontrada."}

    if not os.path.isdir(parent_path):
        return {"status": "error", "message": "O destino informado não é uma pasta."}

    if os.path.isdir(file_path):
        return {"status": "error", "message": "Já existe uma pasta com esse nome."}

    if os.path.exists(file_path) and not overwrite:
        return {"status": "error", "message": "Já existe um arquivo com esse nome."}

    try:
        if encoding == "base64":
            if not isinstance(content, str):
                return {"status": "error", "message": "Conteúdo Base64 inválido."}
            file_content = base64.b64decode(content.encode("utf-8"), validate=True)
        else:
            if not isinstance(content, str):
                return {"status": "error", "message": "Conteúdo do arquivo inválido."}
            file_content = content.encode("utf-8")
    except (ValueError, binascii.Error):
        return {"status": "error", "message": "Conteúdo Base64 inválido."}

    try:
        with open(file_path, "wb") as f:
            f.write(file_content)
    except OSError as e:
        return {"status": "error", "message": f"Não foi possível salvar o arquivo: {e}"}

    return {
        "status": "success",
        "message": "Arquivo enviado com sucesso.",
        "size": len(file_content)
    }

def download_file(username, relative_path):
    #Retorna um arquivo do usuário codificado em Base64.

    users = load_users()
    if username not in users:
        return {"status": "error", "message": "Usuário não encontrado."}

    file_path = get_safe_user_path(username, relative_path)
    if file_path is None:
        return {"status": "error", "message": "Caminho inválido."}

    if not os.path.exists(file_path):
        return {"status": "error", "message": "Arquivo não encontrado."}

    if not os.path.isfile(file_path):
        return {"status": "error", "message": "O caminho informado não é um arquivo."}

    try:
        with open(file_path, "rb") as f:
            file_content = f.read()
    except OSError as e:
        return {"status": "error", "message": f"Não foi possível baixar o arquivo: {e}"}

    return {
        "status": "success",
        "file_name": os.path.basename(file_path),
        "size": len(file_content),
        "encoding": "base64",
        "data": base64.b64encode(file_content).decode("utf-8")
    }

# --- Lógica do Servidor ---

def handle_client(conn, addr):
    print(f"Conectado por {addr}")
    try:
        with conn:
            data = conn.recv(BUFFER_SIZE)
            if not data:
                return

            request = json.loads(data.decode('utf-8'))
            command = request.get("command")
            response = {"status": "error", "message": "Comando inválido."}

            # O servidor usa um protocolo simples de aplicação:
            # o cliente envia um JSON com "command" e os dados necessários;
            # o servidor executa a operação e responde outro JSON.

            # --- Comando: Criar Conta ---
            if command == "create_account":
                username = request.get("username")
                password = request.get("password")
                users = load_users()

                if username in users:
                    response = {"status": "error", "message": "Nome de usuário já existe."}
                else:
                    # Cada usuário recebe uma pasta própria no servidor.
                    os.makedirs(os.path.join(STORAGE_DIR, username), exist_ok=True)
                    users[username] = {"password": password}
                    save_users(users)
                    response = {"status": "success", "message": "Conta criada com sucesso."}

            # --- Comando: Login ---
            elif command == "login":
                username = request.get("username")
                password = request.get("password")
                users = load_users()

                user_data = users.get(username)
                if user_data and user_data.get("password") == password:
                    response = {"status": "success", "message": "Login bem-sucedido."}
                else:
                    response = {"status": "error", "message": "Usuário ou senha inválidos."}

            # --- Comando: Listar Pasta ---
            elif command == "list_folder":
                username = request.get("username")
                path = request.get("path", "")
                response = list_folder(username, path)

            # --- Comando: Criar Pasta ---
            elif command == "create_folder":
                username = request.get("username")
                path = request.get("path", "")
                folder_name = request.get("folder_name") or request.get("folderName") or request.get("name")
                response = create_folder(username, path, folder_name)

            # --- Comando: Ler Arquivo ---
            elif command == "read_file":
                username = request.get("username")
                path = request.get("path", "")
                response = read_file(username, path)

            # --- Comando: Apagar Arquivo ---
            elif command == "delete_file":
                username = request.get("username")
                path = request.get("path", "")
                response = delete_file(username, path)

            # --- Comando: Enviar Arquivo ---
            elif command == "upload_file":
                username = request.get("username")
                path = request.get("path", "")
                file_name = request.get("file_name") or request.get("fileName") or request.get("name")
                content = request.get("content", request.get("data"))
                encoding = request.get("encoding", "text")
                overwrite = request.get("overwrite", False)

                if file_name:
                    # O cliente pode mandar "path" como pasta e "file_name separado. Aqui juntamos os dois em um caminho relativo.
                    path = os.path.join(path or "", file_name)

                response = upload_file(username, path, content, encoding, overwrite)

            # --- Comando: Baixar Arquivo ---
            elif command == "download_file":
                username = request.get("username")
                path = request.get("path", "")
                response = download_file(username, path)
            
            conn.sendall(json.dumps(response).encode('utf-8'))

    except json.JSONDecodeError:
        print("Erro: Dados inválidos recebidos do cliente.")
        conn.sendall(json.dumps({"status": "error", "message": "Formato de dados inválido."}).encode('utf-8'))
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")

def main():
    host = '0.0.0.0'
    port = 65432

    # Garante que o diretório de armazenamento exista
    os.makedirs(STORAGE_DIR, exist_ok=True)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        print(f"Servidor escutando em {host}:{port}")
        while True:
            conn, addr = s.accept()
            handle_client(conn, addr)

if __name__ == "__main__":
    main()
