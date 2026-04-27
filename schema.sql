-- Tabela de avicultores
CREATE TABLE IF NOT EXISTS tb_avicultores(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    nascimento DATE NOT NULL,
    cpf VARCHAR(11) NOT NULL UNIQUE,
    caf VARCHAR(10) NOT NULL
);

-- Tabela de aviários
CREATE TABLE IF NOT EXISTS tb_aviario(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    capacidade INTEGER NOT NULL
);