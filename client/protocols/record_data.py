import socket
import json

def record(obj):
    # Este método deve registrar no servidor as informações passadas pelo dicionário 'obj'.
    
    # IP e Porta da rede interna da VM, para que as VMs possam se comunicar.
    address = '192.168.0.2'
    port = 65432
    username = obj.get('username')
    password = obj.get('password')

    try:
        # Criando o socket TCP
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            # Conectando ao servidor
            s.connect((address, port))

            # Preparando os dados para envio (formato JSON)
            data_to_send = {
                "command": "create_account",
                "username": username,
                "password": password
            }
            s.sendall(json.dumps(data_to_send).encode('utf-8'))

            # Recebendo a resposta do servidor
            response = s.recv(1024).decode('utf-8')
            response_data = json.loads(response)

            if response_data.get("status") == "success":
                print("Conta criada com sucesso!")
                return True
            else:
                print(f"Falha ao criar conta: {response_data.get('message')}")
                return False

    except Exception as e:
        print(f"Ocorreu um erro na comunicação com o servidor: {e}")
        return False