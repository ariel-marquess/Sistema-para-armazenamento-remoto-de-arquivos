from client.protocols.connection import server_connection

def record(obj):
    """
    Usa a conexão central para registrar um novo usuário no servidor.
    O dicionário 'obj' deve conter 'username' e 'password'.
    Retorna True em caso de sucesso, False caso contrário.
    """
    username = obj.get('username')
    password = obj.get('password')

    payload = {"username": username, "password": password}
    response = server_connection.send_request("create_account", payload)

    if response.get("status") == "success":
        print("Conta criada com sucesso no servidor!")
        return True
    else:
        # O erro já é impresso pela classe de conexão.
        print(f"Falha ao criar conta no servidor: {response.get('message')}")
        return False
