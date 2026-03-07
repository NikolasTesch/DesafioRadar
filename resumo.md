# Resumo Executivo: 10 Insights Estratégicos e Propostas de Machine Learning

Este documento consolida as principais descobertas analíticas extraídas dos notebooks do projeto **Desafio Radar/Olist** e apresenta soluções preditivas para otimização do negócio.

---

## 🚀 As 10 Principais Análises e Insights

### 1. Dominância Geográfica de SP
**Notebook:** `02_analise_regionalidade.ipynb`
**Gráfico Recomendado:** Gráfico de Barras (Ranking de Estados) ou Gráfico de Pizza.
**Insight Técnico:** São Paulo abriga mais de 60% dos lojistas ativos (Pareto 60/20 geográfico). Isso cria uma topologia de rede em "Estrela" onde o Sudeste é o único hub de exportação. Tecnicamente, isso resulta em um **Custo Inter-regional** que é, em média, 150% superior ao custo Intra-regional, penalizando a margem de contribuição em vendas fora do eixo Sul-Sudeste.

### 2. O "Doce Ponto" de Logística (Sudeste)
**Notebook:** `02_analise_regionalidade.ipynb`
**Gráfico Recomendado:** Gráfico de Dispersão (Scatter Plot) - Frete vs Tempo.
**Insight Técnico:** A análise de dispersão multivariada revela um cluster de alta densidade onde o frete mediano é de **R$ 15,00** e o tempo de entrega é de **~9.7 dias**. Fora deste cluster (Norte/Nordeste), a variância do tempo de entrega aumenta significativamente (desvio padrão elevado), tornando a promessa de entrega (SLA) estatisticamente instável.

### 3. Elasticidade do Abandono (Norte/Nordeste)
**Notebook:** `04_analise_categorias.ipynb`
**Gráfico Recomendado:** Boxplot (Distribuição de Ticket por Região).
**Insight Técnico:** Observa-se uma "seleção adversa" no funil de vendas geográfico. No Norte/Nordeste, o **Ticket Mediano salta de R$ 65 para R$ 90**. Isso ocorre porque o frete fixo alto (R$ 38+) atua como um filtro econômico, inviabilizando produtos de baixo valor unitário. O CAC (Custo de Aquisição) nessas regiões só se paga em itens com margem absoluta elevada ou cestas compostas (bundles).

### 4. Correlação Crítica: Atraso vs NPS
**Notebook:** `03_analise_satisfacao.ipynb`
**Gráfico Recomendado:** Gráfico de Linhas (NPS vs Dias de Atraso) ou Histograma de Notas.
**Insight Técnico:** Existe um **Ponto de Inflexão (Breaking Point)** na satisfação do cliente aos **20 dias**. Pedidos entregues abaixo de 10 dias mantêm um NPS de promotores (média 4.8 estrelas). Acima de 20 dias, a probabilidade de nota 1 aumenta para 80%, independentemente da categoria do produto, indicando que a logística é o driver primário de insatisfação em detrimento do produto em si.

### 5. O Paradoxo das Categorias
**Notebook:** `04_analise_categorias.ipynb`
**Gráfico Recomendado:** Gráfico de Barras Empilhadas (Proporção de Categorias por Região).
**Insight:** O gosto do brasileiro é homogêneo (Beleza, Cama/Mesa e Esportes lideram em todo lugar). O que muda é a viabilidade financeira de cada item devido à distância do estoque.

### 6. Logística de Mão Única
**Notebook:** `02_analise_regionalidade.ipynb`
**Gráfico Recomendado:** Heatmap de Origem x Destino ou Diagrama de Sankey.
**Insight:** Quase 80% das mercadorias cruzam fronteiras estaduais. O e-commerce não é uma rede capilarizada, mas um corredor de exportação do Sul/Sudeste para o restante do país.

### 7. Impacto do Frete Intra-regional
**Notebook:** `02_analise_regionalidade.ipynb`
**Gráfico Recomendado:** Gráfico de Barras Agrupadas (Frete Inter vs Intra Regional).
**Insight:** Quando o vendedor e o cliente estão no Nordeste, o frete cai de R$ 38 para R$ 15. A falta de lojistas locais é o maior "imposto" invisível da plataforma.

### 8. Concentração de Detratores
**Notebook:** `03_analise_satisfacao.ipynb`
**Gráfico Recomendado:** Mapa de Calor Coroplético (Distribuição de Notas 1-2 por UF).
**Insight Técnico:** O Norte apresenta uma taxa de detratores de **~20%**, contra **13.9%** no Sudeste. Esta diferença de 6 pontos percentuais é estatisticamente significante e está diretamente ligada à ineficiência do *Last-Mile* regional. Esse volume de feedback negativo gera um ciclo de degradação da marca que reduz drasticamente a taxa de retenção e recompra.

