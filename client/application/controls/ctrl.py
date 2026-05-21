import os

import client.application.util.ul as util
import client.protocols.file_handler as file
import client.protocols.open_data as openData

def download(path):
    try:
        file.downloadFile(path)
    except Exception as e:
        util.MessageBox(
            title="Não foi possível realizar o download",
            message=f"ERRO: {e}",
            icon="warning"
        )


def delete(path):
    try:
        file.deleteFile(path)
    except Exception as e:
        util.MessageBox(
            title="Não foi possível apagar o arquivo",
            message=f"ERRO: {e}",
            icon="warning"
        )


def createFolder():
    return False


def openFolder(master, currentSession, path = None):
    if path:
        print(f'Abrindo pasta: {path}')
    else:
        content_descriptionPath = openData.openFolder(path)

        currentSession.destroy()
        master.session_descriptionFolder(content_descriptionPath)


def openFile(master, currentSession, path = None):
    if path:
        print(f'Abrindo arquivo: {path}')
    else:
        content_file = openData.openFile(path)

        currentSession.destroy()
        master.session_contentFile(master, content_file)