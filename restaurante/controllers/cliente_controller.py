import models.cliente as cliente

def get_clientes():
    return cliente.listar_clientes()

def editar_cliente(cliente_id, nome, telefone, email):
    cliente.atualizar_cliente(cliente_id, nome, telefone, email)

def remover_cliente(cliente_id):
    cliente.excluir_cliente(cliente_id)