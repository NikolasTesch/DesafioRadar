# Resumo didático — `Analise_Sazonalidade.ipynb`

## O que este notebook quis responder

Este notebook procura entender **como o faturamento e o volume de pedidos variam ao longo do tempo** no e-commerce da Olist.  
A pergunta principal é: **existem padrões repetitivos de demanda que ajudem a empresa a se preparar melhor?**

Em outras palavras, o estudo quer mostrar quando o negócio vende mais, quando vende menos e como esses ciclos podem orientar decisões de marketing, estoque, logística e pricing.

## Bases de dados utilizadas

O notebook cruza principalmente estas bases:

- `olist_orders_dataset.csv`
- `olist_order_items_dataset.csv`
- `olist_order_payments_dataset.csv`
- `olist_customers_dataset.csv`

A partir delas, o autor constrói uma base com foco temporal e financeiro, onde cada pedido passa a ter:

- data de compra
- status válido para análise
- valor total do pedido, calculado como **preço + frete**

## Preparação e tratamento dos dados

A preparação do notebook é consistente com o objetivo temporal da análise:

- conversão de datas para formato adequado
- filtro para pedidos com status considerados válidos (`delivered`, `shipped`, `invoiced`, `processing`)
- agregação do valor financeiro por pedido
- criação de atributos como:
  - ano e mês
  - mês isolado
  - dia da semana
  - série temporal diária de faturamento

Esse tratamento é importante porque sazonalidade depende de um “relógio” limpo e confiável.

## Principais análises realizadas

### 1. Perfil financeiro do pedido
O notebook começa olhando a distribuição do valor dos pedidos e mostra que a maior parte deles está **abaixo de R$ 200**.

A interpretação sugerida é que o e-commerce analisado tem forte presença de compras de giro rápido, utilidades e itens de valor relativamente moderado.

### 2. Ritmo semanal das compras
Também é analisado o volume por dia da semana. O texto interpretativo aponta maior concentração de compras entre **segunda e quarta-feira**, com queda no fim de semana.

Isso é útil porque indica janelas mais promissoras para campanhas, comunicação e operação comercial.

### 3. Evolução temporal do faturamento
O notebook cria uma série temporal diária de faturamento entre janeiro de 2017 e agosto de 2018.  
A partir dela, faz uma **decomposição estatística aditiva**, separando a série em:

- dados observados
- tendência
- sazonalidade
- resíduos

Essa é uma das partes mais fortes do notebook, porque ajuda a distinguir:

- crescimento estrutural do negócio
- ciclos que se repetem
- choques fora do padrão

### 4. Identificação da Black Friday como evento fora da curva
Na leitura dos resíduos e da série observada, o autor destaca um pico muito forte no fim de 2017, interpretado como efeito de **Black Friday**.

Esse é um insight importante porque mostra que nem todo aumento de demanda é “rotina”; alguns eventos exigem preparação extraordinária.

### 5. Clusterização de meses por nível de demanda
O notebook usa **K-Means** para classificar os meses em três grupos:

- baixa demanda
- média demanda
- alta demanda

A lógica aqui é prática: em vez de tratar todos os meses como iguais, a empresa pode reconhecer perfis diferentes de operação e planejamento.

### 6. Relação entre pagamento e valor do pedido
Por fim, o notebook compara o valor do pedido com o tipo de pagamento.  
A interpretação apresentada é:

- **cartão de crédito** aparece mais ligado a compras de maior valor
- **boleto** se concentra mais em tickets médios ou baixos

Isso ajuda a conectar sazonalidade com comportamento financeiro do consumidor.

## Principais insights do notebook

1. **O negócio apresentava crescimento consistente entre 2017 e 2018.**  
   O notebook não mostra apenas picos isolados; ele identifica uma tendência ascendente de base.

2. **A Black Friday aparece como um choque positivo relevante.**  
   Não é só um mês bom; é um evento com comportamento muito acima do padrão normal.

3. **Existem meses claramente diferentes em termos de demanda.**  
   A clusterização reforça a ideia de que o planejamento operacional deve mudar conforme o período do ano.

4. **A rotina semanal de compra é mais forte no meio da semana.**  
   Isso pode orientar campanhas e calendário comercial.

5. **O tipo de pagamento ajuda a explicar o perfil das compras.**  
   Cartão tende a sustentar tickets mais altos, o que pode ser explorado em períodos de maior demanda.

## O que esse notebook agrega para o “grande resumo”

Este notebook é valioso porque traz uma visão de **tempo e planejamento**.  
Enquanto outros estudos olham para frete, regiões ou satisfação, aqui o foco está em:

- quando a demanda cresce
- quando ela cai
- quando a empresa precisa escalar operação
- em quais períodos faz sentido mudar estratégia de marketing e oferta

Ele ajuda a transformar o negócio em algo mais previsível.

## Recomendações práticas sugeridas no próprio notebook

Na conclusão, o autor sugere algumas ações bem claras:

- preparar logística e contratação temporária antes dos meses de alta demanda
- usar janeiro e fevereiro, historicamente mais fracos, para campanhas de estímulo
- monitorar sistemas e infraestrutura para suportar os picos
- explorar meios de pagamento e parcelamento em momentos de maior apetite de compra

## Limites e cuidados ao apresentar

O notebook é forte em leitura descritiva e planejamento temporal, mas não faz previsão formal de série temporal.  
Ou seja, ele ajuda muito a entender padrões e sazonalidade, mas não entrega um modelo preditivo de demanda futura com métricas de erro.

## Conclusão em linguagem simples

Se fosse para explicar este notebook para alguém de fora da área, eu diria:

> O estudo mostra que as vendas do e-commerce seguem ciclos bem definidos.  
> Há meses naturalmente mais fortes, meses mais fracos e eventos excepcionais, como a Black Friday.  
> Entender esses ciclos ajuda a empresa a planejar estoque, frete, marketing e equipe com muito mais inteligência.
