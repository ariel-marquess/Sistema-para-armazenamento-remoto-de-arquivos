import os

import client.application.utils.ul as util

class Path:
    def __init__(self, root_path=""):
        # O caminho raiz nunca muda (ex: o nome de usuário)
        self.root_path = root_path
        # O histórico de caminhos visitados, começando pela raiz
        self.history = [root_path]

    def get_current_path(self):
        """Retorna o caminho atual (o último item do histórico)."""
        return self.history[-1]

    def get_root_path(self):
        """Retorna o caminho raiz."""
        return self.root_path

    def join(self, folder_name):
        """Avança para uma subpasta e adiciona ao histórico."""
        current = self.get_current_path()
        new_path = os.path.join(current, folder_name)
        self.history.append(new_path)
        return new_path

    def go_back(self):
        """Retrocede para o caminho anterior no histórico."""
        if len(self.history) > 1: # Só pode voltar se não estiver na raiz
            self.history.pop()
            return True
        return False

    def go_to_root_and_join(self, folder_name):
        """Reseta a navegação para a raiz e entra em uma subpasta."""
        self.history = [self.root_path] # Reseta o histórico para a raiz
        return self.join(folder_name)
