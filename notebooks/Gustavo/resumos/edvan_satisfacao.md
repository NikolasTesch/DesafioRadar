# Resumo didático — `03_analise_satisfacao.ipynb`

## O que este notebook quis responder

Este notebook analisa a relação entre **satisfação do cliente** e **desempenho logístico**.  
A pergunta central é: **os clientes avaliam mal porque o produto é ruim ou porque a entrega demora?**

O foco do estudo é mostrar, com dados, se o atraso e o tempo de espera estão ligados à piora da nota dada pelos consumidores.

## Bases de dados utilizadas

O notebook cruza dados de:

- pedidos
- clientes
- avaliações (`review_score`)
- datas de compra e entrega
- região de destino

Assim, ele consegue olhar a experiência do cliente em duas dimensões ao mesmo tempo:

- **tempo de espera**
- **nota atribuída à compra**

## Preparação e tratamento dos dados

O notebook lê a base de avaliações, mantém as colunas de nota e pedido e depois cruza essas informações com a base logística criada anteriormente.

A variável mais importante gerada aqui é:

- **`tempo_espera_dias`**: diferença entre o momento da compra e a entrega ao cliente

Além disso, o notebook classifica os clientes entre:

- **detratores**: notas 1 e 2
- **neutros/promotores**: notas 3, 4 e 5

Essa separação facilita transformar nota em leitura de negócio e de experiência do cliente.

## Principais análises realizadas

### 1. Tempo de espera por nota
O notebook calcula o tempo médio de espera para cada faixa de avaliação.  
A interpretação apresentada é muito direta:

- clientes com **nota 5** receberam mais rápido
- clientes com **nota 1** esperaram muito mais

No relatório associado, esse contraste aparece de forma ainda mais explícita:

- **Nota 5**: média de cerca de **9,7 dias**
- **Nota 1**: média de cerca de **21 dias**

Em termos simples: quanto mais o cliente espera, pior tende a ser sua avaliação.

### 2. Relação entre logística e reputação
O estudo argumenta que a insatisfação digital não vem apenas da qualidade do produto, mas da experiência logística como um todo.  
Ou seja, mesmo que o item esteja correto, o atraso pode contaminar a percepção da compra.

### 3. Distribuição regional dos detratores
Depois de mostrar a relação geral entre prazo e nota, o notebook cruza o comportamento com a geografia.  
A conclusão é que regiões mais penalizadas logisticamente também concentram uma fatia maior de clientes insatisfeitos.

O relatório associado destaca especialmente:

- **Sudeste** com menor taxa de detratores
- **Norte** com taxa muito mais alta de clientes profundamente insatisfeitos
- **Nordeste** também em patamar preocupante

### 4. Leitura de Customer Success
O notebook não fica só na estatística. Ele traduz o achado em linguagem de operação e atendimento ao cliente:

- atraso logístico destrói reputação
- reputação ruim aumenta custo de aquisição perdido
- clientes insatisfeitos têm menor chance de recompra

## Principais insights do notebook

1. **Tempo de entrega e satisfação estão fortemente ligados.**  
   O estudo mostra uma diferença clara entre o tempo de espera dos clientes que deram nota alta e os que deram nota baixa.

2. **Atraso logístico afeta a imagem da empresa.**  
   O cliente costuma avaliar a experiência inteira, e não separar perfeitamente o vendedor da transportadora.

3. **A dor não é igual em todas as regiões.**  
   Regiões com maior dificuldade logística tendem a concentrar mais detratores.

4. **O problema deixa de ser apenas operacional e vira problema de retenção.**  
   Quando a experiência piora, a chance de recompra e o valor de longo prazo do cliente também pioram.

## O que esse notebook agrega para o “grande resumo”

Este notebook é importante porque faz a ponte entre:

- operação logística
- experiência do cliente
- impacto de negócio

Ele mostra que frete e prazo não afetam apenas custo: eles afetam reputação, fidelização e retorno do investimento em aquisição de clientes.

## Ações sugeridas pelo material

Com base no notebook e no relatório de apoio, algumas ações lógicas seriam:

- disparar comunicação proativa para pedidos com risco de atraso
- criar ações de retenção ou compensação em regiões mais afetadas
- monitorar pedidos que ultrapassem um limiar de tempo crítico
- tratar logística e atendimento de forma integrada

## Conclusão em linguagem simples

Se fosse para explicar este notebook para alguém de fora da área, eu diria:

> O estudo mostra que o cliente não olha apenas para o produto.  
> Se a entrega demora demais, a nota cai, a reputação piora e a chance de esse cliente voltar a comprar diminui.  
> Em regiões onde a logística já é mais difícil, esse problema fica ainda mais forte.
