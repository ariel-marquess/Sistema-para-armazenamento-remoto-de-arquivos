# Este código cria e gerencia as páginas do programa

from client_code.pages.login import Login
from client_code.pages.create_account import Create
from client_code.pages.dashboard import Dashboard


def start_login():
    app = Login(open_create = start_create, open_dashboard = start_dashboard)
    app.mainloop()

def start_create():
    app = Create(page_login = start_login)
    app.mainloop()

def start_dashboard():
    app = Dashboard()
    app.mainloop()


if __name__ == "__main__":
    start_dashboard()
