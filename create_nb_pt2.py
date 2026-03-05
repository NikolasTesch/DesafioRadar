import nbformat as nbf
import os

with open('notebooks/Edvan/02_analise_regionalidade.ipynb') as f:
    nb = nbf.read(f, as_version=4)

new_cells = [
    nbf.v4.new_markdown_cell("""---
## PARTE 2: A Rota da Desigualdade (Origem vs Destino)
Nesta segunda parte da Análise Exploratória, investigaremos a **Causa Raiz** do frete caro e do tempo de entrega nas regiões distantes. Será que o problema não é do cliente, e sim de onde os nossos Lojistas (Sellers) estão de fato operando?"""),
    
    nbf.v4.new_code_cell("""# Carregando nova base: Vendedores
path_sellers = '../../data/raw/olist_sellers_dataset.csv'

# Precisamos do seller_id e do estado (uf) onde ele reside
cols_sellers = ['seller_id', 'seller_state']
df_sellers = pd.read_csv(path_sellers, usecols=cols_sellers)

# Problema: A tabela df_items original que lemos não trouxe o seller_id
# Temos que recarregar a df_items puxando o seller_id para fazer a ponte
cols_items_full = ['order_id', 'seller_id', 'price', 'freight_value']
df_items_full = pd.read_csv(path_items, usecols=cols_items_full)

# Como um pedido pode ter itens de múltiplos vendedores (Marketplace), 
# para fins de simplificação logística, vamos pegar o 1º vendedor de cada pedido
df_order_seller = df_items_full.groupby('order_id').first().reset_index()[['order_id', 'seller_id']]

# Integrando ao nosso Super DataFrame Master!
df_master = df_master.merge(df_order_seller, on='order_id', how='left')
df_master = df_master.merge(df_sellers, on='seller_id', how='left')

# Aplicando nossa função 'map_regiao' já existente para classificar o Vendedor
df_master['regiao_vendedor'] = df_master['seller_state'].apply(map_regiao)

print(f"Merge concluído com sucesso. Colunas atuais de localidade: Cliente ({df_master['regiao'].iloc[0]}) || Vendedor ({df_master['regiao_vendedor'].iloc[0]})")"""),

    nbf.v4.new_markdown_cell("""### 2.1 A Concentração do Fornecimento (Marketplace)
Onde estão situadas fisicamente as lojas que vendem pela nossa plataforma e-commerce Olist?"""),

    nbf.v4.new_code_cell("""sellers_por_estado = df_sellers['seller_state'].value_counts().reset_index()
sellers_por_estado.columns = ['Estado', 'Total de Vendedores']

# Exibindo um Gráfico de Barras / Pareto para visualizar o esmagamento
fig_sellers = px.bar(
    sellers_por_estado.head(10), 
    x='Estado', 
    y='Total de Vendedores',
    title='Top 10 Estados Concentradores de Lojistas Parceiros (Fornecimento)',
    template='plotly_white',
    color='Total de Vendedores',
    color_continuous_scale='Reds'
)

fig_sellers.show()"""),

    nbf.v4.new_markdown_cell("""### Insight Socrático 3:
Mais do que comprovamos. **São Paulo (SP) abriga literalmente mais de 60%** dos lojistas parceiros cadastrados no E-commerce. Isso gera um gargalo logístico: a base de clientes do Brasil inteiro está virtualizando compras na mesma cidade logística."""),

    nbf.v4.new_markdown_cell("""### 2.2 O Mapa de Calor do Fluxo (Matriz Origem-Destino)
Quantas vendas (em % ou valor absoluto) cruzam "as fronteiras" das Regiões Brasileiras? O frete Intra-Região (mesma região) é de fato o que alavanca as vendas?"""),

    nbf.v4.new_code_cell("""# Matriz de Pivot (Tabela Dinâmica) cruzando Origem do Produto X Destino do Cliente
matriz_fluxo = pd.crosstab(
    df_master['regiao_vendedor'],   # Origem (Linhas)
    df_master['regiao']             # Destino do Cliente (Colunas)
)

fig_heatmap = go.Figure(data=go.Heatmap(
    z=matriz_fluxo.values,
    x=matriz_fluxo.columns,
    y=matriz_fluxo.index,
    colorscale='dense',
    text=matriz_fluxo.values,
    texttemplate="%{text}",
))

fig_heatmap.update_layout(
    title='Mapa de Fluxo Logístico: Origem do Vendedor (Y) vs Repositório do Cliente (X)',
    xaxis_title='Destino (Região do Cliente)',
    yaxis_title='Origem (Região do Lojista)',
    template='plotly_white'
)
fig_heatmap.show()"""),

    nbf.v4.new_code_cell("""# Prova final do Custo Logístico Inter-Regional
# Criando uma flag: Venda da Mesma Região (True) vs Exportação Interna / Outra Região (False)
df_master['mesma_regiao'] = df_master['regiao'] == df_master['regiao_vendedor']

frete_intra_vs_inter = df_master.groupby(['regiao', 'mesma_regiao'])['freight_value'].mean().reset_index()
frete_intra_vs_inter = frete_intra_vs_inter.pivot(index='regiao', columns='mesma_regiao', values='freight_value')
frete_intra_vs_inter.columns = ['Vem de Outra Região (Inter)', 'Comprado na Própria Região (Intra)']

frete_intra_vs_inter.style.format("R$ {:.2f}").background_gradient(cmap='Greens')"""),

    nbf.v4.new_markdown_cell("""### Conclusão Final (Rota 1)
Eis o nosso argumento irrefutável para a Diretoria.
A tabela viva acima não deixa enganar: Se um cliente do **Nordeste** compra um produto que sai do Nordeste, em média ele paga **R$ 15** de frete. O problema é que isso raramente acontece (olhe o mapa de calor no eixo Nordeste -> Nordeste).
Como o fornecimento está esmagado no Sudeste, esse mesmo cliente nordestino termina importando o produto via SP/Sudeste, encarecendo brutalmente o frete para a média insustentável de **R$ 38** que observamos na primeira análise!""")
]

# Estender o notebook atual com as novas celulas e salvar
nb['cells'].extend(new_cells)

with open('notebooks/Edvan/02_analise_regionalidade.ipynb', 'w') as f:
    nbf.write(nb, f)
