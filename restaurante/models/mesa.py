import database.db as banco

def listar_mesas():
    con = banco.conectar()
    cursor = con.cursor()
    cursor.execute("SELECT id, numero FROM mesas")
    resultado = cursor.fetchall()
    con.close()
    return resultado
