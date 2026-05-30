from client.protocols.connection import server_connection

def openFolder(username, path=""):
    """
    Busca no servidor a lista de arquivos e subpastas de um determinado caminho.

    Args:
        username (str): O nome do usuário logado.
        path (str, optional): O caminho relativo da pasta a ser listada. 
                              Se vazio, lista a raiz do usuário.

    Returns:
        dict: Um dicionário com os dados da pasta, ou None em caso de falha.
    """
    payload = {"username": username, "path": path}
    response = server_connection.send_request("list_folder", payload)

    if response.get("status") == "success":
        return response.get("data")
    else:
        print(f"Falha ao listar pasta '{path}' para o usuário '{username}': {response.get('message')}")
        return None

def openFile(username, path):
    """
    Busca no servidor o conteúdo textual de um arquivo.

    Args:
        username (str): O nome do usuário logado.
        path (str): O caminho relativo do arquivo a ser lido.

    Returns:
        str: O conteúdo do arquivo, ou None em caso de falha.
    """
    payload = {"username": username, "path": path}
    response = server_connection.send_request("read_file", payload)

    if response.get("status") == "success":
        return response.get("data")
    else:
        print(f"Falha ao ler arquivo '{path}' para o usuário '{username}': {response.get('message')}")
        return None
