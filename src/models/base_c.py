from dataclasses import dataclass
from typing import List

from src.models import Usuario


@dataclass(repr=False)
class MovimentacaoFinanceira:
    data: str
    valor: float


@dataclass(repr=False)
class Compra:
    data: str
    valor: float
    aprovada: bool


@dataclass(repr=False)
class EventosUsuario(Usuario):
    data_ultima_consulta: str
    movimentacoes: List[MovimentacaoFinanceira]
    ultima_compra: Compra