# Introdução

Este documento descreve a arquitetura serverless para o cenário hipotético abaixo.

```

Armazenamento
	
	Vamos supor que existam três grandes bases de dados externas que organizam nossas informações.
	A primeira delas, que chamamos de Base A, é extremamente sensível e deve ser protegida com
	os maiores níveis de segurança, mas o acesso a esses dados não precisa ser tão performática. A
	segunda, é a Base B que também possui dados críticos, mas ao contrário da Base A, o acesso
	precisa ser um pouco mais rápido. Uma outra característica da Base B é que além de consultas
	ela é utilizada para extração de dados por meio de algoritmos de aprendizado de máquina. A
	última base, é a Base C, que não possui nenhum tipo de dado crítico, mas precisa de um acesso
	extremamente rápido.

Tráfego
	
	Cada uma das bases existentes, são acessadas por sistemas em duas diferentes arquiteturas: 
	microserviços e nano-serviços. Vale salientar que essas bases de dados são externas, portanto não é
	necessário dissertar sobre suas implementações, apenas suas consumações. Quantos aos payloads
	retornados por esses recursos, o candidato pode usar sua criatividade e definí-los, imaginando quais
	dados seriam importantes de serem retornados por sistemas como esses.
	O primeiro sistema, acessa os seguintes dados da Base A:

		• CPF
		• Nome
		• Endereço
		• Lista de dívidas

	O segundo, acessa a Base B que contém dados para cálculo do Score de Crédito. O Score
	de Crédito é um rating utilizado por instituições de crédito (bancos, imobiliárias, etc) quando
	precisam analisar o risco envolvido em uma operação de crédito a uma entidade.

		• Idade
		• Lista de bens (Imóveis, etc)
		• Endereço
		• Fonte de renda

	O último serviço, acessa a Base C e tem como principal funcionalidade, rastrear eventos relacionados 
	a um determinado CPF.
		
		• Última consulta do CPF em um Bureau de crédito.
		• Movimentação financeira nesse CPF.
		• Dados relacionados a última compra com cartao de crédito vinculado ao CPF.

	Como você resolveria esse problema? Divague sobre os seguintes tópicos e outros que ache
	adequado, sinta-se a vontade para desenhar, escrever, criar diagramas, vídeos, apresentação, ou
	qualquer outro meio que facilite o entendimento por parte dos avaliadores:

		• Tecnologias adotadas
		• Arquitetura utilizada
		• Dados armazenados (já listados ou que você acrescentaria)

Disponibilização dos Dados
	
	Agora que os dados desejados já foram consumidos, processados e armazenados, é necessário que
	eles sejam disponibilizados. Será necessário também desenvolver um meio pelo qual esses dados
	estarão disponíveis. É interessante imaginar os possíveis interessados em consumir esses dados para
	que uma única solução possa ser construída de modo a atender o máximo de situações possíveis.


```


# Solução

Aqui os temas serão separados por camada, a fim de ficar mais simples o entendimento.


## Stack

