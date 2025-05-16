import models.cliente as cliente
import models.mesa as mesa
import models.reserva as reserva

def processar_reserva(nome, telefone, email, data, horario, mesa_nome):
    mesas = mesa.listar_mesas()
    mesa_dict = {f"Mesa {num}": mid for mid, num in mesas}
    mesa_id = mesa_dict.get(mesa_nome)

    if mesa_id is None:
        return False  # Mesa inválida

    if not reserva.verificar_disponibilidade(mesa_id, data, horario):
        return False  # Não disponível

    cliente_id = cliente.adicionar_cliente(nome, telefone, email)
    return reserva.fazer_reserva(cliente_id, mesa_id, data, horario)

def get_mesas_para_combobox():
    mesas = mesa.listar_mesas()
    return [f"Mesa {num}" for _, num in mesas]

def get_reservas():
    return reserva.listar_reservas()

def editar_reserva(reserva_id, nova_data, novo_horario, nova_mesa_nome):
    mesas = mesa.listar_mesas()
    mesa_dict = {f"Mesa {num}": mid for mid, num in mesas}
    mesa_id = mesa_dict.get(nova_mesa_nome)

    if reserva.verificar_disponibilidade(mesa_id, nova_data, novo_horario):
        reserva.atualizar_reserva(reserva_id, nova_data, novo_horario, mesa_id)
        return True
    return False

def excluir_reserva(reserva_id):
    reserva.cancelar_reserva(reserva_id)