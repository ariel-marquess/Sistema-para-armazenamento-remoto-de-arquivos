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

### 8. Finalização das Funcionalidades do Cliente

*   **O que eu modifiquei:**
    1.  **Refatoração:** Centralizei a lógica de socket na nova classe `ServerConnection` em `client/protocols/connection.py`.
    2.  **Implementação de Protocolos:** Implementei as funções de `uploadFile`, `downloadFile`, `deleteFile` em `file_handler.py` e `mkdir` em `mkdir.py`.
    3.  **Navegação de Pastas:** Corrigi e implementei a classe `Path` para gerenciar o histórico de navegação, permitindo entrar e sair de pastas.
    4.  **Integração da UI:** Conectei todos os botões e menus restantes do Dashboard (Upload, Download, Apagar, Criar Pasta, Voltar, Visualizar Arquivo) às suas respectivas funções de controle.

*   **Por que eu modifiquei:** Para finalizar todas as funcionalidades visíveis na interface, tornando o protótipo completamente funcional de ponta a ponta, e para melhorar a qualidade do código do cliente, eliminando repetição.

---

# Diário de Alterações no Código - Backend (Ricardo)

Esta seção registra as mudanças feitas por Ricardo para completar as operações principais do back-end e organizar melhor os arquivos do projeto.

---

### 1. Implementações no back-end (`server/server.py`)

*   **O que eu modifiquei:** Ampliei o servidor para suportar as principais operações de um sistema de armazenamento remoto.
    1.  **Criação automática de pastas de usuário:** O servidor passou a usar `server/storage/` como diretório principal de armazenamento e cria uma pasta específica para cada usuário.
    2.  **Listagem de arquivos:** Implementei o comando `list_folder`, que retorna nomes, tamanhos e tipos dos itens dentro da pasta do usuário.
    3.  **Criação de pastas:** Implementei o comando `create_folder`, permitindo criar diretórios dentro do espaço do usuário.
    4.  **Leitura de arquivo de texto:** Implementei o comando `read_file`, usado para abrir arquivos de texto UTF-8.
    5.  **Exclusão de arquivo:** Implementei o comando `delete_file`, permitindo apagar arquivos do usuário sem remover pastas.
    6.  **Upload de arquivo:** Implementei o comando `upload_file`, permitindo salvar arquivos enviados pelo cliente.
    7.  **Download de arquivo:** Implementei o comando `download_file`, permitindo recuperar arquivos armazenados no servidor.
    8.  **Suporte a arquivos binários:** Usei Base64 para transportar arquivos binários dentro das mensagens JSON.
    9.  **Proteção contra caminhos inválidos:** Adicionei validação para impedir acessos como `../`, evitando que o cliente saia da pasta do usuário.
    10. **Validação de nomes de pasta:** Adicionei uma checagem para impedir nomes vazios, `.`/`..` e caminhos compostos no nome da nova pasta.
    11. **Buffer maior:** Aumentei o buffer de recebimento para `10 MB`, pois upload e download em Base64 geram mensagens maiores.

*   **Por que eu modifiquei:** Essas funções eram necessárias para aproximar o servidor dos requisitos da atividade avaliativa: autenticação, criação de espaço de armazenamento por usuário, listagem, upload, download e persistência dos arquivos no disco da VM do servidor.

### 2. Organização de arquivos e documentação

*   **O que eu modifiquei:** Organizei arquivos que estavam sobrando ou com função pouco clara no estado atual do projeto.
    1.  **Exclusão de `server_storage/`:** Removi a pasta antiga porque o armazenamento atual passou a ser feito em `server/storage/`.
    2.  **Exclusão de `server/data/`:** Removi a pasta `server/data/`, pois ela não estava sendo usada pelo servidor atual.
    3.  **Exclusão de `README-HEITOR.md`:** Removi o arquivo por estar desnecessário diante da nova documentação centralizada.
    4.  **Renomeação de `README.md`:** Renomeei o README antigo para `TESTING_INSTRUCTIONS.md`, pois seu conteúdo estava mais relacionado a instruções de ambiente e testes.
    5.  **Criação de novo `README.md`:** Criei um novo README com a descrição geral do projeto, contexto da atividade, arquitetura, protocolo, comandos implementados, execução e limitações atuais.

*   **Observação:** O novo `README.md` ainda pode ser atualizado e mesclado com `TESTING_INSTRUCTIONS.md` quando o projeto estiver finalizado, para deixar a documentação de entrega mais limpa e centralizada.

### 3. Correções e ajustes para teste local

*   **O que eu modifiquei:** Fiz pequenos ajustes necessários para conseguir testar o projeto durante o desenvolvimento.
    1.  **Correção em `client/application/pages/account/cac.py`:** Na linha 86, alterei `self.open_login = page_login` para `self.open_login = open_login`, pois `page_login` não existia e causava erro ao abrir/usar a tela de criação de conta.
    2.  **Alteração de IP para testes:** Ajustei o endereço IP configurado no cliente para fins de teste local. Esse IP deve ser verificado antes de testar em outra máquina ou antes da demonstração em VMs diferentes.

*   **Por que eu modifiquei:** A correção no `cac.py` evita erro de referência inexistente, e a alteração de IP foi necessária para testar cliente e servidor no ambiente local de desenvolvimento.

---
