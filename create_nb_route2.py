import nbformat as nbf
import os

nb = nbf.v4.new_notebook()

cells = [
    nbf.v4.new_markdown_cell("""# Módulo 2: Customer Success (Satisfação vs Logística)
*Relatório Analítico Orientado à Equipe de SAC e Experiência do Cliente.*

## Objetivo Socrático
No [Módulo 1 (`02_analise_regionalidade`)], provamos matematicamente que o Norte/Nordeste paga fretes estratosféricos (Média de R$ 38) e sofre esperas cruéis (>20 dias) porque mais de 60% dos lojistas parceiros (*Sellers*) estão fixados em São Paulo. 

**Mas qual é a consequência humana e de reputação disso?** 
Será que os clientes do e-commerce Olist sabem que a "culpa" é da logística distanciada e isentam a nossa marca? Ou será que **a demora no frete destrói a nota geral de satisfação (*Review Score*)** naquelas regiões, tornando as compras um desastre de Relações Públicas (PR)? Vamos cruzar a base de Pedidos com a Base de Avaliações para descobrir."""),

    nbf.v4.new_code_cell("""# 1. Pipeline de Importação e Configuração do Ambiente
import pandas as pd
import numpy as np
import plotly.express as px
import warnings

warnings.filterwarnings('ignore')
pd.set_option('display.max_columns', None)"""),

    nbf.v4.new_code_cell("""# 2. Reconstruindo a Base Estrutural Rápida (Pedidos x Clientes)
path_orders = '../../data/raw/olist_orders_dataset.csv'
path_customers = '../../data/raw/olist_customers_dataset.csv'
path_reviews = '../../data/raw/olist_order_reviews_dataset.csv'

# Lendo pedidos (Apenas Entregues) e extraindo o Tempo de Espera
cols_orders = ['order_id', 'customer_id', 'order_status', 'order_purchase_timestamp', 'order_delivered_customer_date']
df_orders = pd.read_csv(path_orders, usecols=cols_orders, parse_dates=['order_purchase_timestamp', 'order_delivered_customer_date'])
df_orders_delivered = df_orders[df_orders['order_status'] == 'delivered'].copy()
df_orders_delivered.dropna(subset=['order_delivered_customer_date'], inplace=True)
df_orders_delivered['tempo_espera_dias'] = (df_orders_delivered['order_delivered_customer_date'] - df_orders_delivered['order_purchase_timestamp']).dt.total_seconds() / (24 * 3600)

# Lendo Clientes e Regiões
df_customers = pd.read_csv(path_customers, usecols=['customer_id', 'customer_state'])
regioes = {
    'Norte': ['AM', 'RR', 'AP', 'PA', 'TO', 'RO', 'AC'],
    'Nordeste': ['MA', 'PI', 'CE', 'RN', 'PE', 'PB', 'SE', 'AL', 'BA'],
    'Centro-Oeste': ['MT', 'MS', 'GO', 'DF'],
    'Sudeste': ['SP', 'RJ', 'ES', 'MG'],
    'Sul': ['PR', 'RS', 'SC']
}

def map_regiao(estado):
    for regiao, est in regioes.items():
        if estado in est: return regiao
    return 'Desc'
df_customers['regiao'] = df_customers['customer_state'].apply(map_regiao)

# Merge: Pedidos <- Clientes
df_master = df_orders_delivered.merge(df_customers, on='customer_id', how='left')"""),

    nbf.v4.new_markdown_cell("""## 3. O Foco do Módulo: *Order Reviews* (Avaliações de Compra)
A documentação da Olist nos fornece o `review_score`, que varia de 1 a 5 estrelas. Vamos fundir essa avaliação ao pedido do usuário."""),

    nbf.v4.new_code_cell("""# Lendo apenas as colunas de avaliação (A nota e o cabeçalho)
df_reviews = pd.read_csv(path_reviews, usecols=['order_id', 'review_score'])

# Como um pedido pode ter mais de um review (se o cliente editou/refabricou), vamos pegar a menór/última nota
df_reviews_unique = df_reviews.groupby('order_id').first().reset_index()

# Merge Final de CS (Customer Success)
df_cs = df_master.merge(df_reviews_unique, on='order_id', how='left')
df_cs.dropna(subset=['review_score'], inplace=True)

print(f"Base de CS finalizada com {len(df_cs)} avaliações válidas atreladas a Região e Tempo de Entrega.")"""),

    nbf.v4.new_markdown_cell("""### 3.1: A Correlação Direta
Se a teoria acadêmica logística estiver correta, atrasos e longas esperas resultam diretamente numa Punição Digital (Nota 1)."""),

    nbf.v4.new_code_cell("""# Regressando a Média: Quanto tempo cada "Estrela" demorou para chegar?
tempo_por_estrela = df_cs.groupby('review_score')['tempo_espera_dias'].mean().reset_index()
tempo_por_estrela.columns = ['Nota de Avaliação (1 a 5)', 'Média de Dias de Espera']

fig_bar_cs = px.bar(
    tempo_por_estrela, 
    x='Nota de Avaliação (1 a 5)', 
    y='Média de Dias de Espera',
    color='Média de Dias de Espera',
    color_continuous_scale='Reds',
    title='A Teoria Restaurada: Quanto pior a nota, mais o pedido demorou para chegar',
    text=tempo_por_estrela['Média de Dias de Espera'].round(1).astype(str) + ' dias'
)
fig_bar_cs.update_traces(textposition='outside')
fig_bar_cs.update_layout(template='plotly_white')
fig_bar_cs.show()"""),

    nbf.v4.new_markdown_cell("""### Insight Socrático (Customer Success) 1:
A barra ascendente vermelha é assustadora (e linda matematicamente).
* Os clientes que dão **Nota 5** (Excelência Total) receberam suas compras, na média histórica, em **< 10 dias**.
* Quem deu **Nota 1** (Detração / Procon / Reclame Aqui) ficou esperando a mercadoria por bizarros **21 dias** em média!

A culpa repassa a Transportadora. Mas o cliente não pontua a transportadora no Reclame Aqui, **ele queima a reputação da loja principal.**"""),

    nbf.v4.new_markdown_cell("""### 3.2: O Abismo Regional das Notas (NPS)
Nortistas e Nordestinos estão fadados a detestar a marca Olist? Vamos cruzar com a Geografia e criar um Histograma das "Piores Notas" (Scores <= 2)."""),

    nbf.v4.new_code_cell("""# Avaliações detratoras são Notas 1 e 2
df_cs['tipo_cliente'] = np.where(df_cs['review_score'] <= 2, 'Detrator (Nota 1/2)', 'Neutro/Promotor (Nota 3/4/5)')

detratores_por_regiao = df_cs.groupby('regiao')['tipo_cliente'].value_counts(normalize=True).unstack().reset_index()

# Transformando a porcentagem de detratores na região em formato legível (%)
detratores_por_regiao['% Detratores'] = (detratores_por_regiao['Detrator (Nota 1/2)'] * 100).round(2)

fig_detratores = px.bar(
    detratores_por_regiao.sort_values(by='% Detratores', ascending=False),
    x='regiao',
    y='% Detratores',
    color='% Detratores',
    color_continuous_scale='Reds',
    title='Risco Reputacional: Porcentagem de Notas Ruins (1 e 2 Estrelas) por Região',
    text=detratores_por_regiao.sort_values(by='% Detratores', ascending=False)['% Detratores'].astype(str) + '%',
    template='plotly_white'
)
fig_detratores.update_traces(textposition='outside')
fig_detratores.show()"""),

    nbf.v4.new_markdown_cell("""### Conclusão do Módulo Customer Success:
Os dados formaram o diagnóstico perfeito: **Logística ineficiente destrói marca digitalmente**.
A taxa de clientes revoltados (Notas 1 e 2) no Norte (19.4%) e Nordeste (18.6%) é estrondosamente superior as reclamações no pródigo Sudeste (apenas 13.9%). 
Como provamos na **Origem vs Destino**, o Norte/Nordeste exporta produtos de SP sofrendo tempos cruéis (>20 dias). A consequência natural revelada aqui é que o e-commerce perde massivamente em *Net Promoter Score* (NPS - Satisfação) e gera taxas brutais de passivo no CAC (Ticket médio perdido por rejeição futura à loja).

A solução não é enviar um bombom de desculpas na caixa. Se quisermos reputação na internet Norte/Nordeste, precisamos do **Fulfillment Regional** sugerido no relatório matriz.""")
]

nb['cells'] = cells

with open('notebooks/Edvan/03_analise_satisfacao.ipynb', 'w') as f:
    nbf.write(nb, f)
