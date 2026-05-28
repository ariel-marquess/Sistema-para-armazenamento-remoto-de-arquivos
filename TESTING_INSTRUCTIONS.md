# Configuração do Ambiente de Desenvolvimento (Backend)

Este documento descreve os passos necessários para configurar uma máquina virtual Debian 13 (Trixie) no VirtualBox para rodar o servidor backend deste projeto.

---

## 1. Configuração da VM Debian (Passo único)

Estes passos preparam a máquina virtual para se comunicar com o VirtualBox e com a sua máquina host.

### 1.1. Habilitar Repositórios Adicionais

1.  Abra o terminal e edite o arquivo `sources.list`:
    ```bash
    sudo nano /etc/apt/sources.list
    ```
2.  Adicione `contrib non-free non-free-firmware` ao final de cada linha `deb`. O arquivo deve ficar similar a este:
    ```bash
    deb http://deb.debian.org/debian/ trixie main contrib non-free non-free-firmware
    deb-src http://deb.debian.org/debian/ trixie main contrib non-free non-free-firmware
    # ... e assim por diante para as outras linhas
    ```
3.  Salve (`Ctrl+X`, `Y`, `Enter`) e atualize a lista de pacotes:
    ```bash
    sudo apt update
    ```

### 1.2. Instalar o VirtualBox Guest Additions

1.  **Instale as dependências:**
    ```bash
    sudo apt install build-essential dkms linux-headers-$(uname -r)
    ```
2.  **Insira o CD do Guest Additions:** No menu da janela da VM, clique em **Dispositivos > Inserir imagem de CD dos Adicionais para Convidado...**.
3.  **Monte e execute o instalador:**
    ```bash
    sudo mkdir -p /media/cdrom
    sudo mount /dev/cdrom /media/cdrom
    sudo sh /media/cdrom/VBoxLinuxAdditions.run
    ```

---

## 2. Configuração da Pasta Compartilhada

Isso permite que o código do projeto apareça dentro da VM.

### 2.1. Configurar no VirtualBox

1.  Com a VM desligada, vá em **Configurações da VM > Pastas Compartilhadas**.
2.  Clique no ícone `+` para adicionar uma nova pasta.
    *   **Caminho da Pasta:** Selecione a pasta raiz do seu projeto.
    *   **Nome da Pasta:** Dê um nome simples, como `projeto_drive`. **Anote este nome.**
    *   **Opções:** Marque **Montar Automaticamente** e **Tornar Permanente**.

### 2.2. Corrigir Permissões na VM

1.  **Crie o grupo `vboxsf`** (se ele não existir):
    ```bash
    sudo groupadd vboxsf
    ```
2.  **Adicione seu usuário ao grupo:**
    ```bash
    sudo adduser $USER vboxsf
    ```
3.  **Reinicie a VM** para que tudo seja aplicado:
    ```bash
    sudo reboot
    ```

---

## 3. Como Executar o Servidor (Uso Diário)

Após a configuração, siga estes passos para rodar o backend.

1.  Inicie a VM do Servidor e abra o terminal.

2.  **Verifique se a pasta compartilhada montou automaticamente.** O local padrão é `/media/sf_<nome_da_pasta>`.
    ```bash
    ls /media/
    ```
    Se você vir sua pasta (ex: `sf_projeto_drive`), pule para o passo 4.

3.  **Se a pasta não apareceu (Solução Manual):**
    A montagem automática pode falhar. Use o comando de montagem manual que sabemos que funciona.
    ```bash
    # Crie um ponto de montagem (só precisa fazer isso uma vez)
    sudo mkdir -p /mnt/share

    # Monte a pasta (use o "Nome da Pasta" do passo 2.1)
    sudo mount -t vboxsf projeto_drive /mnt/share
    ```
    Neste caso, seu projeto estará em `/mnt/share`.

4.  **Navegue até a pasta do projeto e execute o servidor:**
    *   **Se a montagem automática funcionou:**
        ```bash
        cd /media/sf_projeto_drive/
        python3 server.py
        ```
    *   **Se você usou a montagem manual:**
        ```bash
        cd /mnt/share/
        python3 server.py
        ```

O servidor estará rodando. Para encontrar o IP do servidor, use o comando `ip addr show`. A porta padrão é `65432`.