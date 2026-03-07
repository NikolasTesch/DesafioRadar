import streamlit as st
import pandas as pd
import plotly.express as px
from utils import get_analytical_df, treat_outliers_iqr

st.set_page_config(page_title="Qualidade dos Dados - Olist", page_icon="🧹", layout="wide")

st.title("🧹 Qualidade e Saneamento de Dados")

df = get_analytical_df()

if not df.empty:
    st.markdown("""
    ### 🛡️ Tratamento de Outliers (IQR)
    Para garantir que nossas médias não sejam distorcidas por valores extremos (ex: fretes internacionais ou erros de digitação), aplicamos o método do **Intervalo Interquartil (IQR)**.
    """)

    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Antes da Limpeza (Bruto)")
        fig_raw = px.box(df, y="receita_liquida", points="all", 
                        title="Distribuição da Receita (Líquida + Frete)",
                        color_discrete_sequence=['#e74c3c'])
        st.plotly_chart(fig_raw, use_container_width=True)
        st.caption(f"Total de registros: {len(df)}")

    with col2:
        st.subheader("Após a Limpeza (Saneado)")
        df_clean = treat_outliers_iqr(df, 'receita_liquida')
        fig_clean = px.box(df_clean, y="receita_liquida", points="suspectedoutliers",
                          title="Distribuição Saneada via IQR",
                          color_discrete_sequence=['#2ecc71'])
        st.plotly_chart(fig_clean, width="stretch")
        st.caption(f"Total de registros: {len(df_clean)}")

    st.divider()

    st.subheader("📊 Completitude dos Dados (Missing Values)")
    null_counts = df.isnull().sum()
    null_counts = null_counts[null_counts > 0].sort_values(ascending=False).reset_index()
    null_counts.columns = ['Coluna', 'Valores Ausentes']
    
    if not null_counts.empty:
        fig_null = px.bar(null_counts, x='Valores Ausentes', y='Coluna', orientation='h',
                         title="Campos com Valores Nulos",
                         color='Valores Ausentes', color_continuous_scale='Reds')
        st.plotly_chart(fig_null, use_container_width=True)
    else:
        st.success("Nenhum valor nulo encontrado nas colunas principais!")

    st.info("💡 **Garantia Técnica:** As análises financeiras e de ticket médio nas próximas páginas utilizam exclusivamente a base **Saneada**, garantindo que decisões de negócio sejam baseadas na realidade da maioria dos consumidores, não em outliers.")
else:
    st.warning("Dados não carregados.")
