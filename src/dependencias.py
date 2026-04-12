from core.configuracoes import Sessionlocal

# Empresta a sessao do banco de dados sempre que necessário
def sessao():
    sessao_local = Sessionlocal()
    try:
        yield sessao_local
    finally:
        sessao_local.close()