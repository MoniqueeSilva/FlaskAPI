from flask import Flask, request, jsonify
from models.Avicultor import Avicultor
import json # Importa o módulo json para manipular JSON
import os # Importa o módulo os para verificar a existência de arquivos no sistema de arquivos

app = Flask(__name__) # Cria a instância da aplicação Flask

ARQUIVO = "avicultores.json" # Nome do arquivo JSON que serve como BD para armazenar os avicultores

@app.get("/") # Define uma rota GET para o caminho raiz "/"
def index():
    # Retorna uma string JSON indicando a versão da API e o status HTTP 200 (OK)
    return '{"versao":"1.0.1"}', 200

# Define uma rota GET para "/health"
@app.get("/health")
def healthCheck():
    # Retorna um dicionário (que será convertido para JSON pelo Flask) com status online e código 200
    return "{'online':'true'}", 200

# Define uma rota GET para "/avicultores" (listar todos os avicultores)
@app.get("/avicultores")
def getAvicultores():
    # Verifica se o arquivo JSON não existe
    if not os.path.exists(ARQUIVO):
        # Retorna uma lista vazia, se não houver dados
        return [], 200

    # Abre o arquivo em modo leitura ("r")
    with open(ARQUIVO, "r") as f:
        # Carrega o conteúdo JSON do arquivo para uma lista de dicionários
        dados = json.load(f)
    
    # Retorna os dados no formato JSON
    return jsonify(dados), 200

# Define uma rota POST para "/avicultores" (cadastrar um novo avicultor)
@app.post("/avicultores")
def postAvicultores():
    # Obtém o corpo da requisição em formato JSON
    corpo = request.get_json()
    # Cria uma instância da classe Avicultor com os dados fornecidos
    novo = Avicultor(
        nome=corpo.get("nome"),
        nascimento=corpo.get("nascimento"),
        cpf=corpo.get("cpf"),
        caf=corpo.get("caf")
    )

    # Inicializa uma lista vazia para armazenar os avicultores existentes
    lista = []
    # Verifica se o arquivo JSON já existe
    if os.path.exists(ARQUIVO):
        # Abre o arquivo existente para leitura
        with open(ARQUIVO, "r") as f:
            # Carrega os dados atuais na lista
            lista = json.load(f)
    # Adiciona o novo avicultor
    lista.append(novo.toDict())

    # Abre o arquivo em modo escrita ("w")
    with open(ARQUIVO, "w") as f:
        # Escreve a lista completa de dicionários no arquivo JSON
        json.dump(lista, f, indent=4)
    return {"mensagem": "Cadastrado!"}, 201

# Define uma rota PUT para "/avicultores/<cpf>" (atualizar um avicultor pelo CPF)
@app.put("/avicultores/<cpf>")
def putAvicultores(cpf):
    # Obtém o corpo da requisição com os novos dados
    corpo = request.get_json()
    
    # Verifica se o arquivo JSON não existe
    if not os.path.exists(ARQUIVO):
        return {"erro": "Arquivo não encontrado"}, 404
    # Abre o arquivo para leitura e carrega a lista existente
    with open(ARQUIVO, "r") as f:
        lista = json.load(f)

    # Percorre a lista procurando o avicultor cujo CPF corresponde ao parâmetro da URL
    for item in lista:
        if item["cpf"] == cpf:
            # Atualiza os campos com os novos valores fornecidos
            item["nome"] = corpo.get("nome")
            item["nascimento"] = corpo.get("nascimento")
            item["caf"] = corpo.get("caf")
            break

    # Abre o arquivo novamente para escrita
    with open(ARQUIVO, "w") as f:
        json.dump(lista, f, indent=4)
    return {"mensagem": "Dados atualizados"}, 200

# Define uma rota DELETE para "/avicultores/<cpf>" (remover um avicultor pelo CPF)
@app.delete("/avicultores/<cpf>")
def deleteAvicultores(cpf):
    # Verifica se o arquivo não existe
    if not os.path.exists(ARQUIVO):
        return {"erro": "Arquivo vazio"}, 404

    # Carrega a lista atual do arquivo
    with open(ARQUIVO, "r") as f:
        lista = json.load(f)

    # Cria uma nova lista contendo apenas os avicultores cujo CPF é diferente do informado (filtro)
    nova_lista = [a for a in lista if a["cpf"] != cpf]

    # Escreve a nova lista (sem o avicultor removido) de volta no arquivo
    with open(ARQUIVO, "w") as f:
        json.dump(nova_lista, f, indent=4)
    return {"mensagem": "Avicultor foi removido"}, 200

if __name__ == "__main__":
    app.run(debug=True)