import os

from CTkMessagebox import CTkMessagebox
from PIL import Image
import customtkinter as ctk


def MessageBox(title, message, icon):    # Método que cria uma caixa de mensagem quando executado
    CTkMessagebox(title=title, message=message, icon=icon)


def images(command, size=20):    # Método que retorna uma imagem quando chamado
    try:
        current = {
            'folder': os.path.join(os.path.dirname(os.path.relpath(__file__)), "..", "images", "folder.png"),
            'file': os.path.join(os.path.dirname(os.path.relpath(__file__)), "..", "images", "file.png"),
            'tgbg': os.path.join(os.path.dirname(os.path.relpath(__file__)), "..", "images", "toGoBack-gray.png"),
            'tgbw': os.path.join(os.path.dirname(os.path.relpath(__file__)), "..", "images", "toGoBack-white.png")
        }

        return ctk.CTkImage(
            light_image=Image.open(current[command]),
            dark_image=Image.open(current[command]),
            size=(size, size)
        )
    except Exception as e:
        MessageBox(
            title="Problema ao carregar as imagens",
            message=f"ERRO: {e}",
            icon="warning"
        )

    return None