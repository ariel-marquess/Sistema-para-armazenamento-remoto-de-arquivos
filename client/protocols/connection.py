import socket
import json

# Configurações centralizadas de conexão com o servidor
SERVER_ADDRESS = '192.168.0.1'
SERVER_PORT = 65432
BUFFER_SIZE = 10 * 1024 * 1024 # Buffer de 10MB para suportar transferências de arquivo

class _ServerConnection:
    """
    Classe Singleton para gerenciar a comunicação com o servidor.
    O _ no início indica que esta classe é para uso interno deste módulo.
    """
    def send_request(self, command, payload={}):
        """
        Abre uma conexão, envia um comando e um payload para o servidor,
        e retorna a resposta em formato de dicionário.

        Args:
            command (str): O comando a ser executado no servidor (ex: "login").
            payload (dict): Um dicionário com os dados a serem enviados.

        Returns:
            dict: A resposta do servidor.
        """
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((SERVER_ADDRESS, SERVER_PORT))

                # Monta a requisição completa
                request_data = {
                    "command": command,
                    **payload  # Desempacota o payload no dicionário principal
                }
                
                s.sendall(json.dumps(request_data).encode('utf-8'))
                
                # Recebe a resposta
                response = s.recv(BUFFER_SIZE)
                if not response:
                    return {"status": "error", "message": "Servidor não enviou resposta."}
                
                response_data = json.loads(response.decode('utf-8'))
                return response_data

        except ConnectionRefusedError:
            print("Erro de comunicação: A conexão foi recusada. O servidor está offline ou em outro IP?")
            return {"status": "error", "message": "Connection refused."}
        except Exception as e:
            print(f"Erro inesperado na comunicação com o servidor: {e}")
            return {"status": "error", "message": str(e)}

# --- Instância Única (Singleton) ---
# Criamos uma única instância da classe que será importada e usada por todo o cliente.
# Isso evita criar múltiplos objetos de conexão desnecessariamente.
server_connection = _ServerConnection()
