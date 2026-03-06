# Relatório Executivo: Regionalidade Custo-Logística

**Data:** Março de 2026  
**Objetivo:** Analisar os impactos da regionalidade nos custos de frete, no tempo de entrega e, consequentemente, no volume de vendas do modelo de negócio (base Olist/Desafio Radar).

---

## 1. Dados Trabalhados e Metodologia

Para realizar essa Análise Exploratória de Dados (EDA), partimos da base primária do banco relacional do e-commerce.

**Dataset e Merges:**
1. **Pedidos (`olist_orders_dataset.csv`):** Filtramos nossa base apenas para pedidos com o status final `delivered` (entregues), evitando que carrinhos abandonados ou cancelados desvirtuassem a análise logística real.
2. **Geografia do Cliente (`olist_customers_dataset.csv`):** Através do CPF (`customer_id`), trouxemos os estados de origem (`customer_state`) e implementamos nossa primeira grande *Feature Engineering*: o mapeamento dos 27 Estados nas **5 Regiões do Brasil**.
3. **Valores Logísticos (`olist_order_items_dataset.csv`):** Agrupamos (soma) os itens por pedido antes da junção (Merge), garantindo que capturamos o valor real pago pelo cliente e o valor bruto do frete por "cesta", e não apenas por produto individual.

**Métricas Geradas (Feature Engineering):**
- Criamos a variável contínua `tempo_espera_dias` extraindo a diferença, em dias, entre o momento em que a compra ocorreu (`order_purchase_timestamp`) e a entrega ao destinatário (`order_delivered_customer_date`).

---

## 2. Passo a Passo Analítico (Notebook Socrático)

Como mentorado via Engenharia de Dados, nosso processo não foi apenas plotar dados aleatórios, mas validar hipóteses progressivamente:

1. **Univariada (Distribuição):** Primeiro checamos a quantidade de vendas brutas por Região usando gráficos de barras modulares. O Sudeste detém > 70% da massa de vendas totais.
2. **Medianas de Ticket vs Frete:** Através de *DataFrames* ranqueados percebemos que um Morador de Roraima (RR) paga medianamente valores exorbitantes de frete, muitas vezes ultrapassando o valor do próprio ticket do produto.
3. **Dispersão por Boxplots:** Plotamos a métrica cruzando *Regiões vs Custos de Frete (<R$ 150 para limpeza)* e *Regiões vs Tempos de Entrega (< 60 dias)*. Os "Limites Superiores" estatísticos das caixas confirmam estruturalmente a barreira logística das pontas do país.
4. **Agrupamento e Correlação de Dispersão (Bolhas):** Criamos uma Matriz Logística plotada em *Scatter* pelo Estado. Essa visualização multivariada permitiu comparar, num único gráfico: O Frete (Eixo X), O Tempo de Entrega (Eixo Y), a Região (Cor) e a Penetração / Volume de Vendas (Tamanho da Bolha).

---

## 3. Insights Técnicos e Correlações

* **Elasticidade da Distância:** Existe uma forte correlação linear verificada. O eixo inferior esquerdo do nosso gráfico Logístico abriga todas as grandes "bolhas" do e-commerce (Estados do Sudeste). Elas configuram o "Sweet Spot": Fretes abaixo de R\$20 e entregas em média de ~9 dias.
* **Barreira do Centro-Oeste/Nordeste:** Essas regiões ficam no "meio do caminho", com tempos de entrega oscilando em torno de ~15 dias e fretes superando confortavelmente a faixa de R$ 30, desestimulando vendas de Ticket Médio Baixo (Bugigangas, acessórios baratos).
* **Zona de Sacrifício Norte:** Extremos como Roraima e Amapá mostram médias de frete que ultrapassam a margem elástica do consumidor (Fretes > R$40 e entregas > 25 dias). Suas bolhas de vendas são estatisticamente insignificantes quando mapeadas via base Olist.

---

## 4. A Raiz do Problema: Concentração de Fornecimento (Rota Origem x Destino)
Para comprovar que a densidade demográfica ou a distância rodoviária não explicam sozinhas a disparidade, cruzamos a base de Clientes com a de Vendedores (`olist_sellers_dataset.csv`):

