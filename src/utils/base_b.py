from dataclasses import asdict
from random import randint, choice

from src.utils import TIPOS_BEM
from src.models.base_b import Bem, ConsultaBens


def criar_dados_base_b():
    """
    Gera uma lista de usuarios e suas dividas
    :param total: Quantidade de usuarios que deve ser gerada
    :return: List[Usuario]
    """

    bens = list()
    for _ in range(randint(1, 3)):
        bens.append(
            asdict(Bem(tipo=choice(TIPOS_BEM), valor=float(randint(30000, 150000)), quitado=choice([True, False]),
                       saldo_devedor=float(randint(0, 10000)))
        ))

    return [
        asdict(ConsultaBens(
                cpf=12312312312, idade=randint(18, 75), nome="Mr Hardcoded", endereco="Rua do Harcoded",
                bens=bens
            )
        )
    ]
