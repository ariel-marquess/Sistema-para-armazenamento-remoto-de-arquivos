# Diário de Alterações no Código - Backend (Heitor)

Este documento resume as principais alterações que fiz no código para implementar e depurar o fluxo de criação de conta e login.

---

### 1. `server.py` (Movido para `server/server.py`)

*   **O que eu modifiquei:** Refatorei completamente o servidor.
    1.  **Armazenamento de Usuários:** Mudei a forma como os usuários são salvos. Antes, era um arquivo com um objeto JSON por linha. Agora, é um único arquivo `users.json` que contém um dicionário, onde a chave é o nome de usuário.
    2.  **Nova Rota de Login:** Adicionei uma nova lógica para entender o comando `"login"`. O servidor agora pode receber credenciais e verificar se elas batem com o que está salvo no `users.json`.
    3.  **Caminhos Adaptados:** Ajustei os caminhos de `STORAGE_DIR` para que `server_storage` seja criado dentro da pasta `server/`.

*   **Por que eu modifiquei:** O método de armazenamento antigo era ineficiente e difícil de validar. O novo formato é muito mais rápido e robusto para procurar usuários. A rota de login era essencial, pois sem ela o servidor não tinha como validar as tentativas de login do cliente. A adaptação de caminhos foi necessária devido à nova estrutura de pastas do projeto.

### 2. `client/protocols/check_user.py` (Antigo `client_code/controls/check_user.py`)

*   **O que eu modifiquei:** Movi e implementei a função `isUser`.
    1.  **Lógica de Socket:** Adicionei o código para criar um socket e se conectar ao servidor.
    2.  **Comando de Login:** O cliente agora envia um objeto JSON com `{"command": "login", ...}` para o servidor.
    3.  **Tratamento de Resposta:** A função agora retorna `True` ou `False` com base na resposta (`"success"` ou `"error"`) recebida do servidor.
    4.  **IP Fixo:** "Hardcodei" o endereço `192.168.0.2` para garantir a conexão correta entre as VMs.

*   **Por que eu modifiquei:** Esta função era a causa do erro de "inconsistência de dados". Agora, ela executa a comunicação real com o backend para verificar se o usuário e a senha são válidos. A mudança de localização foi para alinhar com a nova arquitetura de `protocols`.

### 3. `client/protocols/record_data.py` (Antigo `client_code/controls/record_data.py`)

*   **O que eu modifiquei:** Movi e implementei a função `record`.
    1.  **Lógica de Socket:** Adicionei o código para criar um socket e se conectar ao servidor.
    2.  **Comando de Criação:** O cliente envia um objeto JSON com `{"command": "create_account", ...}` para o servidor.
    3.  **Tratamento de Resposta:** A função retorna `True` ou `False` com base na resposta.
    4.  **IP Fixo:** "Hardcodei" o endereço `192.168.0.2` para garantir a conexão correta entre as VMs.

*   **Por que eu modifiquei:** Esta função agora executa a comunicação real com o backend para registrar novos usuários. A mudança de localização foi para alinhar com a nova arquitetura de `protocols`.

### 4. `client/application/controls/ctrl.py` (Novo arquivo)

*   **O que eu modifiquei:** Adicionei as funções `isUser` e `record`.
    1.  **Orquestração:** Estas funções agora servem como "pontes", chamando as respectivas funções implementadas em `client/protocols/check_user.py` e `client/protocols/record_data.py`.

*   **Por que eu modifiquei:** Para consolidar os controles em um único arquivo, conforme a nova estrutura do projeto, e para que esta camada chame a camada de `protocols`, separando as responsabilidades.

### 5. `client/application/pages/login/log.py` (Novo arquivo)

*   **O que eu modifiquei:** Adaptei a função `enter`.
    1.  **Importação:** Importei `client.application.controls.ctrl`.
    2.  **Chamada de Login:** A função `enter` agora chama `ctrl.isUser(username, password)` para validar as credenciais.

*   **Por que eu modifiquei:** Para conectar a interface de login com a lógica de verificação de usuário que implementamos.

### 6. `client/application/pages/account/cac.py` (Novo arquivo)

*   **O que eu modifiquei:** Adaptei a função `create`.
    1.  **Importação:** Importei `client.application.controls.ctrl`.
    2.  **Chamada de Criação:** A função `create` agora chama `ctrl.record(infos)` para registrar o novo usuário.
    3.  **Remoção de Validação `isUsername`:** A verificação de nome de usuário existente agora é feita no servidor, então a chamada local foi removida.

*   **Por que eu modifiquei:** Para conectar a interface de criação de conta com a lógica de registro de usuário que implementamos.

### 7. `README-HEITOR.md` e `CHANGELOG.md`

*   **O que eu modifiquei:** Criei e atualizei estes arquivos.
*   **Por que eu modifiquei:** Para documentar todo o processo de configuração do ambiente, os problemas que enfrentei e as soluções, além de registrar as mudanças feitas no código. Isso vai ajudar o resto da equipe a se atualizar e a configurar seus próprios ambientes sem passar pelas mesmas dificuldades.

---