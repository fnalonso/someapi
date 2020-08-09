from dataclasses import asdict
from random import randint, choice

from src.models.base_a import ConsultaUsuario, Divida
from src.utils import CNPJS


def criar_dados_base_a():
    """
    Gera uma lista de usuarios e suas dividas
    :param total: Quantidade de usuarios que deve ser gerada
    :return: List[Usuario]
    """

    dividas = list()
    for _ in range(randint(1, 6)):
        dividas.append(
            asdict(Divida(data="1900-01-01", cnpj_origem=choice(CNPJS), valor=randint(100, 10000) * 1.0))
        )

    return [
        asdict(
            ConsultaUsuario(
                cpf=12312312312, idade=randint(18, 75), nome="Mr Hardcoded", endereco="Rua do Harcoded",
                dividas=dividas
            )
        )
    ]
