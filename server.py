import socket
import json
import os

# --- Constantes ---
STORAGE_DIR = "server_storage"
USERS_FILE = os.path.join(STORAGE_DIR, "users.json")

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
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=4)

# --- Lógica do Servidor ---

def handle_client(conn, addr):
    print(f"Conectado por {addr}")
    try:
        with conn:
            data = conn.recv(1024)
            if not data:
                return

            request = json.loads(data.decode('utf-8'))
            command = request.get("command")
            response = {"status": "error", "message": "Comando inválido."}

            # --- Comando: Criar Conta ---
            if command == "create_account":
                username = request.get("username")
                password = request.get("password")
                users = load_users()

                if username in users:
                    response = {"status": "error", "message": "Nome de usuário já existe."}
                else:
                    # Cria o diretório do usuário
                    os.makedirs(os.path.join(STORAGE_DIR, username), exist_ok=True)
                    # Adiciona o novo usuário e salva
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
            # Idealmente, isso deveria usar threads para lidar com múltiplos clientes
            handle_client(conn, addr)

if __name__ == "__main__":
    main()