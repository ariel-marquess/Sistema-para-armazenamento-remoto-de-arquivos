# Diário de Alterações no Código - Backend (Heitor)

Este documento resume as principais alterações que fiz no código para implementar e depurar o fluxo de criação de conta e login.

---

### 1. `server.py`

*   **O que eu modifiquei:** Refatorei completamente o servidor.
    1.  **Armazenamento de Usuários:** Mudei a forma como os usuários são salvos. Antes, era um arquivo com um objeto JSON por linha. Agora, é um único arquivo `users.json` que contém um dicionário, onde a chave é o nome de usuário.
    2.  **Nova Rota de Login:** Adicionei uma nova lógica para entender o comando `"login"`. O servidor agora pode receber credenciais e verificar se elas batem com o que está salvo no `users.json`.

*   **Por que eu modifiquei:** O método de armazenamento antigo era ineficiente e difícil de validar. O novo formato é muito mais rápido e robusto para procurar usuários. A rota de login era essencial, pois sem ela o servidor não tinha como validar as tentativas de login do cliente.

### 2. `client_code/controls/check_user.py`

*   **O que eu modifiquei:** Implementei a função `isUser`, que antes só retornava `False`.
    1.  **Lógica de Socket:** Adicionei o código para criar um socket e se conectar ao servidor.
    2.  **Comando de Login:** O cliente agora envia um objeto JSON com `{"command": "login", ...}` para o servidor.
    3.  **Tratamento de Resposta:** A função agora retorna `True` ou `False` com base na resposta (`"success"` ou `"error"`) recebida do servidor.

*   **Por que eu modifiquei:** Esta era a causa do erro de "inconsistência de dados". A função não fazia nada. Agora, ela executa a comunicação real com o backend para verificar se o usuário e a senha são válidos.

### 3. `client_code/controls/record_data.py`

*   **O que eu modifiquei:** Mudei a forma como o endereço IP do servidor é obtido.
    1.  **IP Fixo:** Em vez de usar o IP digitado pelo usuário na interface, eu "hardcodei" o endereço `192.168.0.2` diretamente no código.

*   **Por que eu modifiquei:** Isso foi uma **medida de depuração crucial**. Tivemos o erro `Connection Refused` porque o IP digitado na tela podia ser diferente do IP que o `check_user.py` estava usando. Ao forçar o mesmo IP nos dois arquivos, garantimos que tanto a criação de conta quanto o login se conectassem ao lugar certo, eliminando essa fonte de erro.

### 4. `README-HEITOR.md` e `CHANGELOG.md`

*   **O que eu modifiquei:** Criei estes dois arquivos.
*   **Por que eu modifiquei:** Para documentar todo o processo de configuração do ambiente, os problemas que enfrentei e as soluções, além de registrar as mudanças feitas no código. Isso vai ajudar o resto da equipe a se atualizar e a configurar seus próprios ambientes sem passar pelas mesmas dificuldades.

---