def openFolder(path):
    # Deve receber o caminho de uma pasta (seja a pasta que irá guardar os arquivos do usuário; seja uma pasta comum dos diretórios do usuário) e retornar as informações das pastas ou arquivos presentes na mesma.
    # O retorno deve conter o nome do item, o tamanho do item (se for um arquivo, retorne o tamanho em bytes; se for uma pasta, retorne a quantidade de itens presentes nela) e tipo do item (se é uma pasta ou um arquivo).
    # Utilize as propriedades dos objetos (dicionários, na verdade) do Python e, para o envio de retorno ao cliente, transforme a variável que contém os objetos em um arquivo JSON para envio (facilitará o tratamento dos dados após o recebimento).

    # Estrutura do dicionário:
    # dic = {
    #    'name': ['Downloads', 'Documentos', 'Imagens', 'curriculo.txt'],
    #    'size': ['3 itens', '2 itens', '5 itens', '23 kB'],
    #    'type': ['pasta', 'pasta', 'pasta', 'arquivo']
    # }
    return False

def openFile(path):
    # Deve receber o caminho de um aquivo e retornar o conteúdo textual presente no mesmo.
    # O retorno não precisa ser em tipo especial.
    return False

def rootPath(username):
    # Deve pegar o nome do usuário e retornar o caminho de sua pasta raiz.
    # Retorne um caminho fromatado de um modo que possa ser manipulado pela biblioteca os.path.
    # Veja que, caso tenham sido levadas em cosideração as orientações do arquivo "record_data", o nome de usário será o nome da pasta que abriga as informações do próprio usuário.
    pass