Será composto por `AWS WAF`, `API Gateway` e `Lambda`. A escolha destes serviços se faz pelo fato de serem serverless e 
dispensarem o processo de orquestração e possuirem uma estratégia de cobrança orientada a eventos. Abaixo uma breve 
razão da escolha de cada serviço:
 
 - AWS WAF: Adiciona uma camada de proteção ao API Gateway contra ataques massivos através de ACLs.
 - API Gateway: Provê HTTPS, acesso por chave de API com customização de consumo baseado em volume/quantidade, autorização 
 através do cognito ou uma função lambda customizada, versionamento de API, documentação de API, exportação do SDK da API 
 para terceiros (Facilita o processo de integração com terceiros), exportação da API no formato openAPI, integração simples 
 com o cloudWatch, scaling transparente com [limites](https://docs.aws.amazon.com/pt_br/apigateway/latest/developerguide/limits.html) 
 que podem ser expandidos pela equipe da AWS e cache das respostas para minimizar o impacto no backend.
 - Lambda: Scaling transparente e integração simples com outros serviços AWS utilizando gatilhos.


## Segurança

Toda a camada de segurança será fornecida pelo API Gateway + WAF. O WAF, neste cenário, tem como papel proteger a API de eventuais ataques DDoS.

O processo de autorização da requisição é feita através de uma chave de api incluída no cabeçalho da requisição (`x-api-key`).
 A chave é gerenciada pelo API Gateway e permite implementar controles de consumo individualmente e, caso a chave se torne pública,
  o processo de invalidação é simples.
  
*IMPORTANTE* Durante os testes pode-se perceber alguma lentidão, mas isto é proveniente da configuração do `serverless.yml` 
para a estratégia de consumo, que está marcada como `region` ao invés de `Edge` que utiliza o cloudfront para distribuição.
Então caso a região padrão do usuário configurado no aws-cli seja `us-east-1`, por exemplo, pode refletir no tempo de resposta.


## Implementação

A implementação do endpoints que buscam os dados na bases citadas na introdução serão em `python` e ficarão no `Lambda`, 
por utilizar o `API Gateway` para fazer todo o processo de segurança da API, se assume que todas as invocações são válidas.
Para reduzir o impacto do acesso ao banco de dados, pode-se ativar o cache de respostas no próprio `API Gateway` e, desta
forma, retirar a necessidade da implementação do controle manual do mesmo. Este modelo permite a configuração do TTL do registro
no cache através do console da AWS.

O processo de deploy foi efetuado utilizando o framework [serverless](http://serverless.com/) e para utilizá-lo é necessário
fazer a [instalação](https://www.serverless.com/framework/docs/getting-started/) do CLI. Também é necessário configurar
o aws cli com credenciais administrativas para que o deploy seja efetuado de forma mais tranquila (O correto é criar
um usuário com as permissões utilizadas na criação do stack).

Após efetuar os passos acima basta clonar este repositório e executar os passos a seguir:

```shell script
    $ cd <diretorio_repo>/

    # Caso tenha interesse, adicione a flag --verbose para acompanhar o processo passo a passo.
    $ sls deploy --stage dev

```

O arquivo de configuração que possui a especificação dos endpoints é o `serverless.yml` que se encontra na raiz. É possível
efetuar a configuração de diversos recursos através dele, [aqui](https://www.serverless.com/framework/docs/providers/aws/guide/serverless.yml/) 
tem um exemplo de arquivo com vários cenários de configuração.


Quando o processo de deploy da API for concluído, os dados de uso (endpoints e chave) serão exibidos no terminal. Então
basta executar o comando abaixo efetuando as substituições indicadas ou utilizar uma ferramenta como o 
[postman](https://www.postman.com/).

```shell script
    $curl -v -X GET -H "x-api-key: <CHAVE_API>" "<ENDPOINT>"
```

### Rotas

As rotas foram pensadas seguindo estritamente o cenário descrito acima.

Foi adicionado o CPF no objeto da base B para que exista uma chave de consulta. 

#### BASE A

Para permitir a visualização do cenário descrito, foi criada uma representação da Divida contendo os atributos data, cnpj_origem e valor.
O CPF 12312312312 está hardcoded para que o endpoint possa ser testado.

Como se trata de um endpoint com dados restritos, não existe nenhuma impl que permita a listagem dos registros.

```
    GET <ENDPOINT>/data/base-a/<cpf>
    
    JSON CONSULTA USUARIO
    {
        cpf: int,
        idade: int
        nome: str,
        endereco: str,
        dividas: [
           {
                data: str, # No código-fonte a data é uma string hardcoded, mas em uma situação real seria a str resultante de strftime()
                cnpj_origem: int,
                valor: float
            }       
        ]
    }
```


#### BASE B

Neste cenário, foi criado um objeto para representar os bens contidos na lista citada. Assim como a base A, como se trata
de um conteúdo sigiloso, as requisições obrigam um número de CPF e neste caso mantém-se o 12312312312 para testes.


```
    GET <ENDPOINT>/data/base-b/<cpf>
    JSON CONSULTA BENS
    {
        cpf: int,
        idade: int,
        nome: str,
        endereco: str,
        bens: [
            {
                tipo: str,
                valor: float
                quitado: bool,
                saldo_devedor: float
            }
        ]
    }

```


#### BASE C

Para a Base C se aproveitou a estrutura do objeto Usuario para que possamos utilizar o CPF como chave de pesquisa. No momento
em que o usuário é localizado e carregado, as chaves excedentes são removidas do objeto. Novamente o CPF para testes é o
12312312312.

A estrutura dos objetos de movimentações e ultima_compra foram pensados para prover a informação mínima sobre o evento.

```
    GET <ENPOINT>/data/base-c/{cpf}

    {
        cpf: int,
        data_ultima_consulta: str,
        movimentacoes: [
            {
                data: str,
                valor: float
            }
        ]
        ultima_compra: {
            data: str,
            valor: float,
            aprovada: bool
        }

    }

``` 

Para este endpoint, que requer um tempo de resposta menor, pode-se ativar o cache de resposta do `API Gateway` ou utilizar o
`Elasticache` para adicionar um cluster Redis no stack. No caso do `Elasticache`, se adiciona o custo por hora de execução
por nó do cluster e para o cache do `API Gateway` se cobra a hora de memória alocada. O único ponto negativo do cache do `API Gateway`
é que ele é feito por stage, ou seja, toda a API utiliza o recurso, mas tem a vantagem de um item a menos para administração.


## Comentários finais

Esta solução provê um modelo de arquitetura enxuto onde a maior responsabilidade de manutenção da estrutura passa para 
a própria AWS. O fato de utilizar-se o `API Gateway` como receptor dos eventos HTTP das funções traz o benefício de 
reduzir as preocupações que um programador normalmente teria e o permite focar mais na implementação da lógica de 
negócio em si, porém requer mais dedicação do time de arquitetura no processo de configuração do serviço.


O processo de cache é um ponto de atenção, uma vez que pode gerar custos adicionais devido ao modelo de configuração 
quando aplicado diretamente no `API Gateway`. Uma estratégia possível é separar o deploy e criar uma API separada 
para os cenários onde o cache é requisito.

Uma justificativa para o uso do modelo proposto acima é a redução de custo que se pode atingir. Utilizando este 
[site](http://serverlesscalc.com/) pode se ter uma ideia superficial de custos. 