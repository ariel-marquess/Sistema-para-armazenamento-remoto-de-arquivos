# Guia de Configuração e Solução de Problemas do Ambiente de Desenvolvimento

Este documento é um guia completo e detalhado para configurar o ambiente de desenvolvimento do zero, tanto para o servidor quanto para o cliente, em máquinas virtuais Debian 13 (Trixie). Ele inclui os problemas que podem ser encontrados e suas respectivas soluções.

---

## Parte 1: Configuração da VM Base (Servidor e Cliente)

Estes passos são necessários para AMBAS as máquinas virtuais.

### 1. O Problema: Pacotes Faltando e Erros de `apt`
**Solução:** Habilitar os repositórios `contrib`, `non-free` e `non-free-firmware`.
1.  Edite o arquivo `/etc/apt/sources.list` e adicione `contrib non-free non-free-firmware` ao final de cada linha `deb`.
2.  Rode `sudo apt update`.

### 2. O Problema: Integração com VirtualBox (Resolução, Pastas) Falha
**Solução:** Instalar o **VirtualBox Guest Additions** manualmente.
1.  Instale as dependências: `sudo apt install build-essential dkms linux-headers-$(uname -r)`.
2.  No menu da VM, **Dispositivos > Inserir imagem de CD dos Adicionais para Convidado...**.
3.  Monte e execute: `sudo mount /dev/cdrom /media/cdrom` e depois `sudo sh /media/cdrom/VBoxLinuxAdditions.run`.

### 3. O Problema: A Pasta Compartilhada Não Aparece
**Solução:** Corrigir permissões e ter um plano B para montagem manual.
1.  Crie o grupo `vboxsf`: `sudo groupadd vboxsf`.
2.  Adicione seu usuário ao grupo: `sudo adduser $USER vboxsf`.
3.  Reinicie a VM: `sudo reboot`.
4.  **Plano B (Montagem Manual):** Se a pasta não aparecer em `/media/`, monte-a manualmente: `sudo mount -t vboxsf nome_da_pasta_no_virtualbox /mnt`.

---

## Parte 2: Configuração Específica da VM Cliente

### 4. O Problema: Erro `no display` ao Rodar a Aplicação
**Causa:** Falta de um ambiente gráfico para desenhar janelas.
**Solução:** Instalar um ambiente de desktop leve.
1.  Instale o Xfce: `sudo apt install -y xfce4 xfce4-goodies`.
2.  Reinicie. A VM agora iniciará em modo gráfico.

### 5. O Problema: Erro `no display` Persiste Mesmo no Ambiente Gráfico
**Causa:** A sessão de terminal (geralmente como `root`) perdeu a conexão com a "tela".
**Solução:** Forçar o início do ambiente gráfico com `startx`. Abra um terminal **de dentro** deste novo ambiente para continuar.

### 6. O Problema: Erro `AttributeError` ou `ImportError`
**Causa:** Faltam dependências do Python para o projeto.
**Solução:** Instalar os pacotes via `pip`, ignorando a proteção do sistema (seguro para este ambiente de teste).
```bash
pip3 install Pillow --break-system-packages
pip3 install CTkMessagebox --break-system-packages
```

---

## Parte 3: Diagnóstico de Erros de Conexão

### 7. O Problema: `Connection refused`
**Causa:** O cliente não consegue encontrar o servidor.
1.  O `server.py` não está rodando na VM do Servidor.
2.  O IP no código do cliente está errado.
**Solução:**
1.  Garanta que o servidor esteja executando.
2.  Use `ip addr show` na VM do Servidor para encontrar o IP correto (ex: `192.168.0.2`, **não** o `10.0.2.15`).
3.  Corrija o IP nos arquivos de controle do cliente (`check_user.py`, `record_data.py`).

---

## Parte 4: Sucesso! O Próximo Erro

### 8. O Problema: `TypeError: 'bool' object is not subscriptable`
**Causa:** Este é um **erro bom**. Significa que o **Login funcionou!** O programa avançou para a próxima etapa (carregar os arquivos do dashboard), que ainda não foi implementada. A função `openData.rootData()` retornou `False` em vez de uma lista de arquivos, causando o erro.
**Solução:** Implementar a lógica de listagem de arquivos em `open_data.py` e no `server.py`. **Este é o próximo passo do desenvolvimento.**

---

## Parte 5: Como Executar o Projeto (Resumo)

1.  **Na VM Servidor:** Navegue até a pasta do projeto e rode `python3 server.py`.
2.  **Na VM Cliente:** Navegue até a pasta do projeto e rode `python3 -m client_code.main`.