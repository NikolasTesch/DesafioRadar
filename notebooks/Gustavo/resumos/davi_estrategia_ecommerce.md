# Resumo didático — `Analise_Estrategica_Ecommerce.ipynb`

## O que este notebook quis responder

Este notebook investiga uma pergunta central de negócio: **a logística está afetando a satisfação do cliente no e-commerce?**  
A ideia é entender se atrasos, frete e características do produto ajudam a explicar por que alguns pedidos recebem avaliações boas e outros recebem avaliações ruins.

Em termos simples, o notebook tenta sair do “achismo” e mostrar, com dados, se a experiência de entrega está prejudicando a percepção da marca e a chance de recompra.

## Bases de dados utilizadas

O autor integrou várias tabelas do ecossistema Olist para montar uma visão completa da compra:

- `olist_orders_dataset.csv`: pedidos e datas do processo logístico
- `olist_order_items_dataset.csv`: itens de cada pedido
- `olist_customers_dataset.csv`: cliente e localização de destino
- `olist_sellers_dataset.csv`: vendedor e origem do produto
- `olist_products_dataset.csv`: peso, tamanho, categoria e atributos do produto
- `olist_order_reviews_dataset.csv`: nota dada pelo cliente
- `olist_order_payments_dataset.csv`: pagamentos e valor financeiro

Depois dos merges, o notebook informa uma **base consolidada com 112.650 linhas e 31 colunas**, permitindo analisar logística, produto, pagamento e avaliação no mesmo conjunto.

## O que foi feito na preparação dos dados

O notebook faz uma etapa importante de engenharia de variáveis. Isso significa criar colunas novas que traduzem melhor o problema de negócio. As principais são:

- **Tempo real de entrega**: quantos dias o cliente esperou entre a aprovação e a entrega
- **Dias de atraso**: diferença entre a data real de entrega e a data prometida
- **Flag de atraso**: indicador binário para separar pedidos atrasados dos entregues no prazo
- **Frequência de compra**: tentativa de capturar recompra por cliente
- **Taxa de frete sobre o produto**: proporção entre frete e preço, útil para entender a “dor” do frete

Também há tratamento de datas e limpeza de valores anômalos para evitar distorções nas métricas.

## Principais análises realizadas

### 1. Relação entre nota e tempo de entrega
O notebook compara as notas de avaliação com o tempo real de entrega e mostra, por meio de boxplots, que pedidos associados a notas mais baixas tendem a ter tempos de entrega maiores.

### 2. Teste estatístico entre pedidos no prazo e atrasados
Aqui aparece um dos pontos mais fortes do notebook. O autor compara a média das notas entre dois grupos:

- pedidos entregues no prazo
- pedidos atrasados

O resultado reportado no próprio notebook é:

- **Média da nota no prazo: 4,21**
- **Média da nota atrasado: 2,55**
- **p-value ≈ 0,00000**

Em linguagem simples: a diferença não parece aleatória. O atraso está fortemente associado a uma pior avaliação do cliente.

### 3. Matriz de correlação
O notebook calcula correlações entre variáveis como:

- `review_score`
- `tempo_real_entrega_dias`
- `dias_atraso`
- `freight_value`
- `price`
- `product_photos_qty`
- `product_weight_g`

A leitura executiva proposta é que **tempo de entrega e atraso se relacionam negativamente com a nota**. Já peso e frete ajudam a explicar dificuldade operacional, mas não necessariamente geram insatisfação sozinhos se o prazo prometido for cumprido.

### 4. Visualizações de negócio
O notebook também cria gráficos interativos para observar:

- evolução mensal de receita
- volume de pedidos
- categorias e recortes mais ligados à operação logística

Esses gráficos ajudam a transformar a análise em algo útil para acompanhamento por áreas como BI, logística e operação.

### 5. Tentativa de modelagem preditiva
O autor propõe uma **regressão logística** para prever risco de atraso com base em:

- frete
- preço
- peso do produto
- quantidade de fotos do produto

Essa parte é conceitualmente interessante, porque tenta transformar análise descritiva em alerta preditivo.  
Porém, no arquivo enviado, **a célula do modelo termina com erro e a modelagem não foi concluída nem validada**. Então ela deve ser lida como uma proposta de caminho, não como resultado consolidado.

## Principais insights do notebook

1. **Atraso logístico derruba a satisfação do cliente de forma muito forte.**  
   Esse é o principal achado. A diferença entre nota média de pedidos no prazo e atrasados é muito grande.

2. **Cumprir a promessa importa tanto quanto — ou mais do que — apenas reduzir custo.**  
   O notebook sugere que o cliente reage com muita força quando a promessa de entrega é quebrada.

3. **Frete, peso e complexidade do produto ajudam a identificar risco operacional.**  
   Eles não explicam tudo sozinhos, mas ajudam a sinalizar pedidos mais difíceis.

4. **A análise tem valor executivo.**  
   O material não fica só na estatística: ele aponta utilidade prática para operação, monitoramento de risco e retenção de clientes.

## O que esse notebook agrega para o “grande resumo”

Este notebook é importante porque constrói a ponte entre duas áreas que muitas vezes são tratadas separadamente:

- **logística**
- **experiência do cliente**

A contribuição mais forte dele é mostrar que **problemas de entrega não ficam restritos ao operacional; eles viram problema de reputação, recompra e valor do cliente no longo prazo**.

## Limites e cuidados ao apresentar

Ao apresentar este notebook, vale destacar um ponto com honestidade:

- a parte de **modelagem preditiva não foi concluída no arquivo enviado**
- portanto, os resultados mais confiáveis são os de **integração dos dados, engenharia de variáveis, EDA e teste estatístico**
- não é correto afirmar que o notebook “provou” capacidade preditiva de atraso, porque essa etapa não foi finalizada

## Conclusão em linguagem simples

Se fosse para explicar este notebook para alguém de fora da área, eu resumiria assim:

> O estudo mostra que, quando a entrega atrasa, a nota do cliente cai muito.  
> Ou seja: logística ruim não é só um problema de transporte; ela afeta diretamente a imagem da empresa, a satisfação e a chance de o cliente voltar a comprar.
