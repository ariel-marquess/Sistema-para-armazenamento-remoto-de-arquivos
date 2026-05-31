import client.application.utils.ul as util
import client.application.pages.dashboard.sessions.descriptionFile as dfile
import client.application.pages.dashboard.sessions.descriptionFolders as dfolder

import client.protocols.file_handler as file_handler
import client.protocols.open_data as open_data
import client.protocols.check_user as check_user
import client.protocols.record_data as record_data
import client.protocols.creators.mkdir as mkdir

# --- Funções de Manipulação de Arquivos ---

def upload(username, destination_path=""):
    """Controla o fluxo de upload de um arquivo."""
    try:
        if file_handler.uploadFile(username, destination_path):
            util.MessageBox(title="Upload Concluído", message="O arquivo foi enviado para o servidor.", icon="info")
            return True
    except Exception as e:
        util.MessageBox(title="Erro no Upload", message=f"ERRO: {e}", icon="warning")
    return False

def download(username, path):
    """Controla o fluxo de download de um arquivo."""
    try:
        if file_handler.downloadFile(username, path):
            util.MessageBox(title="Download Concluído", message="O arquivo foi salvo em sua máquina.", icon="info")
    except Exception as e:
        util.MessageBox(title="Erro no Download", message=f"ERRO: {e}", icon="warning")

def delete(username, path):
    """Controla o fluxo de exclusão de um arquivo."""
    try:
        if file_handler.deleteFile(username, path):
            util.MessageBox(title="Arquivo Apagado", message="O arquivo foi deletado do servidor.", icon="info")
            return True
    except Exception as e:
        util.MessageBox(title="Erro ao Apagar", message=f"ERRO: {e}", icon="warning")
    return False

def createFolder(username, path, name):
    """Controla o fluxo de criação de uma nova pasta."""
    try:
        if mkdir.mkdir(username, path, name):
            util.MessageBox(title="Pasta Criada", message=f"A pasta '{name}' foi criada com sucesso.", icon="info")
            return True
    except Exception as e:
        util.MessageBox(title="Erro ao Criar Pasta", message=f"ERRO: {e}", icon="warning")
    return False

# --- Funções de Navegação ---

def openFolder(master, currentSession, username, objPath):
    """Abre uma pasta, buscando seu conteúdo no servidor e recriando a sessão de visualização."""
    try:
        path = objPath.get_current_path()
        content = open_data.openFolder(username, path)
        
        if content:
            if currentSession and currentSession.winfo_exists():
                currentSession.destroy()
            # Recria a sessão de pastas com o novo conteúdo
            dfolder.Folders(master, content, objPath)
    except Exception as e:
        util.MessageBox(title="Problema na Abertura da Pasta", message=f"ERRO: {e}", icon="warning")

def openFile(master, currentSession, username, objPath):
    """Abre um arquivo, buscando seu conteúdo no servidor e recriando a sessão de visualização."""
    try:
        path = objPath.get_current_path()
        content = open_data.openFile(username, path)

        if content:
            if currentSession and currentSession.winfo_exists():
                currentSession.destroy()
            master.description_session = dfile.File(master, content, path, username)
    except Exception as e:
        util.MessageBox(title="Problema na Abertura do Arquivo", message=f"ERRO: {e}", icon="warning")

# --- Funções de Autenticação ---

def isUser(username, password):
    """Chama o protocolo para verificar se o usuário e a senha são válidos."""
    return check_user.isUser(username, password)

def record(obj):
    """Chama o protocolo para registrar um novo usuário."""
    return record_data.record(obj)
