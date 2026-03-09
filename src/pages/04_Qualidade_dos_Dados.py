import streamlit as st
import plotly.express as px
import pandas as pd
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from style_utils import inject_global_css, render_sidebar_logo, page_header, problema_box, insight_box, proposta_box, PLOTLY_LAYOUT, ACCENT_COLORS
from utils import get_analytical_df, treat_outliers_iqr

st.set_page_config(page_title="Olist - O peso do Atraso", page_icon=os.path.join(os.path.dirname(__file__), "..", "public", "Radar.svg"), layout="wide")
inject_global_css()
render_sidebar_logo()

page_header("🧹 Qualidade e Saneamento de Dados", "Garantindo que nossas conclusões sejam baseadas em realidade")

problema_box("Dados brutos de e-commerce frequentemente contêm <strong>outliers extremos</strong> — vendas de R$ 50.000 para um produto de R$ 50 — que distorcem médias e levam gestores a decisões erradas. Sem saneamento, o GMV aparente pode ser superestimado em até <strong>15%</strong>.")

df = get_analytical_df()

if not df.empty:
    st.markdown("---")
    st.markdown("### 📦 Tratamento de Outliers via IQR")
    st.markdown("O Intervalo Interquartil (IQR) preserva 95%+ dos dados reais enquanto remove casos extremos.")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Antes da Limpeza — Dados Brutos**")
        fig_raw = px.box(df.sample(min(5000, len(df))), y="receita_liquida",
                         points="suspectedoutliers",
                         labels={'receita_liquida': 'Receita (R$)'},
                         color_discrete_sequence=['#ff6b6b'])
        fig_raw.update_layout(**PLOTLY_LAYOUT, title="Distribuição Bruta")
        st.plotly_chart(fig_raw, use_container_width=True)
        st.caption(f"Total de registros: {len(df):,}")

    with col2:
        st.markdown("**Após a Limpeza — Dados Saneados**")
        df_clean = treat_outliers_iqr(df, 'receita_liquida')
        fig_clean = px.box(df_clean.sample(min(5000, len(df_clean))), y="receita_liquida",
                           points="suspectedoutliers",
                           labels={'receita_liquida': 'Receita (R$)'},
                           color_discrete_sequence=['#00c882'])
        fig_clean.update_layout(**PLOTLY_LAYOUT, title="Distribuição Saneada (IQR)")
        st.plotly_chart(fig_clean, use_container_width=True)
        removed = len(df) - len(df_clean)
        st.caption(f"Registros após limpeza: {len(df_clean):,} ({removed:,} removidos)")

    insight_box(f"O IQR removeu <strong>{len(df) - len(df_clean):,} registros ({(len(df)-len(df_clean))/len(df)*100:.1f}%)</strong> que eram outliers extremos. O ticket médio após limpeza é mais representativo: <strong>R$ {df_clean['receita_liquida'].mean():.2f}</strong> vs R$ {df['receita_liquida'].mean():.2f} bruto.")

    st.markdown("---")
    st.markdown("### 📊 Completitude dos Dados (Valores Ausentes)")

    null_counts = df.isnull().sum()
    null_counts = null_counts[null_counts > 0].sort_values(ascending=False).reset_index()
    null_counts.columns = ['Coluna', 'Valores Ausentes']

    if not null_counts.empty:
        null_counts['Pct'] = (null_counts['Valores Ausentes'] / len(df) * 100).round(2)
        fig_null = px.bar(null_counts, x='Valores Ausentes', y='Coluna', orientation='h',
                         color='Pct', color_continuous_scale='Reds',
                         labels={'Valores Ausentes': 'Qtd. Nulos', 'Coluna': 'Campo', 'Pct': '% Missing'},
                         text='Pct')
        fig_null.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
        fig_null.update_layout(**PLOTLY_LAYOUT, title="Campos com Valores Nulos")
        st.plotly_chart(fig_null, use_container_width=True)
    else:
        st.success("✅ Nenhum valor nulo nas colunas principais após o processamento!")

else:
    st.warning("Dados não carregados.")
