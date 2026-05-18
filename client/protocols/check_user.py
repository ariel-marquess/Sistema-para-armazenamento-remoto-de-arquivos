import socket
import json
# aaa
def isUser(username, password):
    # Este método verifica se o usuário e a senha correspondem aos registros do servidor.
    
    # IP e Porta da rede interna da VM, para que as VMs possam se comunicar.
    address = '192.168.0.2'
    port = 65432

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((address, port))

            # Prepara os dados para o pedido de login
            data_to_send = {
                "command": "login",
                "username": username,
                "password": password
            }
            s.sendall(json.dumps(data_to_send).encode('utf-8'))

            # Recebe a resposta
            response = s.recv(1024).decode('utf-8')
            response_data = json.loads(response)

            if response_data.get("status") == "success":
                return True
            else:
                return False

    except Exception as e:
        print(f"Erro de conexão ao tentar fazer login: {e}")
        return False

def isUsername(username):
    # Este método deve verificar se o nome de usuário já está ou não sendo utilizado.
    # Por enquanto, esta função não está conectada ao servidor.
    # A verificação real é feita no lado do servidor durante a criação da conta.
    return False
