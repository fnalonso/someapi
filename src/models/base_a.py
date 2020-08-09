from dataclasses import dataclass
from typing import List

from src.models import Usuario


@dataclass(repr=False)
class Divida:
    data: str
    cnpj_origem: int
    valor: float


@dataclass(repr=False)
class ConsultaUsuario(Usuario):
    dividas: List[Divida]

