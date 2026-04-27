import sqlite3

DATABASE_NAME = "avicola.db"

tables = [
    """
        CREATE TABLE IF NOT EXISTS tb_avicultores(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                nascimento DATE NOT NULL,
                cpf VARCHAR(11) NOT NULL UNIQUE,
                caf VARCHAR(10) NOT NULL
            )
    """
]

conn = None
try:
    # 1 - Abrir a conexão
    conn = sqlite3.connect(DATABASE_NAME)

    # 2 - Recuperar o cursor
    cursor = conn.cursor()

    # 3 - Preparar a consultar: query | statement
    for table in tables:
        cursor.execute(table)

    # 4.1 - Iterar nos resultados: resultset.
    # 4.2 - Confirmar operação.
    conn.commit()
except sqlite3.Error as e:
    print(e)
finally:
    # 5 - Fechar a conexão
    if conn:
        conn.close()
