# Projeto Olist: Dashboard de Apresentação Estratégica

## Visão Geral
Este projeto consiste em uma aplicação Streamlit para visualização e análise dos dados do e-commerce Olist. Ele consolida análises de regionalidade, logística, satisfação do cliente e finanças.

**Para executar:**
```bash
streamlit run src/app.py
```

## Explicação Técnica Detalhada

### Carregamento e Processamento de Dados (`src/utils.py`)

```python
@st.cache_data
def get_analytical_df():
    # ... merges e feature engineering ...
    df['tempo_real_entrega_dias'] = (df['order_delivered_customer_date'] - df['order_approved_at']).dt.total_seconds() / 86400
```
1. **Snippet**: O código realiza a junção de 7 tabelas e calcula o tempo de entrega em dias.
2. **Explicação**: Utilizamos o `merge` do pandas para criar uma visão 360 do pedido. O cálculo de tempo é feito transformando a diferença de `datetime` em segundos e dividindo pelo total de segundos de um dia (86.400).
3. **Natives**: `pd.merge`, `pd.to_datetime`. Usamos o merge `inner` para garantir integridade entre pedidos e clientes, e `left` para produtos e avaliações que podem ser nulos.
4. **Design**: O uso do decorator `@st.cache_data` é crucial por performance, pois evita reprocessar o merge de ~100k linhas a cada interação do usuário.

### Interface Multipage (`src/app.py` e `src/pages/`)

```python
st.set_page_config(page_title="Análise Estratégica Olist", layout="wide")
```
1. **Snippet**: Configuração básica do Streamlit para modo "wide".
2. **Explicação**: Definimos o layout da página para ocupar toda a largura da tela, ideal para dashboards com muitos gráficos.
3. **Natives**: Estrutura de diretório nativa do Streamlit para múltiplas páginas.
4. **Design**: Priorizamos uma interface limpa com `st.metric` para KPIs rápidos logo na home.

### Visualização de Regionalidade (`src/pages/02_Regionalidade.py`)

```python
fig_scatter = px.scatter(estado_stats, x='freight_value', y='tempo_real_entrega_dias', size='payment_value')
```
1. **Snippet**: Gráfico de dispersão correlacionando Frete, Prazo e Volume.
2. **Explicação**: Cada bolha representa um estado. O tamanho da bolha indica o faturamento, permitindo identificar que o Sudeste (baixo frete/prazo) concentra o maior volume.
3. **Design**: Escolha do Plotly pela capacidade de interatividade (zoom e hover), essencial para explorar 27 estados simultaneamente.