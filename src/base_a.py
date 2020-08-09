import json

from src.utils.base_a import criar_dados_base_a


def handler(event, context):
    """
        Como o cenario nao impoe a camada de banco de dados, os dados serao originados de uma lista.
        A função sempre
    """
    DB = criar_dados_base_a()

    try:
        cpf = int(event.get("pathParameters").get("cpf"))
        print("Diretamente do DB")
        for usuario in DB:
            if usuario.get("cpf") == cpf:
                return {
                    "statusCode": 200,
                    "body": json.dumps(usuario)
                }
        else:
            return {
                "statusCode": 404,
                "body": json.dumps(dict(message="CPF não encontrado."))
            }

    except ValueError:
        return {
            "statusCode": 400,
            "body": json.dumps(dict(message="CPF Inválido"))
        }
