from dataclasses import asdict
from random import randint, choice

from src.models.base_c import Usuario, EventosUsuario, Compra, MovimentacaoFinanceira


def criar_dados_base_c():
    """
    Gera uma lista de usuarios e suas dividas
    :param total: Quantidade de usuarios que deve ser gerada
    :return: List[Usuario]
    """

    movimentacoes = list()
    for _ in range(randint(2, 7)):
        movimentacoes.append(asdict(
            MovimentacaoFinanceira(data="1900-01-01", valor=float(randint(1, 10000)))
        ))



    return [
        asdict(
            EventosUsuario(
                cpf=12312312312, idade=randint(18, 75), nome="Mr Hardcoded again", endereco="Rua hardcoded",
                data_ultima_consulta="2020-08-09 02:30:00", movimentacoes=movimentacoes,
                ultima_compra=Compra(data="1900-01-01", valor=float(randint(1, 10000)), aprovada=choice([True, False]))
            )
        )
    ]
