# Resumo didático — `04_analise_categorias.ipynb`

## O que este notebook quis responder

Este notebook analisa a relação entre **categorias de produto, região e sensibilidade ao frete**.  
A pergunta central é: **os consumidores de diferentes regiões compram coisas muito diferentes, ou o que muda de verdade é o valor do item que compensa o frete?**

É uma análise muito útil para marketing e inteligência comercial, porque ajuda a pensar em mix de produto, mídia e estratégia regional.

## Bases de dados utilizadas

O notebook usa uma base integrada com:

- pedidos
- clientes e região
- itens vendidos
- produtos e categorias
- tradução das categorias
- preço e frete

Isso permite olhar simultaneamente:

- o que está sendo vendido
- em que região
- por qual preço
- sob qual custo logístico

## Preparação e tratamento dos dados

O autor monta uma base com foco em produto e comportamento regional.  
Entre os cuidados importantes, aparecem:

- padronização e tradução das categorias
- agrupamento de vendas por categoria e por região
- cálculo de participação percentual das categorias dentro de cada região
- filtragem de itens com preço acima de **R$ 1.000** para evitar que produtos de luxo distorçam a análise da massa principal de consumo

Esse filtro é importante porque o objetivo é entender comportamento médio, e não extremos.

## Principais análises realizadas

### 1. Top categorias por região
O notebook compara o peso relativo das categorias dentro de cada região.  
A interpretação é que o mix principal é bastante parecido no país.

As categorias que aparecem com destaque recorrente são:

- saúde e beleza
- cama, mesa e banho
- esportes e lazer

Em linguagem simples: o gosto geral do consumidor não muda tanto assim de uma região para outra.

### 2. Comparação do ticket dos produtos por região
Depois de mostrar que o mix é parecido, o notebook muda a pergunta: se o gosto não muda tanto, então por que o comportamento de compra muda?

A resposta proposta é que a diferença está no **ticket do item que o cliente aceita comprar**.  
Regiões mais penalizadas pelo frete acabam comprando itens de valor maior, porque o frete pesa menos proporcionalmente sobre o preço do produto.

### 3. Boxplot de preço dos produtos por região
Para isso, o notebook usa gráficos de distribuição e também calcula a mediana do preço por região.

A conclusão apresentada é:

- **Sudeste**: consegue sustentar compra de itens mais baratos porque o frete é relativamente mais baixo
- **Norte/Nordeste**: tendem a concentrar compras em itens mais caros, já que pagar frete alto em produto barato se torna economicamente pouco atraente

No relatório complementar, esse contraste aparece de forma bem clara:

- ticket mediano no Sudeste em torno de **R$ 65**
- ticket mediano no Norte/Nordeste perto de **R$ 89–90**

### 4. Leitura de sensibilidade ao frete
Esse é o coração do notebook.  
A ideia não é que o consumidor do Norte ou Nordeste “goste” de produtos mais caros, mas que o frete alto empurra o comportamento de compra nessa direção.

Ou seja, produtos baratos ficam relativamente inviáveis em regiões com logística mais cara.

## Principais insights do notebook

1. **O gosto regional não parece ser a principal explicação.**  
   As categorias mais relevantes se repetem bastante entre as regiões.

2. **O frete altera o tipo de compra viável.**  
   Em regiões com frete alto, o cliente tende a buscar itens de maior valor para que a proporção do frete faça mais sentido.

3. **O Sudeste consegue vender mais produto barato porque opera com frete mais amigável.**  
   Isso amplia o alcance do catálogo de baixo ticket.

4. **Marketing nacional padronizado pode desperdiçar verba.**  
   Se o catálogo anunciado não faz sentido econômico para a região, o clique não necessariamente vira compra.

## O que esse notebook agrega para o “grande resumo”

Este notebook é importante porque conecta logística com **estratégia comercial**.  
Ele mostra que não basta entender onde o frete é caro; é preciso adaptar:

- o tipo de produto ofertado
- a faixa de preço
- o formato da campanha
- a composição da cesta

## Ações sugeridas pelo material

Com base no notebook e no relatório complementar, algumas ações coerentes seriam:

- adaptar mídia e campanhas por região
- evitar anunciar itens muito baratos em regiões com frete alto
- usar kits, combos e bundles para elevar o valor da cesta
- trabalhar categorias e faixas de preço compatíveis com a realidade logística local

## Conclusão em linguagem simples

Se fosse para explicar este notebook para alguém de fora da área, eu diria:

> O estudo mostra que as pessoas de regiões diferentes não necessariamente querem coisas muito diferentes.  
> O grande problema é que, onde o frete é caro, produto barato deixa de fazer sentido.  
> Então o comportamento de compra muda não por gosto, mas porque a matemática do frete empurra o cliente para tickets mais altos.
