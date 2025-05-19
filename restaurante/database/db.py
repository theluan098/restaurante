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

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS adm (
                   id INTEGER PRIMARY KEY AUTOINCREMENT, 
                   usuario TEXT,
                   senha INTEGER
        )
    ''')

    cursor.execute('''
        INSERT INTO adm (usuario, senha) VALUES (?, ?)
    ''', ('adm', '123'))

    con.commit()
    con.close()


def verificar_login(usuario, senha):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM adm WHERE usuario = ? AND senha = ?", (usuario, senha))
    resultado = cursor.fetchone()
    conn.close()
    return resultado is not None
