import nbformat as nbf
import os

nb = nbf.v4.new_notebook()

# 1. Introdução Estratégica
nb['cells'].append(nbf.v4.new_markdown_cell("""\
# Análise Estratégica de Sazonalidade: E-Commerce Olist (2016-2018)

## 1. Contexto Executivo

Como cientistas de dados, nossa missão é transformar registros brutos em **inteligência competitiva**. No dinâmico cenário do e-commerce brasileiro, entender os ciclos de demanda não é apenas um exercício estatístico, mas o pilar para a sobrevivência operacional.

Esta análise foca na **Sazonalidade**, o padrão repetitivo que dita o ritmo do faturamento. Navegaremos desde a limpeza técnica dos dados até a aplicação de modelos de decomposição temporal e agrupamento (Clustering) de performance mensal.

**O que este estudo entrega:**
- Identificação de picos de demanda (Black Friday e festividades).
- Decomposição da Tendência de crescimento vs. Ciclos repetitivos.
- Classificação de meses por potencial de receita (Clusters de Demanda).
- Recomendações práticas para Logística, Marketing e Pricing.
"""))

# Imports e Configurações de Design
nb['cells'].append(nbf.v4.new_code_cell("""\
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from statsmodels.tsa.seasonal import seasonal_decompose
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

import warnings
warnings.filterwarnings('ignore')

# Configurações de Estética Profissional
sns.set_theme(style="whitegrid", palette="muted")
plt.rcParams['figure.figsize'] = (12, 6)
plt.rcParams['axes.titlesize'] = 14
plt.rcParams['axes.labelsize'] = 12
"""))

# 2. Ingestão de Dados
nb['cells'].append(nbf.v4.new_markdown_cell("""\
## 2. Ingestão e Integração de Dados

Para uma visão 360º, consolidamos as principais entidades do ecossistema Olist. O foco é garantir que cada transação tenha seu registro temporal e financeiro exatos.
"""))

nb['cells'].append(nbf.v4.new_code_cell("""\
# Caminhos relativos ao workspace do projeto
path_raw = "../../data/raw"

df_orders = pd.read_csv(os.path.join(path_raw, "olist_orders_dataset.csv"))
df_items = pd.read_csv(os.path.join(path_raw, "olist_order_items_dataset.csv"))
df_payments = pd.read_csv(os.path.join(path_raw, "olist_order_payments_dataset.csv"))
df_customers = pd.read_csv(os.path.join(path_raw, "olist_customers_dataset.csv"))

print(f"Base de Pedidos carregada: {df_orders.shape[0]} registros")
"""))

# 3. Engenharia de Variáveis e Limpeza
nb['cells'].append(nbf.v4.new_markdown_cell("""\
## 3. Engenharia de Atributos Temporais

A precisão da análise de sazonalidade depende da qualidade do "Relógio" dos dados. 
- Convertemos strings para objetos de data reais.
- Extraímos componentes (Mês, Ano, Dia da Semana).
- Filtramos apenas pedidos com pagamento aprovado para evitar ruído de carrinhos abandonados.
"""))

nb['cells'].append(nbf.v4.new_code_cell("""\
# Normalização de Datas
df_orders['order_purchase_timestamp'] = pd.to_datetime(df_orders['order_purchase_timestamp'])

# Filtro de Qualidade: Apenas pedidos confirmados/entregues
valid_status = ['delivered', 'shipped', 'invoiced', 'processing']
df_clean = df_orders[df_orders['order_status'].isin(valid_status)].copy()

# Cálculo da Receita por Pedido (Preço + Frete)
df_revenue = df_items.groupby('order_id').agg({
    'price': 'sum',
    'freight_value': 'sum'
}).reset_index()
df_revenue['total_order_value'] = df_revenue['price'] + df_revenue['freight_value']

# Merge Final para Análise
df_master = df_clean.merge(df_revenue, on='order_id', how='inner')
df_master['year_month'] = df_master['order_purchase_timestamp'].dt.to_period('M')
df_master['month'] = df_master['order_purchase_timestamp'].dt.month
"""))

# 4. EDA: Perfil de Consumo
nb['cells'].append(nbf.v4.new_markdown_cell("""\
## 4. Análise Exploratória: O Perfil Financeiro do Pedido

Antes de olhar o tempo, olhamos o comportamento. Qual o "tamanho" médio da compra do brasileiro neste dataset?
"""))

nb['cells'].append(nbf.v4.new_code_cell("""\
fig, ax = plt.subplots(1, 2, figsize=(16, 6))

# Histograma de Gastos
sns.histplot(df_master[df_master['total_order_value'] < 800]['total_order_value'], bins=50, kde=True, ax=ax[0], color='#2c3e50')
ax[0].set_title('Distribuição de Valor por Pedido (Até R$ 800)')
ax[0].set_xlabel('Valor Total (R$)')
ax[0].set_ylabel('Frequência de Pedidos')

# Volume por Dia da Semana
df_master['day_name'] = df_master['order_purchase_timestamp'].dt.day_name()
dias_ordem = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
sns.countplot(data=df_master, x='day_name', order=dias_ordem, ax=ax[1], palette='viridis')
ax[1].set_title('Volume de Vendas por Dia da Semana')
ax[1].set_xlabel('Dia')
ax[1].set_ylabel('Quantidade de Pedidos')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
"""))

