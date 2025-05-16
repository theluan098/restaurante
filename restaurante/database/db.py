import sqlite3

def conectar():
    return sqlite3.connect('restaurante.db')

def criar_tabelas():
    con = conectar()
    cursor = con.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            telefone TEXT NOT NULL,
            email TEXT)
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS mesas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            numero INTEGER NOT NULL UNIQUE,
            capacidade INTEGER NOT NULL)
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS reservas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente_id INTEGER,
            mesa_id INTEGER,
            data TEXT,
            horario TEXT,
            FOREIGN KEY(cliente_id) REFERENCES clientes(id),
            FOREIGN KEY(mesa_id) REFERENCES mesas(id))
    ''')

    con.commit()
    con.close()