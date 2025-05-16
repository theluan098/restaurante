from database.db import criar_tabelas
from views.interface import janela_principal
from utils.dados_iniciais import inserir_mesas_iniciais

if __name__ == "__main__":
    criar_tabelas()
    inserir_mesas_iniciais()
    janela_principal()
