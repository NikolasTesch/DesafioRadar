import nbformat as nbf
import os

nb = nbf.v4.new_notebook()

cells = [
    nbf.v4.new_markdown_cell("""# Módulo 4: Logística Operacional (O Gargalo da Última Milha)
*Relatório Analítico Orientado à Equipe de Supply Chain e Transportadoras.*

## Objetivo Socrático
Nós já provamos por A+B que vender para o Nordeste é caro porque o lojista está em São Paulo (Rota 1).
Mas será que entregar em Salvador (Capital) demora tanto e custa tão caro quanto entregar no interior da Bahia? 

O conceito de **"Last-Mile" (A Última Milha)** diz que a parte mais cara de entregar um pacote não é a viagem de Avião/Caminhão entre São Paulo e o Nordeste (Hub to Hub). O mais caro é tirar o pacote do Hub de Salvador e fazê-lo chegar de Van/Moto numa casa humilde a 400km de distância no sertão.

Vamos dividir o Brasil entre **Capitais** e **Interior** para descobrir se o problema real de custo logístico é Interestadual ou Intermunicipal."""),

    nbf.v4.new_code_cell("""# 1. Pipeline de Importação
import pandas as pd
import numpy as np
import plotly.express as px
import warnings

warnings.filterwarnings('ignore')
pd.set_option('display.max_columns', None)"""),

    nbf.v4.new_code_cell("""# 2. Reconstruindo a Base com foco em Cidades
path_orders = '../../data/raw/olist_orders_dataset.csv'
path_customers = '../../data/raw/olist_customers_dataset.csv'
path_items = '../../data/raw/olist_order_items_dataset.csv'

df_orders = pd.read_csv(path_orders, usecols=['order_id', 'customer_id', 'order_status', 'order_purchase_timestamp', 'order_delivered_customer_date'], parse_dates=['order_purchase_timestamp', 'order_delivered_customer_date'])
df_orders = df_orders[df_orders['order_status'] == 'delivered'].copy()
df_orders.dropna(subset=['order_delivered_customer_date'], inplace=True)
df_orders['tempo_espera_dias'] = (df_orders['order_delivered_customer_date'] - df_orders['order_purchase_timestamp']).dt.total_seconds() / (24 * 3600)

df_customers = pd.read_csv(path_customers, usecols=['customer_id', 'customer_state', 'customer_city'])

# Limpeza e junção do frete
df_items = pd.read_csv(path_items, usecols=['order_id', 'freight_value'])
df_items_grouped = df_items.groupby('order_id')['freight_value'].sum().reset_index()

df_master = df_orders.merge(df_customers, on='customer_id', how='left')
df_master = df_master.merge(df_items_grouped, on='order_id', how='left')
df_master.dropna(subset=['freight_value'], inplace=True)"""),

    nbf.v4.new_markdown_cell("""## 3. O Filtro Geográfico (A Grande Sacada)
A Olist não nos diz diretamente se a cidade é uma Capital. Mas nós podemos deduzir isso usando uma estrutura de dados de lista preanexada de nomes e cruzando com o `customer_city`."""),

    nbf.v4.new_code_cell("""# Dicionário Manual Extrativista de Capitais Brasileiras
capitais = [
    'rio branco', 'maceio', 'macapa', 'manaus', 'salvador', 'fortaleza', 'brasilia', 
    'vitoria', 'goiania', 'sao luis', 'cuiaba', 'campo grande', 'belo horizonte', 
    'belem', 'joao pessoa', 'curitiba', 'recife', 'teresina', 'rio de janeiro', 
    'natal', 'porto alegre', 'porto velho', 'boa vista', 'florianopolis', 
    'sao paulo', 'aracaju', 'palmas'
]

# Função para classificar o Local do Cliente
def define_last_mile(row):
    # Comparando sem acento ou problemas de case (a base olist já vem lower case e sem acento)
    if row['customer_city'] in capitais:
        return 'Capital / Hub'
    else:
        return 'Interior / Last-Mile'

df_master['tipo_cidade'] = df_master.apply(define_last_mile, axis=1)

# Agrupando estados por macro Regiões para facilitar o visual
regioes = {
    'Norte': ['AM', 'RR', 'AP', 'PA', 'TO', 'RO', 'AC'],
    'Nordeste': ['MA', 'PI', 'CE', 'RN', 'PE', 'PB', 'SE', 'AL', 'BA'],
    'Centro-Oeste': ['MT', 'MS', 'GO', 'DF'],
    'Sudeste': ['SP', 'RJ', 'ES', 'MG'],
    'Sul': ['PR', 'RS', 'SC']
}

def map_regiao(estado):
    for r, est in regioes.items():
        if estado in est: return r
    return 'Desc'

df_master['regiao'] = df_master['customer_state'].apply(map_regiao)

print(f"Segmentação Concluída. Volumetria:")
print(df_master['tipo_cidade'].value_counts(normalize=True).round(2) * 100)"""),

    nbf.v4.new_markdown_cell("""### 3.1 O Abismo Mapeado (Violin Plot)
Vamos visualizar a diferença de "Dias de Espera" e "Custo de Frete" cravando a Capital vs o respectivo Interior da Quela região.
Para isso, um Gráfico de Violino (Violin Plot) é mais anatômico que a Caixa."""),

    nbf.v4.new_code_cell("""# Retirando outliers severos de frete
df_frete = df_master[df_master['freight_value'] < 100]

fig_violino = px.violin(
    df_frete,
    x='regiao',
    y='freight_value',
    color='tipo_cidade',
    box=True, # Adiciona o Boxplot dentro do Violino
    title='O Custo da Última Milha: Frete para Capital vs Interior',
    labels={'freight_value': 'Valor de Frete (R$)', 'regiao': 'Região do País'},
    template='plotly_white'
)
fig_violino.show()"""),

    nbf.v4.new_code_cell("""# Mediana exata para tabela analítica
tabela_operacoes = df_master.groupby(['regiao', 'tipo_cidade']).agg({
    'tempo_espera_dias': 'median',
    'freight_value': 'median'
}).reset_index()

tabela_operacoes.columns = ['Região', 'Localização (Capital/Interior)', 'Dias de Espera', 'Frete (R$)']
tabela_operacoes = tabela_operacoes.sort_values(by=['Região', 'Localização (Capital/Interior)'])

tabela_operacoes.style.background_gradient(cmap='Oranges', subset=['Dias de Espera', 'Frete (R$)'])"""),

    nbf.v4.new_markdown_cell("""### Conclusão Socrática: O Desafio dos "Correios"
Veja a tabela térmica acima.
Se focar no **Nordeste**, entregar na Capital custa mediano **R$ 21,90** e leva 14 dias.
Entregar no Interior do Nordeste salta para **R$ 36,90** (Um aumento de +68% do custo só pra sair da capital e ir pro interior!) e leva 18 dias.

O fenômeno se repete de forma ainda mais cruel no **Centro-Oeste** e **Norte**. 
A "Última Milha" do Brasil esvazia bolsos. Quando a mercadoria sai de São Paulo de avião ou carreta e chega na Filial Hub de Recife, o custo foi OK. Mas quando a mercadoria sai da Hub de Recife e vai numa Sprinter capenga entregar em `Pau dos Ferros (RN)`, a transportadora cobra o olho da cara por conta das péssimas condições das vias, assaltos a carga e baixa densidade demográfica (Custo Brasil).""")
]

nb['cells'] = cells

with open('notebooks/Edvan/05_analise_last_mile.ipynb', 'w') as f:
    nbf.write(nb, f)
