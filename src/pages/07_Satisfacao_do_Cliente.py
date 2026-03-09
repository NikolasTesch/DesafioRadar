import streamlit as st
import plotly.express as px
import pandas as pd
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from style_utils import inject_global_css, render_sidebar_logo, page_header, problema_box, insight_box, proposta_box, PLOTLY_LAYOUT, ACCENT_COLORS
from utils import get_analytical_df

st.set_page_config(page_title="Olist - O peso do Atraso", page_icon=os.path.join(os.path.dirname(__file__), "..", "public", "Radar.svg"), layout="wide")
inject_global_css()
render_sidebar_logo()

page_header("⭐ Satisfação do Cliente (NPS)", "Entendendo os detratores e drivers de lealdade")

problema_box("Embora a média de avaliação seja de ~4.0/5, categorias específicas arrastam o NPS para baixo. Mais preocupante: a <strong>nota média cai linearmente conforme o frete aumenta</strong>, revelando que o cliente percebe o custo de entrega como parte do valor do produto — e julga a empresa por isso.")

df = get_analytical_df()

if not df.empty:
    avg_score = df['review_score'].mean()
    total_reviews = df['review_score'].count()
    pct_5 = len(df[df['review_score'] == 5]) / total_reviews * 100
    pct_1_2 = len(df[df['review_score'] <= 2]) / total_reviews * 100

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Média Geral", f"{avg_score:.2f} / 5.0")
    col2.metric("Total de Reviews", f"{total_reviews:,}")
    col3.metric("% Nota 5 (Promotores)", f"{pct_5:.1f}%")
    col4.metric("% Notas 1-2 (Detratores)", f"{pct_1_2:.1f}%", delta=f"-{pct_1_2:.1f}% do total", delta_color="inverse")

    st.markdown("---")
    st.markdown("### 📊 Distribuição e Categorias Críticas")

    col_a, col_b = st.columns(2)
    with col_a:
        score_dist = df['review_score'].value_counts().sort_index().reset_index()
        score_dist.columns = ['Nota', 'Quantidade']
        score_dist['Cor'] = score_dist['Nota'].map({1: '#ff3030', 2: '#ff6b6b', 3: '#ffd93d', 4: '#4ecdc4', 5: '#00c882'})
        fig_dist = px.bar(
            score_dist, x='Nota', y='Quantidade',
            color='Nota', color_continuous_scale='RdYlGn',
            text_auto=',.0f', title="Distribuição de Notas (1 a 5)"
        )
        fig_dist.update_layout(**PLOTLY_LAYOUT)
        st.plotly_chart(fig_dist, use_container_width=True)

    with col_b:
        cat_counts = df['product_category_name'].value_counts()
        relevant_cats = cat_counts[cat_counts > 100].index
        bad_cats = (df[df['product_category_name'].isin(relevant_cats)]
                    .groupby('product_category_name')['review_score']
                    .mean().sort_values().head(10).reset_index())
        fig_bad = px.bar(
            bad_cats, x='review_score', y='product_category_name', orientation='h',
            title="Top 10 Categorias Detratoras",
            color='review_score', color_continuous_scale='Reds_r',
            labels={'review_score': 'Nota Média', 'product_category_name': 'Categoria'},
            text_auto='.2f'
        )
        fig_bad.update_layout(**PLOTLY_LAYOUT)
        st.plotly_chart(fig_bad, use_container_width=True)

    insight_box("Categorias como <strong>móveis de escritório</strong> e <strong>telefonia fixa</strong> lideram as insatisfações — frequentemente associadas a danos durante o transporte de itens volumosos e frágeis, além de prazos mais longos para entregas especiais.")

    st.markdown("---")
    st.markdown("### 💸 Sensibilidade ao Custo do Frete")
    st.markdown("Quanto mais caro o frete, menor a nota. O cliente não dissocializa o custo logístico da experiência de compra.")

    df_copy = df.copy()
    df_copy['freight_bin'] = pd.cut(df_copy['freight_value'], bins=[0, 10, 20, 30, 50, 100, 500],
                                    labels=['R$ 0–10', 'R$ 10–20', 'R$ 20–30', 'R$ 30–50', 'R$ 50–100', 'R$ 100+'])
    freight_impact = df_copy.groupby('freight_bin', observed=True)['review_score'].agg(['mean', 'count']).reset_index()
    freight_impact.columns = ['Faixa de Frete', 'Nota Média', 'Qtd Reviews']

    fig_freight = px.line(
        freight_impact, x='Faixa de Frete', y='Nota Média',
        markers=True, text='Nota Média',
        title="Impacto do Custo do Frete na Nota Média",
        labels={'Nota Média': 'Avaliação Média', 'Faixa de Frete': 'Faixa de Frete Pago'},
        color_discrete_sequence=['#6c63ff']
    )
    fig_freight.update_traces(texttemplate='%{text:.2f}', textposition='top center', line_width=3, marker_size=10)
    fig_freight.update_layout(**PLOTLY_LAYOUT)
    st.plotly_chart(fig_freight, use_container_width=True)

    proposta_box("""
    1. <strong>Frete Grátis Estratégico</strong>: Subsidiar o frete em categorias críticas (móveis, eletro) para reverter o impacto no NPS. <br><br>
    2. <strong>Programa de Proteção de Itens Frágeis</strong>: Embalagem reforçada como diferencial de categoria. <br><br>
    3. <strong>SLA de Qualidade</strong>: Estipular taxa máxima de avaliações 1-2 por seller como critério de permanência na plataforma.
""")
else:
    st.warning("Dados não carregados.")
