import tkinter as tk
from tkcalendar import DateEntry
from tkinter import ttk, messagebox
from datetime import datetime, timedelta, date
import controllers.reserva_controller as ctrl_res
import controllers.cliente_controller as ctrl_cli

def gerar_horarios():
    inicio = datetime.strptime("17:00", "%H:%M")
    fim = datetime.strptime("22:00", "%H:%M")
    horarios = []
    atual = inicio
    while atual <= fim:
        horarios.append(atual.strftime("%H:%M"))
        atual += timedelta(minutes=30)
    return horarios

def formatar_telefone(event):
    telefone = telefone_entry.get()
    numeros = ''.join(filter(str.isdigit, telefone))[:11]  # Máximo de 11 dígitos

    telefone_formatado = ""
    if len(numeros) >= 2:
        telefone_formatado = f"({numeros[:2]})"
        if len(numeros) >= 7:
            telefone_formatado += f"{numeros[2:7]}-{numeros[7:]}"
        elif len(numeros) > 2:
            telefone_formatado += numeros[2:]
    else:
        telefone_formatado = numeros

    # Atualiza o campo
    telefone_entry.delete(0, tk.END)
    telefone_entry.insert(0, telefone_formatado)

def abrir_nova_reserva():
    janela = tk.Toplevel()
    janela.title("Nova Reserva")

    tk.Label(janela, text="Nome do Cliente").grid(row=0, column=0)
    nome_entry = tk.Entry(janela)
    nome_entry.grid(row=0, column=1)

    tk.Label(janela, text="Telefone").grid(row=1, column=0)
    global telefone_entry
    telefone_entry = tk.Entry(janela)
    telefone_entry.grid(row=1, column=1)
    telefone_entry.bind("<KeyRelease>", formatar_telefone)

    tk.Label(janela, text="E-mail").grid(row=2, column=0)
    email_entry = tk.Entry(janela)
    email_entry.grid(row=2, column=1)

    tk.Label(janela, text="Data").grid(row=3, column=0)
    data_entry = DateEntry(janela, date_pattern="dd-mm-yyyy", locale="pt_BR", mindate=date.today())
    data_entry.grid(row=3, column=1)

    tk.Label(janela, text="Horário").grid(row=4, column=0)
    horarios_disponiveis = gerar_horarios()
    horario_combo = ttk.Combobox(janela, values=horarios_disponiveis, state="readonly")
    horario_combo.grid(row=4, column=1)
    horario_combo.current(0)  # seleciona o primeiro horário por padrão

    tk.Label(janela, text="Mesa").grid(row=5, column=0)
    mesa_combo = ttk.Combobox(janela, values=ctrl_res.get_mesas_para_combobox())
    mesa_combo.grid(row=5, column=1)

    def confirmar():
        nome = nome_entry.get()
        telefone = telefone_entry.get()
        email = email_entry.get()
        data = data_entry.get_date().strftime("%d-%m-%Y")
        horario = horario_combo.get()
        mesa = mesa_combo.get()

        if not (nome and telefone and email and data and horario and mesa):
            messagebox.showwarning("Campos vazios", "Preencha todos os campos!")
            return

        if ctrl_res.processar_reserva(nome, telefone, email, data, horario, mesa):
            messagebox.showinfo("Reserva", "Reserva realizada com sucesso!")
            janela.destroy()
        else:
            messagebox.showerror("Erro", "Mesa indisponível nesse horário.")

    tk.Button(janela, text="Confirmar", command=confirmar).grid(row=6, column=0, columnspan=2, pady=10)


def abrir_edicao():
    janela = tk.Toplevel()
    janela.title("Editar Reserva")

    reservas = ctrl_res.get_reservas()
    reserva_dict = {f"Mesa {r[2]} - {r[1]} ({r[4]} {r[5]})": r[0] for r in reservas}

    tk.Label(janela, text="Selecione a Reserva").pack()
    lista = ttk.Combobox(janela, values=list(reserva_dict.keys()), width=50)
    lista.pack(pady=5)

    tk.Label(janela, text="Data").pack()
    data_entry = DateEntry(janela, date_pattern="dd-mm-yyyy", locale="pt_BR", mindate=date.today())
    data_entry.pack()

    tk.Label(janela, text="Horário").pack()
    horario_combo = ttk.Combobox(janela, values=gerar_horarios(), state="readonly")
    horario_combo.pack()

    tk.Label(janela, text="Mesa").pack()
    mesa_combo = ttk.Combobox(janela, values=ctrl_res.get_mesas_para_combobox())
    mesa_combo.pack()

    def preencher_campos_reserva(event):
        selecionado = lista.get()
        reserva_id = reserva_dict.get(selecionado)
        if reserva_id:
            for r in reservas:
                if r[0] == reserva_id:
                    data_entry.delete(0, tk.END)
                    data_entry.set_date(r[4])
                    horario_combo.set(r[5])
                    mesa_combo.set(f"Mesa {r[2]}")
                    break

    lista.bind("<<ComboboxSelected>>", preencher_campos_reserva)


    def atualizar():
        item = lista.get()
        if item:
            reserva_id = reserva_dict[item]
            data = data_entry.get_date().strftime("%d-%m-%Y")
            mesa_nome = mesa_combo.get()
            ctrl_res.editar_reserva(reserva_id, data, horario_combo.get(), mesa_nome)
            messagebox.showinfo("Atualização", "Reserva atualizada!")
            janela.destroy()

    tk.Button(janela, text="Atualizar", command=atualizar).pack(pady=10)

