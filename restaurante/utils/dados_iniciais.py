import database.db as banco

def inserir_mesas_iniciais():
    con = banco.conectar()
    cursor = con.cursor()
    for i in range(1, 11):
        try:
            cursor.execute("INSERT INTO mesas (numero, capacidade) VALUES (?, ?)", (i, 4))
        except:
            pass  # Mesa já existe
    con.commit()
    con.close()