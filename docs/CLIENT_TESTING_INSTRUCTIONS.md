# Configuração do Ambiente de Execução do Client

Este documento descreve os passos necessários para configurar uma máquina virtual Debian para executar a parte **client** deste projeto.

> **Observação sobre a rede interna:**  
> Para o funcionamento esperado na rede interna, considere a seguinte configuração de IP:
>
> - **Servidor:** `192.168.0.1`
> - **Cliente:** `192.168.0.2`
>
> Certifique-se de que a configuração de rede da máquina virtual permite a comunicação entre o client e o servidor.

---

## 1. Instalação de uma interface gráfica mínima no Debian

O client do projeto utiliza uma interface gráfica. Por isso, em uma instalação mínima do Debian, é necessário instalar um ambiente gráfico antes da execução da aplicação.

Neste guia será utilizada a interface **XFCE**, por ser leve e adequada para máquinas virtuais.

### 1.1. Atualizar os pacotes do sistema

Abra o terminal na máquina virtual Debian e execute:

```bash
sudo apt update
```

### 1.2. Instalar XFCE e dependências gráficas

Execute o comando abaixo para instalar uma interface gráfica mínima e o suporte ao `tkinter`, necessário para aplicações gráficas em Python:

```bash
sudo apt install -y xfce4 xfce4-goodies python3-tk
```

### 1.3. Reiniciar a máquina virtual

Após a instalação, reinicie a VM:

```bash
sudo reboot
```

Depois da reinicialização, a máquina deverá iniciar com uma interface gráfica ou permitir o login em uma sessão XFCE.

---

## 2. Configuração do ambiente virtual Python

O projeto utiliza um ambiente virtual Python para isolar as dependências necessárias à execução do client.

Antes de executar a aplicação, acesse a pasta raiz do projeto dentro da máquina virtual.

Exemplo:

```bash
cd /caminho/do/projeto
```

Substitua `/caminho/do/projeto` pelo caminho real onde o projeto está localizado na VM.

---

## 3. Criando o ambiente virtual, caso ainda não exista

Se o projeto ainda não possuir um ambiente virtual configurado, será necessário criá-lo.

### 3.1. Verificar se o módulo `venv` está instalado

Em algumas instalações do Debian, o suporte à criação de ambientes virtuais pode não estar disponível por padrão.

Instale o pacote necessário com:

```bash
sudo apt update
sudo apt install -y python3-venv
```

### 3.2. Criar o ambiente virtual

Dentro da pasta raiz do projeto, execute:

```bash
python3 -m venv .venv
```

Esse comando criará uma pasta chamada `.venv`, que armazenará o ambiente virtual do projeto.

### 3.3. Ativar o ambiente virtual

Depois de criado, ative o ambiente virtual com:

```bash
source .venv/bin/activate
```

Se a ativação funcionar corretamente, o terminal deverá exibir algo semelhante a:

```bash
(.venv) usuario@debian:/caminho/do/projeto$
```

---

## 4. Instalação das dependências do Client

Com o ambiente virtual ativado, instale as dependências necessárias para executar o client:

```bash
pip install customtkinter Pillow CTkMessagebox
```

Essas bibliotecas são utilizadas para a interface gráfica e exibição de elementos visuais da aplicação.

---

## 5. Execução do Client

Após instalar as dependências, ainda com o ambiente virtual ativado e estando na raiz do projeto, execute:

```bash
python3 -m client.application.pages.main
```

Esse comando iniciará a aplicação client.

---

## 6. Fluxo completo de execução

Para uso diário, após a configuração inicial, o processo básico para executar o client será:

```bash
cd /caminho/do/projeto
source .venv/bin/activate
python3 -m client.application.pages.main
```

Caso as dependências ainda não tenham sido instaladas, execute antes:

```bash
pip install customtkinter Pillow CTkMessagebox
```

---

## 7. Possíveis problemas e soluções

### 7.1. Erro informando que `venv` não existe

Se o comando abaixo falhar:

```bash
python3 -m venv .venv
```

Instale o pacote de suporte a ambientes virtuais:

```bash
sudo apt install -y python3-venv
```

Depois, tente criar o ambiente novamente:

```bash
python3 -m venv .venv
```

---

### 7.2. Erro relacionado ao `tkinter`

Se a aplicação apresentar erro relacionado ao `tkinter`, instale o pacote necessário:

```bash
sudo apt install -y python3-tk
```

Depois, tente executar novamente:

```bash
python3 -m client.application.pages.main
```

---

### 7.3. Ambiente virtual não ativado

Se o comando `pip install` instalar pacotes fora do projeto ou se a aplicação não encontrar as dependências, verifique se o ambiente virtual está ativado.

Ative-o com:

```bash
source .venv/bin/activate
```

---

### 7.4. Client não consegue se conectar ao servidor

Verifique se:

1. O servidor está em execução.
2. A VM do client consegue acessar o endereço IP configurado para o servidor.
3. A rede interna da VM está configurada corretamente.
4. O endereço IP esperado para o servidor é `192.168.0.1`.
5. A porta utilizada pelo servidor está liberada e acessível.

Para testar conectividade básica, pode-se usar:

```bash
ping 192.168.0.1
```

---

## 8. Resumo dos comandos principais

### Instalação da interface gráfica

```bash
sudo apt update
sudo apt install -y xfce4 xfce4-goodies python3-tk
sudo reboot
```

### Criação do ambiente virtual

```bash
cd /caminho/do/projeto
sudo apt install -y python3-venv
python3 -m venv .venv
source .venv/bin/activate
```

### Instalação das dependências do client

```bash
pip install customtkinter Pillow CTkMessagebox
```

### Execução do client

```bash
python3 -m client.application.pages.main
```