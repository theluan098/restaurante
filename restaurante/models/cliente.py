import database.db as banco

def adicionar_cliente(nome, telefone, email):
    con = banco.conectar()
    cursor = con.cursor()
    cursor.execute("INSERT INTO clientes (nome, telefone, email) VALUES (?, ?, ?)", (nome, telefone, email))
    con.commit()
    cliente_id = cursor.lastrowid
    con.close()
    return cliente_id

def listar_clientes():
    con = banco.conectar()
    cursor = con.cursor()
    cursor.execute("SELECT id, nome, telefone, email FROM clientes")
    resultado = cursor.fetchall()
    con.close()
    return resultado

def atualizar_cliente(cliente_id, novo_nome, novo_telefone, novo_email):
    con = banco.conectar()
    cursor = con.cursor()
    cursor.execute("UPDATE clientes SET nome = ?, telefone = ?, email = ? WHERE id = ?", (novo_nome, novo_telefone, novo_email, cliente_id))
    con.commit()
    con.close()

def excluir_cliente(cliente_id):
    con = banco.conectar()
    cursor = con.cursor()
    cursor.execute("DELETE FROM clientes WHERE id = ?", (cliente_id,))
    con.commit()
    con.close()