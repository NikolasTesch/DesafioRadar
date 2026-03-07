import streamlit as st
import plotly.express as px
from utils import get_analytical_df, treat_outliers_iqr

st.set_page_config(page_title="Regionalidade - Olist", page_icon="🌎", layout="wide")

st.title("🌎 Análise de Regionalidade: O Impacto Geográfico")

df = get_analytical_df()

if not df.empty:
    st.markdown("""
    ### 🗺️ Contexto Regional
    O comércio eletrônico no Brasil é ditado pela distância física. 
    Abaixo, analisamos como a concentração logística no Sudeste cria barreiras para outras regiões.
    """)

    # Usando base saneada para médias de frete e receita por estado
    df_clean = treat_outliers_iqr(df, 'receita_liquida')
    
    estado_stats = df_clean.groupby('customer_state').agg({
        'receita_liquida': 'sum',
        'freight_value': 'mean',
        'tempo_entrega_real': 'mean'
    }).reset_index()

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Faturamento Total por UF")
        fig_rev = px.bar(estado_stats.sort_values('receita_liquida', ascending=False), 
                         x='customer_state', y='receita_liquida', 
                         labels={'receita_liquida': 'Receita (R$)', 'customer_state': 'Estado'},
                         color='receita_liquida', color_continuous_scale='Blues')
        st.plotly_chart(fig_rev, width="stretch")

    with col2:
        st.subheader("Custo Médio de Frete por UF")
        fig_freight = px.bar(estado_stats.sort_values('freight_value', ascending=True), 
                             x='customer_state', y='freight_value',
                             labels={'freight_value': 'Frete Médio (R$)', 'customer_state': 'Estado'},
                             color='freight_value', color_continuous_scale='YlOrRd')
        st.plotly_chart(fig_freight, width="stretch")

    st.divider()
    
    st.subheader("📍 Matriz de Dispersão: Frete vs Prazo vs Volume")
    st.markdown("Quanto maior a bolha, maior o faturamento. Note como os estados do Norte (RR, AP, AC) estão isolados no canto superior direito.")
    
    fig_scatter = px.scatter(estado_stats, x='freight_value', y='tempo_entrega_real',
                             size='receita_liquida', color='customer_state', 
                             hover_name='customer_state',
                             labels={'freight_value': 'Frete Médio (R$)', 
                                     'tempo_entrega_real': 'Prazo Médio Real (Dias)'},
                             title="Análise de Competitividade Regional")
    st.plotly_chart(fig_scatter, width="stretch")

    st.info("💡 **Insight Geográfico:** O frete em Roraima (RR) é até 4x mais caro que em São Paulo (SP). Isso cria uma barreira de entrada intransponível para categorias de baixo ticket médio fora do eixo Sul-Sudeste.")
else:
    st.warning("Dados não carregados.")
