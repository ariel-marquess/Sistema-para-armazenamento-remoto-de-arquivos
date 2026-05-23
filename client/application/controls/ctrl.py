import client.application.util.ul as util
import client.application.pages.dashboard.sessions.descriptionFile as dfile
import client.application.pages.dashboard.sessions.descriptionFolders as dfolder

import client.protocols.file_handler as file
import client.protocols.open_data as openData
import client.protocols.check_user as checkUser # Importa o protocolo de verificação
import client.protocols.record_data as recordData # Importa o protocolo de registro
import client.protocols.creators.mkdir as mk


def upload(path):
    try:
        file.uploadFile(path)

        util.MessageBox(
            title="Upload realizado com sucesso",
            message="O arquivo foi enviado para o servidor.",
            icon="info"
        )
    except Exception as e:
        util.MessageBox(
            title="Não foi possível realizar o upload",
            message=f"ERRO: {e}",
            icon="warning"
        )

def download(path):
    try:
        file.downloadFile(path)

        util.MessageBox(
            title="Download realizado com sucesso",
            message="O arquivo foi baixado em sua máquina.",
            icon="info"
        )
    except Exception as e:
        util.MessageBox(
            title="Não foi possível realizar o download",
            message=f"ERRO: {e}",
            icon="warning"
        )


def delete(container, path):
    try:
        file.deleteFile(path)
        container.destroy()

        util.MessageBox(
            title="Arquivo apagado com sucesso",
            message="O arquivo foi deletado do servidor.",
            icon="info"
        )
    except Exception as e:
        util.MessageBox(
            title="Não foi possível apagar o arquivo",
            message=f"ERRO: {e}",
            icon="warning"
        )


def createFolder(path, name, master, currentSession):
    try:
        mk.mkdir(path, name)

        content_descriptionPath = openData.openFolder(path)
        currentSession.destroy()
        descriptionFolder.session_descriptionFolder(master, content_descriptionPath)
    except Exception as e:
        util.MessageBox(
            title="Problema na criação da pasta",
            message=f"ERRO: {e}",
            icon="warning"
        )


def openFolder(master, currentSession, path = None):
    try:
        if path:
            print(f'Abrindo pasta: {path}')
        else:
            content_descriptionPath = openData.openFolder(path)

            currentSession.destroy()
            dfolder.session_descriptionFolder(master, content_descriptionPath)
    except Exception as e:
        util.MessageBox(
            title="Problema na abertura da pasta",
            message=f"ERRO: {e}",
            icon="warning"
        )


def openFile(master, currentSession, path = None):
    try:
        if path:
            print(f'Abrindo arquivo: {path}')
        else:
            content_file = openData.openFile(path)

            currentSession.destroy()
            dfile.session_contentFile(master, content_file)
    except Exception as e:
        util.MessageBox(
            title="Problema na abertura do arquivo",
            message=f"ERRO: {e}",
            icon="warning"
        )

# --- Funções de Autenticação ---

def isUser(username, password):
    """
    Chama o protocolo para verificar se o usuário e a senha são válidos.
    """
    return checkUser.isUser(username, password)

def record(obj):
    """
    Chama o protocolo para registrar um novo usuário.
    """
    return recordData.record(obj)
