from dataclasses import dataclass
from typing import List

from src.models import Usuario


@dataclass(repr=False)
class Bem:
    tipo: str
    valor: float
    quitado: bool
    saldo_devedor: float


@dataclass(repr=False)
class ConsultaBens(Usuario):
    bens: List[Bem]