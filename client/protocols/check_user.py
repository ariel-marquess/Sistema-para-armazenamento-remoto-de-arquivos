from client.protocols.connection import server_connection

def isUser(username, password):
    """
    Usa a conexão central para verificar se o usuário e a senha correspondem.
    Retorna True em caso de sucesso, False caso contrário.
    """
    payload = {"username": username, "password": password}
    response = server_connection.send_request("login", payload)
    
    if response.get("status") == "success":
        return True
    else:
        # O erro já é impresso pela classe de conexão, mas podemos adicionar mais contexto se necessário.
        print(f"Falha no login para o usuário '{username}': {response.get('message')}")
        return False

def isUsername(username):
    """
    Verifica no lado do servidor se um nome de usuário já existe.
    (Esta função pode ser implementada no futuro se for necessário
    verificar o nome de usuário em tempo real, antes de submeter o formulário).
    """
    # Exemplo de como poderia ser implementado:
    # payload = {"username": username}
    # response = server_connection.send_request("check_username", payload)
    # return response.get("exists", True) # Retorna True por segurança se a resposta falhar
    return False
