import os

from CTkMessagebox import CTkMessagebox
from PIL import Image
import customtkinter as ctk


def MessageBox(title, message, icon):    # Método que cria uma caixa de mensagem quando executado
    CTkMessagebox(title=title, message=message, icon=icon)


def change_background(event, forced_widget, color):
    target = forced_widget if forced_widget else event.widget
    if not isinstance(target, ctk.CTkFrame):
        target = target.master

    target.configure(fg_color=color)


def execute(master, function, args=None):
    try:
        function(*args)
    except:
        MessageBox(
            title="Problema de execussão",
            message=f"ERRO: {e}",
            icon="warning"
        )
    finally:
        master.destroy()


def images(command, size=20):    # Método que retorna uma imagem quando chamado
    try:
        currentFile = os.path.dirname(os.path.abspath(__file__))
        current = {
            'close': os.path.join(currentFile, "../..", "images", "close.png"),
            'folder': os.path.join(currentFile, "../..", "images", "folder.png"),
            'file': os.path.join(currentFile, "../..", "images", "file.png"),
            'tgbg': os.path.join(currentFile, "../..", "images", "toGoBack-gray.png"),
            'tgbw': os.path.join(currentFile, "../..", "images", "toGoBack-white.png"),
            'eclosed': os.path.join(currentFile, "../..", "images", "eye-closed.png"),
            'eopen': os.path.join(currentFile, "../..", "images", "eye-open.png")
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