from dataclasses import dataclass


@dataclass(repr=False)
class Usuario:
    """
     Esta classe é a base para os cenários da Base A e B já que suas estruturas são semelhantes e precisamos
     de uma chave de pesquisa para o endpoint.
    """
    cpf: int
    idade: int
    nome: str
    endereco: str