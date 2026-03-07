# Resumo didático — `02_analise_regionalidade.ipynb`

## O que este notebook quis responder

Este notebook investiga como a **geografia brasileira influencia o desempenho do e-commerce**.  
A pergunta central é: **as diferenças regionais de venda, frete e prazo acontecem por acaso ou refletem uma estrutura logística desigual?**

O estudo vai além de mostrar “quem vende mais”. Ele tenta explicar **por que certas regiões compram mais, recebem mais rápido e pagam menos**, enquanto outras ficam penalizadas.

## Bases de dados utilizadas

O notebook integra várias fontes da Olist para montar a análise:

- clientes
- pedidos
- itens do pedido
- produtos
- pagamentos
- geolocalização implícita por estado/região
- vendedores, na segunda parte do estudo

A lógica principal é conectar **origem da mercadoria** com **destino do cliente**, para analisar custo e tempo de entrega de forma territorial.

## O que foi feito na preparação dos dados

O notebook faz uma série de etapas importantes:

- agrega itens por pedido para obter preço e frete totais do carrinho
- junta os dados de pedido com cliente e região
- cria métricas como:
  - **preço total**
  - **frete**
  - **tempo de espera em dias**
  - região do cliente
  - região do vendedor
- constrói visões por estado e por região
- separa análises de:
  - volume de vendas
  - custo logístico
  - tempo de entrega
  - fluxo origem-destino

Essa preparação é essencial porque o notebook quer explicar a desigualdade logística, e isso exige enxergar o trajeto da venda de ponta a ponta.

## Principais análises realizadas

### 1. Volume de vendas por região
O notebook mostra uma **forte concentração de pedidos no Sudeste**.  
O próprio texto do autor destaca que o Sudeste responde por mais de 70% da massa de vendas do dataset.

Em linguagem simples: a maior parte do mercado analisado está concentrada nessa região.

### 2. Medianas de frete e tempo de entrega por região
Depois de olhar volume, o notebook compara:

- valor mediano do frete
- tempo mediano de entrega

Essa comparação mostra um padrão claro:

- **Sudeste**: frete mais baixo e entrega mais rápida
- **Norte**: frete mais alto e entrega muito mais lenta
- **Nordeste e Centro-Oeste**: situação intermediária, mas ainda mais penalizada que o Sudeste

### 3. Boxplots para entender dispersão
O autor usa boxplots para enxergar não apenas a média, mas a distribuição do frete e do prazo.  
Isso é importante porque duas regiões podem ter médias parecidas, mas comportamentos muito diferentes.

A leitura do notebook reforça que o Norte apresenta um salto visível no tempo de entrega e nas caudas de custo.

### 4. Análise por estado com gráfico de bolhas
Em uma etapa mais analítica, o notebook agrupa dados por estado e cria uma visualização que cruza:

- frete
- tempo de entrega
- região
- volume de vendas

A interpretação proposta é bastante clara:

- os estados do Sudeste se concentram em uma zona “favorável”, com frete menor, prazo menor e mais vendas
- estados mais distantes, especialmente do Norte, ficam na zona oposta, com frete alto, prazo longo e menor escala de vendas

### 5. Parte 2 — origem vs destino
Essa é uma das partes mais fortes do notebook.  
O autor traz a base de vendedores para investigar se o problema é apenas distância ou se existe um **desequilíbrio estrutural na origem das mercadorias**.

O achado principal é que há forte concentração de vendedores em São Paulo, o que faz com que grande parte das mercadorias precise viajar do Sudeste para outras regiões.

### 6. Matriz de fluxo inter-regional
Com uma tabela dinâmica de origem x destino, o notebook mostra que a logística funciona quase como uma “mão única”:

- muitos produtos saem do Sul/Sudeste
- muitos consumidores estão em outras regiões
- isso aumenta a dependência de transporte inter-regional

### 7. Comparação entre frete intra-regional e inter-regional
O notebook conclui que, quando a venda acontece dentro da mesma região, o frete tende a cair bastante.  
O grande problema é que muitas regiões não têm densidade suficiente de vendedores locais, o que força o fluxo vindo de fora.

## Principais insights do notebook

1. **A desigualdade regional do e-commerce não é apenas comercial; ela é logística.**  
   Regiões com frete alto e prazo longo ficam naturalmente menos competitivas.

2. **O Sudeste é favorecido por concentração de mercado e de oferta.**  
   Ele vende mais, entrega mais rápido e opera com menor fricção logística.

3. **O Norte é a região mais penalizada.**  
   O notebook mostra que essa região sofre com fretes muito altos, prazos longos e baixa representatividade de volume.

4. **A concentração de vendedores em São Paulo é peça-chave para explicar o problema.**  
   Isso cria dependência estrutural de envios longos para outras regiões.

5. **Frete intra-regional tende a ser muito mais eficiente.**  
   Ou seja: ampliar a presença regional de vendedores e estoques pode ser uma alavanca real de melhoria.

## O que esse notebook agrega para o “grande resumo”

Este notebook é importante porque fornece a **base estrutural** para os outros estudos do Edvan.  
Ele mostra que o problema não é só “o Norte compra menos” ou “o Nordeste demora mais”, mas sim que existe uma arquitetura logística desigual por trás disso.

Em outras palavras: ele ajuda a explicar a raiz do problema.

## Recomendações de negócio sugeridas no material

A partir do notebook e do relatório associado, as ações mais coerentes são:

- criar ou aproximar centros de distribuição de regiões penalizadas
- incentivar entrada de vendedores locais em regiões menos atendidas
- trabalhar estratégias de frete e mix de produto por região
- reduzir dependência de origem concentrada no Sudeste

## Conclusão em linguagem simples

Se fosse para explicar este notebook para alguém de fora da área, eu diria:

> O estudo mostra que vender para o Brasil não custa a mesma coisa em todo lugar.  
> O Sudeste está mais perto da oferta e por isso compra mais barato e recebe mais rápido.  
> Já regiões mais distantes sofrem porque boa parte dos produtos precisa sair de longe, principalmente de São Paulo.  
> Isso encarece o frete, aumenta o prazo e enfraquece as vendas.
