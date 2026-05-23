import socket
import json

# IP e Porta da rede interna da VM, para que as VMs possam se comunicar.
SERVER_ADDRESS = '192.168.0.2'
SERVER_PORT = 65432

def record(obj):
    """
    Este método se conecta ao servidor para registrar um novo usuário.
    O dicionário 'obj' deve conter 'username' e 'password'.
    Retorna True em caso de sucesso, False caso contrário.
    """
    username = obj.get('username')
    password = obj.get('password')

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((SERVER_ADDRESS, SERVER_PORT))

            data_to_send = {
                "command": "create_account",
                "username": username,
                "password": password
            }
            s.sendall(json.dumps(data_to_send).encode('utf-8'))

            response = s.recv(1024).decode('utf-8')
            response_data = json.loads(response)

            if response_data.get("status") == "success":
                print("Conta criada com sucesso no servidor!")
                return True
            else:
                print(f"Falha ao criar conta no servidor: {response_data.get('message')}")
                return False

    except Exception as e:
        print(f"Ocorreu um erro na comunicação ao criar conta: {e}")
        return False