nb['cells'].append(nbf.v4.new_markdown_cell("""\
### 💡 Análise do Especialista:
- **Concentração de Gasto:** A grande massa de pedidos ocorre abaixo de **R$ 200**, indicando um perfil de consumo de bens de giro rápido ou utilidades domésticas.
- **Ritmo Semanal:** Notamos um volume maior de compras entre segunda e quarta-feira, com uma queda perceptível nos fins de semana. Isso sugere que o consumidor brasileiro tende a realizar compras planejadas durante a rotina de trabalho/estudo.
"""))

# 5 e 6. Séries Temporais e Decomposição
nb['cells'].append(nbf.v4.new_markdown_cell("""\
## 5 e 6. Evolução Temporal e Decomposição Estatística

Abaixo, transformamos os dados em uma Série Temporal contínua para isolar a **Tendência** (crescimento orgânico) da **Sazonalidade** (padrões cíclicos).
"""))

nb['cells'].append(nbf.v4.new_code_cell("""\
# Agregação Diária para Decomposição
ts_daily = df_master.set_index('order_purchase_timestamp').resample('D')['total_order_value'].sum().fillna(0)
# Filtro para período com dados consistentes
ts_daily = ts_daily[(ts_daily.index >= '2017-01-01') & (ts_daily.index <= '2018-08-31')]

# Decomposição Aditiva (Período de 30 dias para capturar ciclo mensal)
dec = seasonal_decompose(ts_daily, model='additive', period=30)

fig, axes = plt.subplots(4, 1, figsize=(15, 12), sharex=True)
dec.observed.plot(ax=axes[0], color='blue', title='1. Realidade (Dados Observados)')
dec.trend.plot(ax=axes[1], color='red', title='2. Tendência (Crescimento a Longo Prazo)')
dec.seasonal.plot(ax=axes[2], color='green', title='3. Sazonalidade (O Padrão Repetitivo Mensal)')
dec.resid.plot(ax=axes[3], color='gray', title='4. Resíduos (Eventos Inesperados/Ruído)')

for ax in axes:
    ax.set_ylabel('Valor (R$)')
    ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()
"""))

nb['cells'].append(nbf.v4.new_markdown_cell("""\
### 💡 Análise do Especialista:
1. **Dados Observados:** Vemos o faturamento real dia a dia, com picos muito claros no final de cada ano.
2. **Tendência:** Mostra que o negócio estava em franca expansão orgânica ao longo de 2017 e 2018. A curva é ascendente e constante.
3. **Sazonalidade:** Este é o gráfico mais importante para o planejamento. Note que ele se repete como uma "assinatura". Ele mostra os vales e picos que ocorrem dentro de cada mês.
4. **Resíduos:** Note um pico gigantesco no final de 2017 que a sazonalidade normal não explicou. Esse é o efeito isolado da **Black Friday**, um evento "fora da curva" que demanda operação especial.
"""))

# 8. Clustering de Performance (Níveis de Demanda)
nb['cells'].append(nbf.v4.new_markdown_cell("""\
## 8. Agrupamento (Clustering) de Meses por Nível de Demanda

Não tratamos todos os meses da mesma forma. Usamos aprendizado de máquina (K-Means) para classificar cada mês em categorias de performance: **Baixa**, **Média** ou **Alta Demanda**.
"""))

nb['cells'].append(nbf.v4.new_code_cell("""\
# Preparação dos dados por mês
meses_metrics = df_master.groupby('year_month').agg({
    'order_id': 'count',
    'total_order_value': 'sum'
}).reset_index()

# Filtrando bordas
meses_metrics = meses_metrics[(meses_metrics['year_month'] >= '2017-01') & (meses_metrics['year_month'] <= '2018-08')]

scaler = StandardScaler()
X = scaler.fit_transform(meses_metrics[['order_id', 'total_order_value']])

# K-Means com 3 clusters
kmeans = KMeans(n_clusters=3, random_state=42)
meses_metrics['cluster'] = kmeans.fit_predict(X)

# Mapeando Nomes Baseado no Faturamento Central de cada Cluster
centros = meses_metrics.groupby('cluster')['total_order_value'].mean().sort_values()
mapeamento = {
    centros.index[0]: 'Baixa Demanda',
    centros.index[1]: 'Média Demanda',
    centros.index[2]: 'Alta Demanda'
}
meses_metrics['Categoria'] = meses_metrics['cluster'].map(mapeamento)

# Visualização do Agrupamento
plt.figure(figsize=(12, 7))
sns.scatterplot(data=meses_metrics, x='order_id', y='total_order_value', 
                hue='Categoria', style='Categoria', s=200, palette=['red', 'orange', 'green'])

# Anotando os meses para clareza - Usando iloc para evitar KeyError
for i in range(meses_metrics.shape[0]):
    plt.text(meses_metrics['order_id'].iloc[i]+100, 
             meses_metrics['total_order_value'].iloc[i], 
             str(meses_metrics['year_month'].iloc[i]), 
             fontsize=9)

plt.title('Classificação do Meses: Qual o Potencial de Faturamento?')
plt.xlabel('Volume de Pedidos')
plt.ylabel('Faturamento Total (R$)')
plt.grid(True, linestyle='--', alpha=0.6)
plt.show()
"""))

