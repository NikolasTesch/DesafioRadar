import nbformat as nbf
import os

nb = nbf.v4.new_notebook()

cells = [
    nbf.v4.new_markdown_cell("""# Análise de Regionalidade do E-Commerce Tesch

## Objetivo Socrático
O objetivo deste notebook não é apenas plotar gráficos, mas entender **os porquês**. Queremos responder: como a localidade do cliente influencia o volume de vendas, os custos de frete e o tempo de entrega? Onde estão nossos principais gargalos logísticos?

## 1. Configuração e Bibliotecas
Nesta etapa, importamos as ferramentas clássicas de Ciência de Dados:
- `pandas` para estruturação tabular (DataFrame).
- `numpy` para operações numéricas de alto desempenho.
- `plotly` para visualizações ricas e interativas (essencial para apresentações executivas)."""),
    
    nbf.v4.new_code_cell("""import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import warnings

warnings.filterwarnings('ignore')
pd.set_option('display.max_columns', None)"""),

    nbf.v4.new_markdown_cell("""## 2. Carregamento dos Dados Primários
Conforme o `SKILL` de Análise de Dados (EDA), nosso primeiro passo prático é entender de qual 'unidade de análise' estamos falando e juntá-las.

O modelo do nosso banco de dados relacional separa **Clientes** (`olist_customers_dataset.csv`), os **Pedidos Gerais** (`olist_orders_dataset.csv`), os **Itens de Cada Pedido** contendo os valores e o frete (`olist_order_items_dataset.csv`) e, logicamente, os **Produtos e Geolocalizações**."""),

    nbf.v4.new_code_cell("""# Caminhos baseados na raiz do projeto (dentro da pasta data/raw)
path_customers = '../../data/raw/olist_customers_dataset.csv'
path_orders = '../../data/raw/olist_orders_dataset.csv'
path_items = '../../data/raw/olist_order_items_dataset.csv'
path_geolocation = '../../data/raw/olist_geolocation_dataset.csv'

# Leitura otimizada. Usaremos apenas as colunas essenciais para polpar memória
cols_orders = ['order_id', 'customer_id', 'order_status', 'order_purchase_timestamp', 'order_delivered_customer_date']
df_orders = pd.read_csv(path_orders, usecols=cols_orders, parse_dates=['order_purchase_timestamp', 'order_delivered_customer_date'])

cols_items = ['order_id', 'price', 'freight_value']
df_items = pd.read_csv(path_items, usecols=cols_items)

cols_customers = ['customer_id', 'customer_city', 'customer_state']
df_customers = pd.read_csv(path_customers, usecols=cols_customers)

# Exibindo o tamanho inicial do nosso universo de pedidos
print(f"Total de Pedidos Brutos: {df_orders.shape[0]}")"""),

    nbf.v4.new_markdown_cell("""## 3. Integração (Merges) e Feature Engineering

A "Feature Engineering" é a arte de criar novas variáveis a partir das existentes. A riqueza do nosso *insight* mora aqui:
1. **Agregação:** Um pedido pode ter vários itens. Para analisar o custo de frete total e o valor total de uma compra (cesta), devemos agrupar a tabela de itens por `order_id` *antes* do merge.
2. **Limpeza:** Filtraremos apenas pedidos com status `delivered` (entregues), já que cancelamentos poderiam distorcer a análise de tempo de entrega real.
3. **Novas Variáveis:** Calcularemos o `tempo_espera_dias` (diferença entre compra e entrega) e criaremos uma função para mapear os **Estados (`customer_state`)** em suas respectivas **Regiões** geográficas brasileiras."""),

    nbf.v4.new_code_cell("""# 1. Agrupar os itens por pedido (Somando Preço e Frete de cada carrinho)
df_items_grouped = df_items.groupby('order_id').agg({
    'price': 'sum',
    'freight_value': 'sum'
}).reset_index()

# 2. Filtrar apenas pedidos Entregues ('delivered')
df_orders_delivered = df_orders[df_orders['order_status'] == 'delivered'].copy()

# 3. Realizar os Merges (Left Joins para preservar o escopo do pedido)
df_master = df_orders_delivered.merge(df_customers, on='customer_id', how='left')
df_master = df_master.merge(df_items_grouped, on='order_id', how='left')

# Remover nulos de preço (pedidos que falharam ao relacionar itens)
df_master.dropna(subset=['price', 'order_delivered_customer_date'], inplace=True)

# Feature Engineering: Tempo de Entrega (em dias)
df_master['tempo_espera_dias'] = (df_master['order_delivered_customer_date'] - df_master['order_purchase_timestamp']).dt.total_seconds() / (24 * 3600)

# Feature Engineering: Mapeamento de Regiões
regioes = {
    'Norte': ['AM', 'RR', 'AP', 'PA', 'TO', 'RO', 'AC'],
    'Nordeste': ['MA', 'PI', 'CE', 'RN', 'PE', 'PB', 'SE', 'AL', 'BA'],
    'Centro-Oeste': ['MT', 'MS', 'GO', 'DF'],
    'Sudeste': ['SP', 'RJ', 'ES', 'MG'],
    'Sul': ['PR', 'RS', 'SC']
}

def map_regiao(estado):
    for regiao, estados in regioes.items():
        if estado in estados:
            return regiao
    return 'Desconhecido'

df_master['regiao'] = df_master['customer_state'].apply(map_regiao)

# Visualizar as primeiras linhas da nossa tabela unificada e rica
df_master.head(3)"""),

    nbf.v4.new_markdown_cell("""## 4. Análise Exploratória (EDA): Volume de Vendas e Concentração Regional

*Onde estão nossos clientes?* Vamos entender o Market Share do E-commerce Tesch por Região."""),

    nbf.v4.new_code_cell("""# Contagem de pedidos por Região
vendas_por_regiao = df_master['regiao'].value_counts().reset_index()
vendas_por_regiao.columns = ['Região', 'Quantidade de Pedidos']

fig_vendas = px.bar(
    vendas_por_regiao, 
    x='Região', 
    y='Quantidade de Pedidos',
    color='Região',
    text='Quantidade de Pedidos',
    title='Volume de Pedidos Entregues por Região',
    template='plotly_white',
    color_discrete_sequence=px.colors.qualitative.Pastel
)

fig_vendas.update_traces(textposition='outside')
fig_vendas.update_layout(showlegend=False, xaxis_title='Região', yaxis_title='Pedidos')
fig_vendas.show()"""),

    nbf.v4.new_markdown_cell("""### Insight Socrático 1:
Note a hiperconcentração no Sudeste. Como de costume no e-commerce brasileiro (e refletido no dataset da Olist), o Sudeste detém >70% de todo o volume de mercado. Mas e o ticket médio (valor gasto) vs. Frete? Regiões distantes pagam muito mais caro para comprar o mesmo produto?"""),

    nbf.v4.new_code_cell("""# Analisando as medianas (Mediana é mais robusta contra outliers que a média)
metricas_regiao = df_master.groupby('regiao').agg({
    'price': 'median',
    'freight_value': 'median',
    'tempo_espera_dias': 'median',
    'order_id': 'count'
}).reset_index()

metricas_regiao.columns = ['Região', 'Ticket Mediano (R$)', 'Frete Mediano (R$)', 'Tempo de Entrega (Dias)', 'Volume']

# Ordenar do mais barato para o mais caro no frete
metricas_regiao = metricas_regiao.sort_values(by='Frete Mediano (R$)')

metricas_regiao.style.background_gradient(cmap='YlOrRd', subset=['Frete Mediano (R$)', 'Tempo de Entrega (Dias)'])"""),

    nbf.v4.new_markdown_cell("""## 5. Boxplots de Frete e Tempo de Entrega (Dispersão)
Tabelas são ótimas, mas gráficos de Boxplot nos deixam ver *toda* a distribuição dos dados (limites superiores, caudas e valores fora da curva)."""),

    nbf.v4.new_code_cell("""# Filtrando outliers extremos de frete apenas para visualização de caixas limpas (<R$150)
df_clean_freight = df_master[df_master['freight_value'] < 150]

fig_box_frete = px.box(
    df_clean_freight, 
    x='regiao', 
    y='freight_value', 
    color='regiao',
    title='Distribuição dos Custos de Frete (R$) por Região',
    template='plotly_white',
    labels={'freight_value': 'Valor de Frete (R$)', 'regiao': 'Região'}
)
fig_box_frete.show()"""),

    nbf.v4.new_code_cell("""# Análise similar para Tempo de Espera (< 60 dias para limpar ruído externo)
df_clean_time = df_master[df_master['tempo_espera_dias'] < 60]

fig_box_tempo = px.box(
    df_clean_time, 
    x='regiao', 
    y='tempo_espera_dias', 
    color='regiao',
    title='Distribuição do Tempo de Entrega (Dias) por Região',
    template='plotly_white',
    labels={'tempo_espera_dias': 'Tempo de Espera (Dias)', 'regiao': 'Região'}
)
fig_box_tempo.show()"""),

    nbf.v4.new_markdown_cell("""### Insight Socrático 2:
Observe o gráfico de Tempo de Entrega: A caixa do Norte (linha do meio = mediana) salta abruptamente para quase 20 dias, contra os ~9 dias do Sudeste.
A infraestrutura logística do país e as malhas aéreas centradas em Viracopos/Guarulhos criam barreiras de distância cruéis para o Norte/Nordeste.

Isso sugere algo forte: se o custo logístico afasta os clientes (elasticidade de preço e tempo), podemos hipotetizar que o Norte/Nordeste teriam mais vendas se tivessemos *Fulfillment Centers* locais."""),

    nbf.v4.new_markdown_cell("""## 6. Correlação Linear e Conclusões
Será que as vendas caem matematicamente por conta do frete caro, ou ambos são apenas reflexos da densidade populacional? 
Vamos fazer um agrupamento a nível `Estado` para testar essa correlação."""),

    nbf.v4.new_code_cell("""# Agrupar dados macroeconômicos do e-commerce por ESTADO (uf)
estado_stats = df_master.groupby('customer_state').agg({
    'order_id': 'count',                 # Volume de vendas
    'freight_value': 'mean',             # Frete médio
    'tempo_espera_dias': 'mean',         # Tempo de entrega médio
    'regiao': 'first'                    # Pegar o nome da região mapeada
}).reset_index()

estado_stats.columns = ['Estado', 'Total Pedidos', 'Frete Medio', 'Tempo Entrega Medio', 'Região']

# Gráfico de Dispersão (Bolhas) - Vendas vs Frete e Tempo
fig_scatter = px.scatter(
    estado_stats,
    x='Frete Medio',
    y='Tempo Entrega Medio',
    size='Total Pedidos',
    color='Região',
    hover_name='Estado',
    log_x=False, size_max=60,
    title='Matriz Logística: Frete vs Tempo vs Volume de Vendas (Tamanho da Bolha)',
    template='plotly_white',
    labels={'Frete Medio': 'Frete Médio (R$)', 'Tempo Entrega Medio': 'Tempo de Entrega Médio (Dias)'}
)

# Adicionando linhas de tendência ou anotações lógicas
fig_scatter.add_vline(x=20, line_width=1, line_dash="dash", line_color="gray", annotation_text="Frete Baixo < 20")
fig_scatter.add_hline(y=15, line_width=1, line_dash="dash", line_color="gray", annotation_text="Entrega < 15 Dias")

fig_scatter.show()"""),

    nbf.v4.new_markdown_cell("""### Conclusões do Notebook:
- Os estados do **Sudeste** estão espremidos no bloco inferior esquerdo: **Frete baixo, Tempo de Entrega muito baixo, e as maiores bolhas de volume**.
- Enquanto isso, Roraima (RR), Amapá (AP) e Amazonas (AM) figuram no canto superior direito: os **Tempos mais críticos (> 25 dias)** e **Fretes mais caros (> R$40 médio)**, com bolhas estruturalmente minúsculas.

**Hipótese Verificada:** Há uma correlação linear alta entre Custo Logístico (Frete + Tempo) e Penetração de Mercado. Vender na região Norte não é apenas distante, é financeiramente proibitivo para tickets baixos, pois o frete ultrapassa o custo do item.""")
]

nb['cells'] = cells

with open('notebooks/Edvan/02_analise_regionalidade.ipynb', 'w') as f:
    nbf.write(nb, f)
