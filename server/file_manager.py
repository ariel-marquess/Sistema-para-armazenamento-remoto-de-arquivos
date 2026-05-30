import os
import base64
import binascii

# --- Constantes ---
SERVER_BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STORAGE_DIR = os.path.join(SERVER_BASE_DIR, "storage")

# --- Funções de Gerenciamento de Arquivos ---

def get_safe_user_path(username, relative_path=""):
    """
    Garante que o caminho solicitado esteja sempre dentro da pasta do usuário.
    Bloqueia tentativas de acesso a diretórios pais (ex: ../).
    """
    if not username:
        return None

    user_dir = os.path.abspath(os.path.join(STORAGE_DIR, username))
    requested_path = os.path.abspath(os.path.join(user_dir, relative_path or ""))

    if not requested_path.startswith(user_dir):
        return None

    return requested_path

def _format_folder_size(path):
    """Retorna a quantidade de itens dentro de uma pasta."""
    try:
        return f"{len(os.listdir(path))} itens"
    except OSError:
        return "0 itens"

def _format_file_size(path):
    """Retorna o tamanho de um arquivo em bytes."""
    try:
        return f"{os.path.getsize(path)} bytes"
    except OSError:
        return "0 bytes"

def _is_valid_folder_name(folder_name):
    """Valida se um nome de pasta é seguro e não contém caracteres de caminho."""
    if not isinstance(folder_name, str):
        return False
    folder_name = folder_name.strip()
    if not folder_name or folder_name in (".", ".."):
        return False
    return os.sep not in folder_name and (os.altsep is None or os.altsep not in folder_name)

def list_folder(username, relative_path=""):
    """Lista o conteúdo de uma pasta do usuário."""
    folder_path = get_safe_user_path(username, relative_path)
    if folder_path is None or not os.path.exists(folder_path) or not os.path.isdir(folder_path):
        return {"status": "error", "message": "Caminho da pasta inválido ou não encontrado."}

    folder_data = {"name": [], "size": [], "type": []}
    try:
        entries = sorted(os.scandir(folder_path), key=lambda entry: (not entry.is_dir(), entry.name.lower()))
        for entry in entries:
            folder_data["name"].append(entry.name)
            if entry.is_dir():
                folder_data["size"].append(_format_folder_size(entry.path))
                folder_data["type"].append("pasta")
            else:
                folder_data["size"].append(_format_file_size(entry.path))
                folder_data["type"].append("arquivo")
    except OSError as e:
        return {"status": "error", "message": f"Não foi possível listar a pasta: {e}"}

    return {"status": "success", "data": folder_data}

def create_folder(username, relative_path, folder_name):
    """Cria uma nova pasta dentro de um diretório do usuário."""
    if not _is_valid_folder_name(folder_name):
        return {"status": "error", "message": "Nome de pasta inválido."}

    parent_path = get_safe_user_path(username, relative_path)
    if parent_path is None or not os.path.isdir(parent_path):
        return {"status": "error", "message": "Caminho pai inválido."}

    new_folder_path = os.path.join(parent_path, folder_name.strip())
    if os.path.exists(new_folder_path):
        return {"status": "error", "message": "Já existe um arquivo ou pasta com esse nome."}

    try:
        os.mkdir(new_folder_path)
        return {"status": "success", "message": "Pasta criada com sucesso."}
    except OSError as e:
        return {"status": "error", "message": f"Não foi possível criar a pasta: {e}"}

def read_file(username, relative_path):
    """Lê o conteúdo textual de um arquivo."""
    file_path = get_safe_user_path(username, relative_path)
    if file_path is None or not os.path.isfile(file_path):
        return {"status": "error", "message": "Arquivo não encontrado."}

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        return {"status": "success", "data": content}
    except UnicodeDecodeError:
        return {"status": "error", "message": "O arquivo não é um texto UTF-8 válido."}
    except OSError as e:
        return {"status": "error", "message": f"Não foi possível ler o arquivo: {e}"}

def delete_file(username, relative_path):
    """Apaga um arquivo do usuário."""
    file_path = get_safe_user_path(username, relative_path)
    if file_path is None or not os.path.isfile(file_path):
        return {"status": "error", "message": "Arquivo não encontrado ou o caminho é uma pasta."}

    try:
        os.remove(file_path)
        return {"status": "success", "message": "Arquivo apagado com sucesso."}
    except OSError as e:
        return {"status": "error", "message": f"Não foi possível apagar o arquivo: {e}"}

def upload_file(username, relative_path, content, encoding="text", overwrite=False):
    """Salva um arquivo enviado pelo cliente."""
    file_path = get_safe_user_path(username, relative_path)
    if file_path is None:
        return {"status": "error", "message": "Caminho inválido."}
    if os.path.isdir(file_path):
        return {"status": "error", "message": "Já existe uma pasta com esse nome."}
    if os.path.exists(file_path) and not overwrite:
        return {"status": "error", "message": "Já existe um arquivo com esse nome."}

    try:
        file_content = base64.b64decode(content.encode("utf-8"), validate=True) if encoding == "base64" else content.encode("utf-8")
        with open(file_path, "wb") as f:
            f.write(file_content)
        return {"status": "success", "message": "Arquivo enviado com sucesso.", "size": len(file_content)}
    except (ValueError, binascii.Error):
        return {"status": "error", "message": "Conteúdo Base64 inválido."}
    except OSError as e:
        return {"status": "error", "message": f"Não foi possível salvar o arquivo: {e}"}

def download_file(username, relative_path):
    """Retorna um arquivo do usuário codificado em Base64."""
    file_path = get_safe_user_path(username, relative_path)
    if file_path is None or not os.path.isfile(file_path):
        return {"status": "error", "message": "Arquivo não encontrado."}

    try:
        with open(file_path, "rb") as f:
            file_content = f.read()
        return {
            "status": "success",
            "file_name": os.path.basename(file_path),
            "size": len(file_content),
            "encoding": "base64",
            "data": base64.b64encode(file_content).decode("utf-8")
        }
    except OSError as e:
        return {"status": "error", "message": f"Não foi possível baixar o arquivo: {e}"}
