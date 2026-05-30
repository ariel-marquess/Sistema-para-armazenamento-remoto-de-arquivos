from client.protocols.connection import server_connection

def mkdir(username, path, folder_name):
    """
    Envia um comando para o servidor para criar uma nova pasta.

    Args:
        username (str): O nome do usuário logado.
        path (str): O caminho da pasta pai onde a nova pasta será criada.
        folder_name (str): O nome da nova pasta a ser criada.
    
    Returns:
        bool: True se a operação for bem-sucedida, False caso contrário.
    """
    payload = {
        "username": username,
        "path": path,
        "folder_name": folder_name
    }
    response = server_connection.send_request("create_folder", payload)

    if response.get("status") == "success":
        print(f"Pasta '{folder_name}' criada com sucesso em '{path}'.")
        return True
    else:
        print(f"Falha ao criar pasta: {response.get('message')}")
        return False
