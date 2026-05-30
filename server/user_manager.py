import os
import json

# --- Constantes ---
# O diretório base do servidor é o diretório onde este script está localizado.
SERVER_BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STORAGE_DIR = os.path.join(SERVER_BASE_DIR, "storage")
USERS_FILE = os.path.join(STORAGE_DIR, "users.json")

# --- Funções de Gerenciamento de Usuários ---

def _load_users():
    """Carrega os usuários do arquivo JSON. Retorna um dicionário de usuários."""
    if not os.path.exists(USERS_FILE):
        return {}
    try:
        with open(USERS_FILE, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return {}

def _save_users(users):
    """Salva o dicionário de usuários no arquivo JSON."""
    os.makedirs(STORAGE_DIR, exist_ok=True)
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=4)

def validate_user(username, password):
    """
    Valida as credenciais de um usuário.
    Retorna um dicionário de resposta padrão.
    """
    users = _load_users()
    user_data = users.get(username)
    if user_data and user_data.get("password") == password:
        return {"status": "success", "message": "Login bem-sucedido."}
    else:
        return {"status": "error", "message": "Usuário ou senha inválidos."}

def create_user(username, password):
    """
    Cria um novo usuário.
    Retorna um dicionário de resposta padrão.
    """
    users = _load_users()
    if username in users:
        return {"status": "error", "message": "Nome de usuário já existe."}
    
    # Cria o diretório do usuário
    try:
        user_dir = os.path.join(STORAGE_DIR, username)
        os.makedirs(user_dir, exist_ok=True)
    except OSError as e:
        return {"status": "error", "message": f"Não foi possível criar o diretório do usuário: {e}"}

    # Adiciona o novo usuário e salva
    users[username] = {"password": password}
    _save_users(users)
    return {"status": "success", "message": "Conta criada com sucesso."}