def abrir_cancelamento():
    janela = tk.Toplevel()
    janela.title("Cancelar Reserva")

    reservas = ctrl_res.get_reservas()
    reserva_dict = {f"Mesa {r[2]} - {r[1]} ({r[4]} {r[5]})": r[0] for r in reservas}

    lista = ttk.Combobox(janela, values=list(reserva_dict.keys()), width=50)
    lista.pack(pady=10)

    def cancelar():
        item = lista.get()
        if item:
            reserva_id = reserva_dict[item]
            ctrl_res.excluir_reserva(reserva_id)
            messagebox.showinfo("Cancelamento", "Reserva cancelada!")
            janela.destroy()

    tk.Button(janela, text="Cancelar Reserva", command=cancelar).pack()

def abrir_gerenciar_clientes():
    janela = tk.Toplevel()
    janela.title("Gerenciar Clientes")

    clientes = ctrl_cli.get_clientes()
    cliente_dict = {f"{c[1]} | Tel: {c[2]} | Email: {c[3]}": c[0] for c in clientes}

    tk.Label(janela, text="Selecione um cliente").pack()
    lista = ttk.Combobox(janela, values=list(cliente_dict.keys()), width=70)
    lista.pack(pady=5)

    tk.Label(janela, text="Nome").pack()
    nome_entry = tk.Entry(janela)
    nome_entry.pack()

    tk.Label(janela, text="Telefone").pack()
    global telefone_entry
    telefone_entry = tk.Entry(janela)
    telefone_entry.pack()
    telefone_entry.bind("<KeyRelease>", formatar_telefone)

    tk.Label(janela, text="E-mail").pack()
    email_entry = tk.Entry(janela)
    email_entry.pack()

    def preencher_campos_cliente(event):
        selecionado = lista.get()
        cliente_id = cliente_dict.get(selecionado)
        if cliente_id:
            for c in clientes:
                if c[0] == cliente_id:
                    nome_entry.delete(0, tk.END)
                    nome_entry.insert(0, c[1])
                    telefone_entry.delete(0, tk.END)
                    telefone_entry.insert(0, c[2])
                    email_entry.delete(0, tk.END)
                    email_entry.insert(0, c[3])
                    break

    lista.bind("<<ComboboxSelected>>", preencher_campos_cliente)

    def atualizar():
        selecionado = lista.get()
        if selecionado:
            cliente_id = cliente_dict[selecionado]
            ctrl_cli.editar_cliente(cliente_id, nome_entry.get(), telefone_entry.get(), email_entry.get())
            messagebox.showinfo("Atualizado", "Cliente atualizado com sucesso.")
            janela.destroy()

    def excluir():
        selecionado = lista.get()
        if selecionado:
            cliente_id = cliente_dict[selecionado]
            if messagebox.askyesno("Confirmação", "Deseja realmente excluir este cliente?"):
                ctrl_cli.remover_cliente(cliente_id)
                messagebox.showinfo("Excluído", "Cliente excluído com sucesso.")
                janela.destroy()

    tk.Button(janela, text="Atualizar Cliente", command=atualizar).pack(pady=5)
    tk.Button(janela, text="Excluir Cliente", command=excluir).pack(pady=5)

def abrir_reservas():
    janela = tk.Toplevel()
    janela.title("Reservas Agendadas")

    reservas = ctrl_res.get_reservas()

    for r in reservas:
        texto = f"{r[1]} - Mesa {r[2]} ({r[4]} {r[5]})"
        tk.Label(janela, text=texto).pack(anchor="w")

def janela_principal():
    root = tk.Tk()
    root.title("Restaurante")
    root.geometry("300x200")

    tk.Button(root, text="Nova Reserva", width=25, command=abrir_nova_reserva).pack(pady=5)
    tk.Button(root, text="Ver Reservas", width=25, command=abrir_reservas).pack(pady=5)
    tk.Button(root, text="Editar Reserva", width=25, command=abrir_edicao).pack(pady=5)
    tk.Button(root, text="Cancelar Reserva", width=25, command=abrir_cancelamento).pack(pady=5)
    tk.Button(root, text="Gerenciar Clientes", width=25, command=abrir_gerenciar_clientes).pack(pady=5)

    root.mainloop()