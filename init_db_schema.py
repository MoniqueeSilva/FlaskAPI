import sqlite3

DATABASE_NAME = "avicola.db"

conn = None
try:
    # 1 - Abrir a conexão
    conn = sqlite3.connect(DATABASE_NAME)

    # 2 - Recuperar o cursor
    cursor = conn.cursor()

    # 3 - Preparar a consultar: query | statement
    with open('schema.sql', mode='r') as file:
        cursor.executescript(file.read())

    # 4.1 - Iterar nos resultados: resultset.
    # 4.2 - Confirmar operação.
    conn.commit()
except sqlite3.Error as e:
    print(e)
finally:
    # 5 - Fechar a conexão
    if conn:
        conn.close()