1. **Monopólio Geográfico de Venda:** Pelo gráfico de Pareto gerado na Parte 2 da nossa Análise Estrutural, **o Estado de São Paulo (SP) abriga literalmente mais de 60% de todos os lojistas ativos** na plataforma, seguido de longe por MG e PR. 
2. **Matriz de Fluxo Lógico (Exportação):** Usando uma Tabela Dinâmica Heatmap, provou-se que a logística do E-commerce não é uma teia, e sim uma **Avenida de Mão Única**. Quase todas as mercadorias consumidas no Norte, Nordeste e Centro-Oeste estão cruzando divisas de Estado, originando-se do Sul e Sudeste.
3. **Métrica Custo Intra vs Inter Regional:** 

- Se um cliente Nordestino tiver a sorte de encontrar um produto cujo vendedor também seja do Nordeste (Frete Intra-Regional), o frete médio cai drasticamente para cerca de **R$ 15,00**.
- O grande problema é que, devido ao déficit de vendedores cadastrados na plataforma e alocados naquela região, o cliente é engolido pela exportação (Frete Inter-Regional do Sudeste p/ Nordeste), elevando violentamente a média de frete para **R$ 38,00**.

---

## 5. Validação Cruzada (Contexto Externo)

Nossas conclusões baseadas em banco de dados podem ser perenemente validadas pela malha rodoviária e matriz de carga brasileira:
1. **Hubs Produtores no Eixo SP-MG-SC:** Mais de 60% da indústria de transformação do Brasil se concentra aqui. E-commerces que não pulverizam seus depósitos forçam o produto a viajar milhares de quilômetros de caminhão (a malha aérea é restritiva para baixo ticket). 
2. A baixa **Densidade Populacional** do Sistema Norte e interior do Centro-Oeste encarece fortemente a logística chamada *Last-Mile* ("a última milha"). Transportadoras não conseguem fechar o peso cúbico de um caminhão inteiro com destino a uma cidade ribeirinha com facilidade, encarecendo brutalmente a tarifa e o Custo Brasil repassado ao consumidor, que acaba optando pelo varejo local.

---

## 6. Desafios, Soluções e Propostas de Valor

### Desafio
A hiperconcentração de faturamento do e-commerce na região Sudeste indica um funil de conversão que está vazando pesadamente no topo no Norte e Nordeste devido ao Custo do Frete e Tempo, o que chamamos de *Abandono de Carrinho induzido por Logística*.

### Propostas de Soluções Arquiteturais / Físicas

- **Centro de Distribuição Avançado (Fulfillment Centers):** O dado grita por Hubs Logísticos descentralizados localizados estrategicamente nos portais do Nordeste (ex: Recife/PE ou Salvador/BA). Armazenar o estoque "Best-Seller" nesses pontos reduz o Custo de Frete (R$/Km) e corta a espera pela metade, alavancando massivamente a bolha de volume dessas regiões.
- **Intenção de Compra por Ticket Composto:** Para produtos que ainda exigem saída via Hub Sudeste com direção ao Norte/Nordeste, nosso site deve induzir o *Cross-Selling*. Se o algoritmo front-end notar que o CEP de entrega é Norte, de forma agressiva deverá sugerir produtos pequenos e de alta margem (ex: película protetora se ele comprou cabo USB) para inflacionar o Ticket e o Custo Composto do frete tornar-se atrativo, criando Campanhas de Desconto de Frete em compras acima de "R$X" reais fixado dinamicamente por CEP de destino.
- **🚨 Recrutamento de Parceiros Regionais (Subsidio):** Comprovado o peso da barreira Origem-Destino, o setor Comercial da plataforma deve mapear polos atacarejos no Nordeste (Ex: Polo de Confecção do Agreste Pernambucano) e oferecer carência na taxa da plataforma (zero comissão) pelos 6 primeiros meses para esses lojistas se cadastrarem. Lojista ativo no Nordeste = Venda garantida e rápida pro público de lá.
