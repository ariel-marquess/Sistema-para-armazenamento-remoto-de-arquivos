import socket
import json
import os
import user_manager
import file_manager

# --- Constantes ---
BUFFER_SIZE = 10 * 1024 * 1024 # 10MB

# --- Lógica de Manipulação de Comandos ---

def handle_request(request):
    """
    Recebe a requisição do cliente e delega para o manager apropriado.
    Retorna um dicionário de resposta.
    """
    command = request.get("command")
    username = request.get("username")
    password = request.get("password")
    path = request.get("path", "")
    
    # Comandos de Usuário
    if command == "create_account":
        return user_manager.create_user(username, password)
    
    if command == "login":
        return user_manager.validate_user(username, password)

    # Validação de sessão (todos os comandos abaixo precisam de um usuário válido)
    # A validação de senha aqui pode ser opcional dependendo da política de segurança.
    # Por enquanto, vamos assumir que o cliente é confiável após o login.
    if not username:
        return {"status": "error", "message": "Comando requer nome de usuário."}

    # Comandos de Arquivo
    if command == "list_folder":
        return file_manager.list_folder(username, path)

    if command == "create_folder":
        folder_name = request.get("folder_name")
        return file_manager.create_folder(username, path, folder_name)

    if command == "read_file":
        return file_manager.read_file(username, path)

    if command == "delete_file":
        return file_manager.delete_file(username, path)

    if command == "upload_file":
        file_name = request.get("file_name")
        content = request.get("content")
        encoding = request.get("encoding", "text")
        overwrite = request.get("overwrite", False)
        if file_name:
            path = os.path.join(path, file_name)
        return file_manager.upload_file(username, path, content, encoding, overwrite)

    if command == "download_file":
        return file_manager.download_file(username, path)

    return {"status": "error", "message": "Comando desconhecido."}

# --- Lógica Principal do Servidor ---

def handle_client_connection(conn, addr):
    """Lida com uma única conexão de cliente."""
    print(f"Conectado por {addr}")
    try:
        with conn:
            data = conn.recv(BUFFER_SIZE)
            if not data:
                return

            request = json.loads(data.decode('utf-8'))
            response = handle_request(request)
            conn.sendall(json.dumps(response).encode('utf-8'))

    except json.JSONDecodeError:
        print(f"Erro: Dados inválidos recebidos de {addr}.")
        conn.sendall(json.dumps({"status": "error", "message": "Formato de dados inválido."}).encode('utf-8'))
    except Exception as e:
        print(f"Ocorreu um erro inesperado com {addr}: {e}")

def main():
    """Inicia o servidor e o loop de escuta."""
    host = '192.168.0.1'
    port = 65432

    # Garante que o diretório de armazenamento principal exista
    os.makedirs(os.path.join(os.path.dirname(__file__), "storage"), exist_ok=True)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        print(f"Servidor escutando em {host}:{port}")
        while True:
            conn, addr = s.accept()
            # Idealmente, isso deveria usar threads para lidar com múltiplos clientes
            handle_client_connection(conn, addr)

if __name__ == "__main__":
    main()
