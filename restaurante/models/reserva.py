import database.db as banco

def verificar_disponibilidade(mesa_id, data, horario):
    con = banco.conectar()
    cursor = con.cursor()
    cursor.execute("SELECT * FROM reservas WHERE mesa_id=? AND data=? AND horario=?", (mesa_id, data, horario))
    resultado = cursor.fetchone()
    con.close()
    return resultado is None

def fazer_reserva(cliente_id, mesa_id, data, horario):
    if verificar_disponibilidade(mesa_id, data, horario):
        con = banco.conectar()
        cursor = con.cursor()
        cursor.execute("INSERT INTO reservas (cliente_id, mesa_id, data, horario) VALUES (?, ?, ?, ?)", (cliente_id, mesa_id, data, horario))
        con.commit()
        con.close()
        return True
    return False

def listar_reservas():
    con = banco.conectar()
    cursor = con.cursor()
    cursor.execute("""
        SELECT reservas.id, clientes.nome, mesas.numero, mesas.capacidade, reservas.data, reservas.horario
        FROM reservas
        JOIN clientes ON reservas.cliente_id = clientes.id
        JOIN mesas ON reservas.mesa_id = mesas.id
        ORDER BY reservas.data, reservas.horario
    """)
    resultado = cursor.fetchall()
    con.close()
    return resultado

def atualizar_reserva(reserva_id, data, horario, mesa_id):
    con = banco.conectar()
    cursor = con.cursor()
    cursor.execute("UPDATE reservas SET data=?, horario=?, mesa_id=? WHERE id=?", (data, horario, mesa_id, reserva_id))
    con.commit()
    con.close()

def cancelar_reserva(reserva_id):
    con = banco.conectar()
    cursor = con.cursor()
    cursor.execute("DELETE FROM reservas WHERE id = ?", (reserva_id,))
    con.commit()
    con.close()