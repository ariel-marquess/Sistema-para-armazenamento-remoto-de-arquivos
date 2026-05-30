import os
import base64
from tkinter import filedialog
from client.protocols.connection import server_connection

def downloadFile(username, path):
    """
    Solicita o download de um arquivo do servidor e o salva localmente.
    """
    payload = {"username": username, "path": path}
    response = server_connection.send_request("download_file", payload)

    if response.get("status") == "success":
        try:
            # Abre a caixa de diálogo para o usuário escolher onde salvar
            file_content = base64.b64decode(response.get("data"))
            save_path = filedialog.asksaveasfilename(initialfile=response.get("file_name"))

            if save_path:
                with open(save_path, "wb") as f:
                    f.write(file_content)
                print(f"Arquivo salvo em: {save_path}")
                return True
            else:
                print("Download cancelado pelo usuário.")
                return False
        except Exception as e:
            print(f"Erro ao salvar o arquivo baixado: {e}")
            return False
    else:
        print(f"Falha no download do arquivo '{path}': {response.get('message')}")
        return False

def deleteFile(username, path):
    """
    Solicita a exclusão de um arquivo no servidor.
    """
    payload = {"username": username, "path": path}
    response = server_connection.send_request("delete_file", payload)

    if response.get("status") == "success":
        print(f"Arquivo '{path}' deletado com sucesso.")
        return True
    else:
        print(f"Falha ao deletar o arquivo '{path}': {response.get('message')}")
        return False

def uploadFile(username, destination_path=""):
    """
    Abre uma caixa de diálogo para o usuário escolher um arquivo e o envia para o servidor.
    """
    try:
        # Abre a caixa de diálogo para o usuário escolher o arquivo
        file_path = filedialog.askopenfilename()
        if not file_path:
            print("Upload cancelado pelo usuário.")
            return False

        file_name = os.path.basename(file_path)
        
        with open(file_path, "rb") as f:
            file_content = f.read()
        
        # Codifica o conteúdo em Base64 para transporte seguro via JSON
        encoded_content = base64.b64encode(file_content).decode('utf-8')

        payload = {
            "username": username,
            "path": destination_path,
            "file_name": file_name,
            "encoding": "base64",
            "content": encoded_content,
            "overwrite": True # Permitir sobrescrever por padrão, pode ser alterado
        }

        response = server_connection.send_request("upload_file", payload)

        if response.get("status") == "success":
            print(f"Arquivo '{file_name}' enviado com sucesso para '{destination_path}'.")
            return True
        else:
            print(f"Falha no upload do arquivo: {response.get('message')}")
            return False

    except Exception as e:
        print(f"Erro durante o processo de upload: {e}")
        return False