### 9. Sazonalidade de Stress (Black Friday)
**Notebook:** `4_Analise_Exploratoria_Olist.ipynb`
**Gráfico Recomendado:** Séries Temporais (Gráfico de Área ou Linha por Mês).
**Insight Técnico:** Durante picos sazonais, o volume de pedidos cresce em escala logarítmica, mas a capacidade logística responde de forma linear. Isso gera um **efeito chicote (Bullwhip Effect)** onde o tempo de entrega aumenta de forma desproporcional ao volume, estressando a operação de SAC e comprometendo o LTV dos clientes adquiridos durante o evento.

### 10. Eficiência de Pagamento
**Notebook:** `AnaliseParcelamento.ipynb`
**Gráfico Recomendado:** Treemap ou Gráfico de Barras (Taxa de Cancelamento por Método).
**Insight Técnico:** A análise de funil por método de pagamento revela que o Boleto Bancário possui a maior **taxa de vacância de estoque** (lead time entre reserva e confirmação). Implementar incentivos para PIX ou cartões de crédito pode reduzir o ciclo financeiro (Cash Conversion Cycle) e liberar o estoque para compradores de conversão imediata.

---

## 🤖 5 Propostas de Machine Learning

### 1. Modelo Preditivo de Churn de Carrinho (Logístico)
**Problema:** Alta taxa de abandono no Norte/Nordeste.
**Proposta:** Um modelo de classificação que, no momento em que o usuário insere o CEP, calcula a probabilidade de abandono com base no valor do frete/ticket. 
**Preparação de Dados:** Necessária. Precisaremos calcular a `razão_frete_produto` e criar uma variável alvo simulada (`churn_carrinho`) com base em pedidos iniciados vs finalizados, além de realizar a codificação (encoding) de regiões por faixa de CEP.
**Ação:** Se a probabilidade for alta, o sistema oferece um cupom de desconto no frete ou sugere um "Bundle" (kit) para diluir o custo logístico.

### 2. CLV (Customer Lifetime Value) Regionalizado
**Problema:** Marketing gastando igual em regiões com baixa fidelização.
**Proposta:** Regressão para estimar o valor futuro do cliente com base na sua primeira experiência de entrega.
**Preparação de Dados:** Necessária. Requer agregação histórica por `customer_unique_id`, cálculo de métricas RFM (Recência, Frequência e Valor) e cruzamento com a `média_atraso_entrega`. Será preciso tratar outliers de faturamento por cliente.
**Ação:** Priorizar investimentos de Ads (Google/Meta) em usuários com alta probabilidade de se tornarem recorrentes, evitando "clientes de uma compra só" que saíram frustrados com a logística.

### 3. Recomendação Estratégica de Cross-Selling por CEP
**Problema:** Frete alto para itens pequenos.
**Proposta:** Sistema de recomendação baseado em filtragem colaborativa, mas com restrição geográfica.
**Preparação de Dados:** Necessária. Precisaremos de uma matriz item-usuário e o cálculo de `peso_cubado_restante` (usando dimensões do produto que já temos no dataset) para sugerir itens que não aumentem a faixa de peso do frete atual.
**Ação:** Para clientes de longa distância, o algoritmo deve recomendar prioritariamente itens leves de alta margem que "cabem no mesmo frete", aumentando o ticket médio daquela remessa específica.

### 4. Detector de Anomalias em Trânsito (Fricção de SAC)
**Problema:** O cliente só reclama quando o atraso já é crítico.
**Proposta:** Modelo de detecção de anomalias que monitora o status de rastreamento em tempo real.
**Preparação de Dados:** Necessária. Precisamos criar uma "baseline" de tempo médio por rota específica (Origem-Destino). Os dados de `order_status_history` precisam ser transformados em séries temporais para identificar gargalos em hubs específicos.
**Ação:** Identificar automaticamente pedidos parados em hubs por mais de 48h e disparar um "SAC Preditivo" (alerta proativo ao cliente), reduzindo a probabilidade de Nota 1 na entrega.

### 5. Otimização de Mix de Estoque para CD Avançado
**Problema:** Onde abrir um novo Centro de Distribuição?
**Proposta:** Clusterização K-Means cruzada com análise de demanda latente.
**Preparação de Dados:** Já parcialmente tratada na EDA. Precisaremos apenas normalizar a densidade de pedidos por `coordenadas_geográficas` e calcular o `ganho_potencial_gmv` se o frete fosse reduzido em 50%, usando escalonamento (scaling) para o algoritmo de clusterização.
**Ação:** Identificar quais categorias teriam maior salto de volume se o frete fosse reduzido em 50%. Isso define não só *onde* abrir o CD, mas *quais* produtos (SKUs) devem ser movidos para lá primeiro.
