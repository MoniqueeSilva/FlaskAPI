from flask import Flask, request, jsonify
from models.Avicultor import Avicultor
import json
import os

app = Flask(__name__)

ARQUIVO = "avicultores.json"

@app.get("/")
def index():
    return '{"versao":"1.0.1"}', 200

@app.get("/health")
def healthCheck():
    return "{'online':'true'}", 200

@app.get("/avicultores")
def getAvicultores():
    if not os.path.exists(ARQUIVO):
        return [], 200

    with open(ARQUIVO, "r") as f:
        dados = json.load(f)
    
    return jsonify(dados), 200

@app.post("/avicultores")
def postAvicultores():
    corpo = request.get_json()
    novo = Avicultor(
        nome=corpo.get("nome"),
        nascimento=corpo.get("nascimento"),
        cpf=corpo.get("cpf"),
        caf=corpo.get("caf")
    )

    lista = []
    if os.path.exists(ARQUIVO):
        with open(ARQUIVO, "r") as f:
            lista = json.load(f)

    lista.append(novo.toDict())

    with open(ARQUIVO, "w") as f:
        json.dump(lista, f, indent=4)

    return {"mensagem": "Cadastrado!"}, 201

@app.put("/avicultores/<cpf>")
def putAvicultores(cpf):
    corpo = request.get_json()
    
    if not os.path.exists(ARQUIVO):
        return {"erro": "Arquivo não encontrado"}, 404

    with open(ARQUIVO, "r") as f:
        lista = json.load(f)

    for item in lista:
        if item["cpf"] == cpf:
            item["nome"] = corpo.get("nome")
            item["nascimento"] = corpo.get("nascimento")
            item["caf"] = corpo.get("caf")
            break

    with open(ARQUIVO, "w") as f:
        json.dump(lista, f, indent=4)

    return {"mensagem": "Dados atualizados"}, 200

@app.delete("/avicultores/<cpf>")
def deleteAvicultores(cpf):
    if not os.path.exists(ARQUIVO):
        return {"erro": "Arquivo vazio"}, 404

    with open(ARQUIVO, "r") as f:
        lista = json.load(f)

    nova_lista = [a for a in lista if a["cpf"] != cpf]

    with open(ARQUIVO, "w") as f:
        json.dump(nova_lista, f, indent=4)

    return {"mensagem": "Avicultor foi removido"}, 200

if __name__ == "__main__":
    app.run(debug=True)