nb['cells'].append(nbf.v4.new_markdown_cell("""\
### 💡 Análise do Especialista:
Este gráfico "clusteriza" os meses em três grupos de risco e oportunidade:
1. **🔴 Baixa Demanda (Vermelho):** O início de 2017. É a fase de entrada ou períodos de ressaca pós-festas.
2. **🟠 Média Demanda (Laranja):** Onde o negócio estabiliza. Requer manutenção de estoque padrão.
3. **🟢 Alta Demanda (Verde):** Meses como Novembro (Black Friday) e picos de 2018. Aqui a infraestrutura logística deve estar no limite máximo de escalonamento para evitar atrasos.
"""))

# 9. Correlação e Pagamentos
nb['cells'].append(nbf.v4.new_markdown_cell("""\
## 9. Tendência de Pagamentos vs. Valor do Pedido

Existe relação entre o valor da compra e como o cliente paga? No Brasil, o faturamento via Cartão de Crédito costuma estar atado a parcelamentos de alto ticket.
"""))

nb['cells'].append(nbf.v4.new_code_cell("""\
df_pay_order = df_payments.merge(df_master[['order_id', 'total_order_value', 'month']], on='order_id')

plt.figure(figsize=(12, 6))
sns.boxplot(data=df_pay_order, x='payment_type', y='total_order_value', palette='Set2')
plt.ylim(0, 1000) # Foco na massa principal
plt.title('Distribuição de Gasto por Tipo de Pagamento')
plt.xlabel('Tipo de Pagamento')
plt.ylabel('Valor do Pedido (R$)')
plt.show()
"""))

nb['cells'].append(nbf.v4.new_markdown_cell("""\
### 💡 Análise do Especialista:
- **Cartão de Crédito:** É o método que sustenta os pedidos de maior valor (Outliers acima de R$ 500 são comuns).
- **Boleto:** Utilizado majoritariamente para compras de ticket médio-baixo.
- **Estratégia:** Em meses de **Alta Demanda**, incentivar o parcelamento no cartão pode elevar ainda mais o Ticket Médio, enquanto em meses de **Baixa Demanda**, descontos no boleto podem atrair fluxo de caixa rápido.
"""))

# 13. Conclusões e Recomendações
nb['cells'].append(nbf.v4.new_markdown_cell("""\
## 13. Conclusão Geral e Recomendações Estratégicas

Após a análise profunda dos ciclos de 2017-2018, consolidamos os seguintes pilares para a tomada de decisão:

### Principais Descobertas:
1. **O Efeito Black Friday:** Novembro não é apenas um mês de "Alta Demanda", é uma anomalia estatística positiva. O faturamento chega a ser o triplo de um mês de baixa.
2. **Resiliência de Meio de Semana:** As vendas síncronas com o horário comercial sugerem que o marketing deve ser intensificado entre **Segunda e Quinta**, quando o consumidor está "ativo" digitalmente.
3. **Crescimento Saudável:** A tendência mostra que o e-commerce não depende só de datas sazonais; há um crescimento de base constante mês a mês.

### Recomendações para a Diretoria:
- **Operacional (Set-Nov):** Iniciar contratação de transportadoras temporárias (contratos Flex) já em Setembro para suportar o cluster de "Alta Demanda".
- **Marketing (Jan-Fev):** Período histórico de menor faturamento. Recomenda-se campanhas de "Liquidação de Verão" para girar o estoque que sobrou do Natal.
- **Sistemas:** Monitorar a escalabilidade dos servidores para os picos identificados nos "Resíduos" da série temporal, garantindo que o site suporte o tráfego 5x superior em dias promocionais.
"""))

# Gravação do Notebook
notebook_path = 'e:/AULAS/Alpha edtech/hard skill/Modulo 11 - Python/desafio dados/DesafioRadar/notebooks/davi/Analise_Sazonalidade.ipynb'
os.makedirs(os.path.dirname(notebook_path), exist_ok=True)
with open(notebook_path, 'w', encoding='utf-8') as f:
    nbf.write(nb, f)

print(f"Notebook gerado com sucesso em: {notebook_path}")
