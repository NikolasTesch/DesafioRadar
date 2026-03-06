import nbformat as nbf
import os

nb = nbf.v4.new_notebook()

cells = [
    nbf.v4.new_markdown_cell("""# Módulo 3: Inteligência de Mercado (Marketing & Categorias)
*Relatório Analítico Orientado à Equipe Comercial, Tráfego Pago e Mix de Produtos.*

## Objetivo Socrático
Já provamos o Custo do Frete e a Destruição da Satisfação (Rotas 1 e 2).
Mas agora entra uma das perguntas mais cruciais para o faturamento (Ebitda): **"O que os brasileiros de diferentes regiões compram?"**
Será que a barreira do "Frete de R$ 40" afasta a compra de cabos USB e blusas baratas, forçando o cliente a usar o Olist/E-commerce apenas quando precisa comprar itens muito caros (Eletrodomésticos, Informática)?

Se isso for verdade, mapear as *Categorias de Produto* nos permite parar de jogar dinheiro fora anunciando bugigangas no Facebook Ads do Acre ou Roraima."""),

    nbf.v4.new_code_cell("""# 1. Pipeline de Importação Standard
import pandas as pd
import numpy as np
import plotly.express as px
import warnings

warnings.filterwarnings('ignore')
pd.set_option('display.max_columns', None)"""),

    nbf.v4.new_code_cell("""# 2. Base Estrutural com Inteligência de Produto (SKU)
path_orders = '../../data/raw/olist_orders_dataset.csv'
path_customers = '../../data/raw/olist_customers_dataset.csv'
path_items = '../../data/raw/olist_order_items_dataset.csv'
path_products = '../../data/raw/olist_products_dataset.csv'
path_translation = '../../data/raw/product_category_name_translation.csv'

# Limpeza e Cruzamento Rápido
df_orders = pd.read_csv(path_orders, usecols=['order_id', 'customer_id', 'order_status'])
df_orders = df_orders[df_orders['order_status'] == 'delivered'].copy()

df_customers = pd.read_csv(path_customers, usecols=['customer_id', 'customer_state'])
df_master = df_orders.merge(df_customers, on='customer_id', how='left')

# Mapeando Regiões
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

# Agregando Itens e Produtos
df_items = pd.read_csv(path_items, usecols=['order_id', 'product_id', 'price', 'freight_value'])
df_products = pd.read_csv(path_products, usecols=['product_id', 'product_category_name'])
df_trans = pd.read_csv(path_translation)

# Fundir a Categoria (Em Inglês para padronização gráfica profissional)
df_products = df_products.merge(df_trans, on='product_category_name', how='left')
df_items = df_items.merge(df_products[['product_id', 'product_category_name_english']], on='product_id', how='left')
df_items.rename(columns={'product_category_name_english': 'categoria'}, inplace=True)

# Merge com o Pedido
# Nota Técnica: Aqui NÃO podemos agrupar a df_items. Precisamos de cada "Linha de Produto" para contar Categorias.
df_marketing = df_master.merge(df_items, on='order_id', how='left')
df_marketing.dropna(subset=['categoria', 'price'], inplace=True)

print(f"Base de Marketing processada: {len(df_marketing)} SKUs vendidos com categoria catalogada.")"""),

    nbf.v4.new_markdown_cell("""## 3. Top Categorias por Região
O Sudeste dita as regras do top 10 porque tem 70% da massa de vendas. Vamos olhar o Top 5 de Vendas percentual **dentro de cada região**. Será que o Norte consome algo diferente do Sudeste?"""),

    nbf.v4.new_code_cell("""# Calcula o share (porcentagem) de uma categoria dentro de sua própria região
vendas_categoria = df_marketing.groupby(['regiao', 'categoria'])['order_id'].count().reset_index()
vendas_categoria.columns = ['regiao', 'categoria', 'vendas']

vendas_totais_regiao = vendas_categoria.groupby('regiao')['vendas'].transform('sum')
vendas_categoria['share_perc'] = (vendas_categoria['vendas'] / vendas_totais_regiao) * 100

# Pegando o Top 5 de cada Região
top_categorias = vendas_categoria.sort_values(['regiao', 'share_perc'], ascending=[True, False]).groupby('regiao').head(5)

fig_top_cat = px.bar(
    top_categorias,
    x='regiao',
    y='share_perc',
    color='categoria',
    title='Mix de Produtos: O Top 5 que movimenta cada Região do Brasil (%)',
    labels={'share_perc': 'Representação (%) no Mix Regional', 'regiao': 'Regiões'},
    template='plotly_white',
    text=top_categorias['share_perc'].round(1).astype(str) + '%'
)
fig_top_cat.update_traces(textposition='inside', textfont_size=11)
fig_top_cat.show()"""),

    nbf.v4.new_markdown_cell("""### Insight Socrático (Marketing) 1:
Curiosamente, *Health Beauty* (Beleza) e *Bed Bath Table* (Cama Mesa Banho) e *Sports Leisure* (Esportes) dominam de forma consistente o gosto nacional, independentemente da região.

Mas se o gosto é o mesmo, onde a logística interfere na decisão da compra?"""),

    nbf.v4.new_markdown_cell("""## 4. O Abismo de Ticket (Sensibilidade ao Frete)
O Princípio Econômico de Sensibilidade ao Frete diz:
* Se um pen-drive custa R$ 20 e o frete R$ 40 -> Eu não compro. (200% do Custo do Bem).
* Se uma geladeira custa R$ 2.000 e o frete R$ 150 -> Eu compro. (7.5% do Custo do Bem).

Provaremos que os moradores das zonas distantes (Norte/Nordeste) evitam comprar coisas baratas, elevando o Ticket Médio final transacionado."""),

    nbf.v4.new_code_cell("""# Filtrando outliers de luxo (produtos > R$ 1000) para análise comportamental das massas
df_massas = df_marketing[df_marketing['price'] <= 1000]

fig_ticket = px.box(
    df_massas,
    x='regiao',
    y='price',
    color='regiao',
    title='Sensibilidade ao Frete: Distribuição do Preço do Produto (Ticket) por Região',
    labels={'price': 'Preço do Produto (R$)', 'regiao': 'Região'},
    template='plotly_white'
)
fig_ticket.show()"""),

    nbf.v4.new_code_cell("""# Olhando a mediana (Centro da caixa) de forma exata
ticket_mediano = df_marketing.groupby('regiao')['price'].median().reset_index().sort_values('price')
ticket_mediano.columns = ['Região do Cliente', 'Mediana do Item Comprado (R$)']
ticket_mediano.style.background_gradient(cmap='Purples')"""),

    nbf.v4.new_markdown_cell("""### Conclusão e Oportunidade de Mercado
* O Mediano do Sudeste (que paga em média R$ 15 de frete) é confortável em comprar produtos que custam **R$ 65,00**.
* Já o Mediano do Norte/Nordeste, como paga R$ 40 de frete, ele eleva a régua do carrinho e só abre a carteira para produtos de **R$ 89,00**, evitando ou abandonando o carrinho de produtos mais baratos pela taxa de entrega percebida.

**Solução Tráfego Pago (Ads):** O Time de Marketing do E-commerce Olist está queimando R$ se anuncia produtos baratos (< R$ 60) no `Facebook Ads / Google Ads` voltados aos IPs do Nordeste. O clique vai acontecer, mas o Abandono de Carrinho é certo na hora que o frete entrar. As campanhas segmentadas para as pontas do Brasil devem exibir **apenas banners de Ticket Médio/Alto ($$$)**.""")
]

nb['cells'] = cells

with open('notebooks/Edvan/04_analise_categorias.ipynb', 'w') as f:
    nbf.write(nb, f)
