import sqlite3
from flask import request, jsonify
from marshmallow import ValidationError

from models.Avicultor import Avicultor, AvicultorSchema
from helpers.application import app
from helpers.database import get_conn


@app.get("/")
def index():
    return '{"versao":"1.0.1"}', 200


@app.get("/health")
def healthCheck():
    return "{'online':'true'}", 200


@app.get("/avicultores")
def getAvicultores():
    avicultores = []
    # DB
    conn = None
    try:
        conn = get_conn()

        # 2 - Recuperar o cursor
        cursor = conn.cursor()

        # 3 - Preparar a consultar: query | statement
        cursor.execute("select * from tb_avicultores")

        # 4.1 - Iterar nos resultados: resultset (fetchall, fecthone)
        rows = cursor.fetchall()

        for row in rows:
            id = row[0]
            nome = row[1]
            nascimento = row[2]
            cpf = row[3]
            caf = row[4]
            avicultor = Avicultor(id, nome, nascimento, cpf, caf)
            avicultores.append(avicultor.toDict())

    except sqlite3.Error as e:
        print(e)
    finally:
        # 5 - Fechar a conexão
        if conn:
            conn.close()

    return avicultores, 200


@app.post("/avicultores")
def postAvicultores():
    avicultorJson = request.get_json()
    # DB
    conn = None
    try:
        avicultorSchema = AvicultorSchema()
        avicultorData = avicultorSchema.load(avicultorJson)

        # 1 - Abrir a conexão
        conn = get_conn()

        # 2 - Recuperar o cursor
        cursor = conn.cursor()

        # 3 - Preparar a consultar: query | statement
        cursor.execute(
            "INSERT INTO tb_avicultores(nome, nascimento, cpf, caf) VALUES(?, ?, ?, ?)", (avicultorData["nome"], avicultorData["nascimento"], avicultorData["cpf"], avicultorData["caf"]))

        # 4.2 - Confirmar operação.
        conn.commit()
    except sqlite3.Error as e:
        print(e)
    except ValidationError as err:
        return jsonify(err.messages), 400
    finally:
        # 5 - Fechar a conexão
        if conn:
            conn.close()

    return avicultorJson, 200


@app.put("/avicultores")
def putAvicultores():
    pass


@app.delete("/avicultores")
def deleteAvicultores():
    pass

# /avicultores - nome, cpf, caf, nascimento
# /avicolas
# /aviarios ou /galpoes
