import streamlit as st
import plotly.express as px
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from style_utils import inject_global_css, render_sidebar_logo, page_header, problema_box, insight_box, proposta_box, PLOTLY_LAYOUT, ACCENT_COLORS
from utils import get_analytical_df, treat_outliers_iqr

st.set_page_config(page_title="Olist - O peso do Atraso", page_icon=os.path.join(os.path.dirname(__file__), "..", "public", "Radar.svg"), layout="wide")
inject_global_css()
render_sidebar_logo()

page_header("🌎 Análise de Regionalidade", "Como a geografia divide o Brasil em dois e-commerces")

problema_box("O Brasil é continental. O custo de frete para Roraima (RR) pode ser <strong>4x maior</strong> que para São Paulo (SP). Isso cria uma barreira de entrada insuperável para categorias de baixo ticket médio fora do eixo Sul-Sudeste, limitando o crescimento orgânico da plataforma em regiões com alta demanda reprimida.")

df = get_analytical_df()

if not df.empty:
    df_clean = treat_outliers_iqr(df, 'receita_liquida')

    estado_stats = df_clean.groupby('customer_state').agg(
        receita_liquida=('receita_liquida', 'sum'),
        freight_value=('freight_value', 'mean'),
        tempo_entrega_real=('tempo_entrega_real', 'mean'),
        num_pedidos=('order_id', 'count')
    ).reset_index()

    st.markdown("---")
    st.markdown("### 💰 Faturamento vs Custo Logístico por UF")

    col1, col2 = st.columns(2)
    with col1:
        fig_rev = px.bar(
            estado_stats.sort_values('receita_liquida', ascending=False),
            x='customer_state', y='receita_liquida',
            labels={'receita_liquida': 'Receita Total (R$)', 'customer_state': 'Estado'},
            color='receita_liquida', color_continuous_scale='Blues',
            title="Faturamento Total por UF"
        )
        fig_rev.update_layout(**PLOTLY_LAYOUT)
        st.plotly_chart(fig_rev, use_container_width=True)

    with col2:
        fig_freight = px.bar(
            estado_stats.sort_values('freight_value', ascending=False),
            x='customer_state', y='freight_value',
            labels={'freight_value': 'Frete Médio (R$)', 'customer_state': 'Estado'},
            color='freight_value', color_continuous_scale='YlOrRd',
            title="Custo Médio de Frete por UF"
        )
        fig_freight.update_layout(**PLOTLY_LAYOUT)
        st.plotly_chart(fig_freight, use_container_width=True)

    insight_box("SP, RJ e MG concentram <strong>mais de 60% do faturamento</strong>, mas têm os menores fretes e prazos. Estados do Norte e Nordeste pagam mais caro, esperam mais e ainda assim têm volumes menores — evidenciando um mercado potencial sub-explorado.")

    st.markdown("---")
    st.markdown("### 📍 Matriz de Competitividade Regional")
    st.markdown("Cada bolha representa um estado. Tamanho = volume de pedidos. Posição = custo de frete vs prazo de entrega.")

    fig_scatter = px.scatter(
        estado_stats, x='freight_value', y='tempo_entrega_real',
        size='num_pedidos', color='customer_state',
        hover_name='customer_state',
        hover_data={'receita_liquida': ':,.0f', 'num_pedidos': ':,'},
        labels={
            'freight_value': 'Frete Médio (R$)',
            'tempo_entrega_real': 'Prazo Médio Real (Dias)',
            'customer_state': 'Estado'
        },
        title="Análise de Competitividade Regional: Frete × Prazo × Volume",
        color_discrete_sequence=ACCENT_COLORS
    )
    fig_scatter.update_layout(**PLOTLY_LAYOUT, height=500)
    st.plotly_chart(fig_scatter, use_container_width=True)

    st.markdown("---")
    st.markdown("### 🏆 Ranking de Estados por Eficiência Logística")
    estado_stats['score_eficiencia'] = (
        (1 / estado_stats['freight_value'].rank()) +
        (1 / estado_stats['tempo_entrega_real'].rank())
    ).rank(ascending=False)

    top_states = estado_stats.nsmallest(10, 'freight_value')[['customer_state', 'freight_value', 'tempo_entrega_real', 'num_pedidos']]
    top_states.columns = ['Estado', 'Frete Médio (R$)', 'Prazo Médio (Dias)', 'Volume de Pedidos']
    st.dataframe(top_states.reset_index(drop=True), use_container_width=True, hide_index=True)

    proposta_box("Implementar <strong>Hubs de Distribuição Regionais</strong> em Recife (PE) e Manaus (AM) reduziria o custo e prazo logístico para Norte e Nordeste em até 40%, desbloqueando um mercado potencial de milhões de consumidores mal atendidos.")
else:
    st.warning("Dados não carregados.")
