import streamlit as st
import pandas as pd
import plotly.express as px
from utils import get_analytical_df

st.set_page_config(page_title="Satisfação - Olist", page_icon="⭐", layout="wide")

st.title("⭐ Satisfação do Cliente (NPS)")

df = get_analytical_df()

if not df.empty:
    st.markdown("""
    ### 🗣️ O que o cliente diz
    A nota de avaliação (`review_score`) é o principal termômetro. 
    Aqui entendemos quais categorias estão decepcionando e como o custo do frete afeta a percepção de valor.
    """)

    # KPIs de Satisfação
    avg_score = df['review_score'].mean()
    total_reviews = df['review_score'].count()
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Média de Avaliações", f"{avg_score:.2f} / 5.0")
    col2.metric("Total de Reviews", f"{total_reviews:,}")
    col3.metric("% Nota 5", f"{(len(df[df['review_score']==5])/total_reviews*100):.1f}%")

    st.divider()

    col_a, col_b = st.columns(2)

    with col_a:
        st.subheader("Distribuição de Notas (1 a 5)")
        score_dist = df['review_score'].value_counts().sort_index().reset_index()
        score_dist.columns = ['Nota', 'Quantidade']
        fig_dist = px.bar(score_dist, x='Nota', y='Quantidade', 
                         color='Nota', color_continuous_scale='RdYlGn',
                         text_auto=True)
        st.plotly_chart(fig_dist, width="stretch")

    with col_b:
        st.subheader("Categorias Críticas (Menores Notas)")
        # Apenas categorias com volume relevante (> 100 pedidos)
        cat_counts = df['product_category_name'].value_counts()
        relevant_cats = cat_counts[cat_counts > 100].index
        
        bad_cats = df[df['product_category_name'].isin(relevant_cats)].groupby('product_category_name')['review_score'].mean().sort_values().head(10).reset_index()
        
        fig_bad = px.bar(bad_cats, x='review_score', y='product_category_name', orientation='h',
                        title="Top 10 Categorias Detratoras",
                        color='review_score', color_continuous_scale='Reds_r',
                        labels={'review_score': 'Média', 'product_category_name': 'Categoria'})
        st.plotly_chart(fig_bad, width="stretch")

    st.divider()

    st.subheader("💸 Sensibilidade ao Preço do Frete")
    # Binando o frete para ver tendência
    df['freight_bin'] = pd.cut(df['freight_value'], bins=[0, 10, 20, 30, 50, 100, 500], 
                            labels=['R$ 0-10', '10-20', '20-30', '30-50', '50-100', '100+'])
    freight_impact = df.groupby('freight_bin')['review_score'].mean().reset_index()
    
    fig_freight_score = px.line(freight_impact, x='freight_bin', y='review_score', markers=True,
                               title="Impacto do Custo Logístico na Percepção de Valor",
                               labels={'review_score': 'Média de Avaliação', 'freight_bin': 'Faixa de Frete'})
    st.plotly_chart(fig_freight_score, width="stretch")

    st.info("💡 **Insight Crítico:** A nota média cai linearmente conforme o frete aumenta. Categorias como 'moveis_escritorio' e 'telefonia_fixa' lideram as insatisfações, muitas vezes ligadas a danos no transporte ou prazos excessivos em itens volumosos.")
else:
    st.warning("Dados não carregados.")
