from flask import Flask, jsonify
from models.Avicultor import Avicultor
import sqlite3

DATABASE_NAME = "avicola.db"

app = Flask(__name__)

avicultor1 = Avicultor("João Silva", "1980-05-12", "123.456.789-00", "CAF001")
avicultor2 = Avicultor("Maria Oliveira", "1975-11-30",
                       "987.654.321-11", "CAF002")
avicultor3 = Avicultor("Carlos Santos", "1990-02-20",
                       "111.222.333-44", "CAF003")
avicultor4 = Avicultor("Ana Costa", "1985-07-18", "555.666.777-88", "CAF004")
avicultor5 = Avicultor("Pedro Lima", "1978-09-05", "999.888.777-66", "CAF005")
avicultor6 = Avicultor("Luciana Pereira", "1992-03-15",
                       "444.333.222-11", "CAF006")
avicultor7 = Avicultor("Rafael Gomes", "1983-12-25",
                       "222.111.333-55", "CAF007")
avicultor8 = Avicultor("Beatriz Almeida", "1995-06-10",
                       "666.555.444-33", "CAF008")
avicultor9 = Avicultor("Thiago Rocha", "1988-01-02",
                       "777.888.999-00", "CAF009")
avicultor10 = Avicultor("Carla Mendes", "1991-08-22",
                        "333.444.555-66", "CAF010")

# Exemplo de como transformar cada instância em dicionário
avicultores = [avicultor1, avicultor2, avicultor3, avicultor4, avicultor5,
               avicultor6, avicultor7, avicultor8, avicultor9, avicultor10]


@app.get("/")
def index():
    return '{"versao":"1.0.1"}', 200


@app.get("/health")
def healthCheck():
    return "{'online':'true'}", 200


@app.get("/avicultores")
def getAvicultores():
    avicultoresDict = []

    # DB
    conn = None
    try:
        # 1 - Abrir a conexão
        conn = sqlite3.connect(DATABASE_NAME)

        # 2 - Recuperar o cursor
        cursor = conn.cursor()

        # 3 - Preparar a consultar: query | statement
        cursor.execute("select * from tb_avicultor")

        # 4.1 - Iterar nos resultados: resultset (fetchall, fecthone)
        # 4.2 - Confirmar operação.

        for item in avicultores:
            avicultoresDict.append(item.toDict())

    except sqlite3.Error as e:
        print(e)
    finally:
        # 5 - Fechar a conexão
        if conn:
            conn.close()

    return avicultoresDict, 200


@app.post("/avicultores")
def postAvicultores():
    pass


@app.put("/avicultores")
def putAvicultores():
    pass


@app.delete("/avicultores")
def deleteAvicultores():
    pass

# /avicultores - nome, cpf, caf, nascimento
# /avicolas
# /aviarios ou /galpoes
