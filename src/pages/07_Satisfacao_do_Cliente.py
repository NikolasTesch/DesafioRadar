import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from style_utils import inject_global_css, render_sidebar_logo, page_header, problema_box, insight_box, proposta_box, PLOTLY_LAYOUT, ACCENT_COLORS
from utils import get_analytical_df

st.set_page_config(page_title="Olist - Satisfação", page_icon=os.path.join(os.path.dirname(__file__), "..", "public", "Radar.svg"), layout="wide")
inject_global_css()
render_sidebar_logo()

page_header("⭐ Capítulo 3: A Voz do Cliente", "Quem são os detratores e o que os transforma em promotores")

# ── INTRO NARRATIVO ─────────────────────────────────────────────────────────────
st.markdown("""
<div style="background: rgba(108,99,255,0.07); border-left: 4px solid #6c63ff; border-radius: 0 12px 12px 0; padding: 1.2rem 1.5rem; margin-bottom: 1.5rem; font-family: 'DM Sans', sans-serif; color: #ccc; font-size: 0.95rem; line-height: 1.8;">
    Vimos que o atraso derruba a nota. Mas a insatisfação vai além do prazo.
    <strong style="color:#a89bff;">O cliente julga o produto, a embalagem, o preço e até a aparência do anúncio.</strong><br><br>
    Neste capítulo, analisamos a <strong style="color:#ffd93d;">voz do cliente através das avaliações</strong>:
    quais categorias concentram os maiores detratores, como o custo do frete impacta a percepção de valor,
    e o que realmente separa um cliente que volta a comprar de um que nunca mais vai usar a plataforma.
</div>
""", unsafe_allow_html=True)

problema_box("Embora a média geral seja de ~4.0/5, a nota <strong>cai linearmente conforme o frete aumenta</strong>. O cliente não dissocia o custo logístico da experiência — e pune a plataforma pela ineficiência, mesmo que seja culpa da transportadora.")

df = get_analytical_df()

if not df.empty:
    avg_score = df['review_score'].mean()
    total_reviews = df['review_score'].count()
    pct_5 = len(df[df['review_score'] == 5]) / total_reviews * 100
    pct_1_2 = len(df[df['review_score'] <= 2]) / total_reviews * 100
    pct_delayed_reviews = df[df['flag_atraso'] == 1]['review_score'].mean()

    # ── KPI BANNER ─────────────────────────────────────────────────────────────
    k1, k2, k3, k4, k5 = st.columns(5)
    k1.metric("Média Geral", f"{avg_score:.2f} / 5.0")
    k2.metric("Total de Reviews", f"{total_reviews:,}")
    k3.metric("% Nota 5 (Promotores)", f"{pct_5:.1f}%")
    k4.metric("% Notas 1-2 (Detratores)", f"{pct_1_2:.1f}%", delta=f"-{pct_1_2:.1f}% do total", delta_color="inverse")
    k5.metric("Nota Média c/ Atraso", f"{pct_delayed_reviews:.2f} / 5.0", delta="vs média geral", delta_color="inverse")

    st.markdown("---")

    # ── GRÁFICO GAUGE E DISTRIBUIÇÃO ───────────────────────────────────────────
    st.markdown("### Termômetro de Satisfação Geral")
    col_gauge, col_dist = st.columns([1, 2])
    with col_gauge:
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=avg_score,
            domain={'x': [0, 1], 'y': [0, 1]},
            delta={'reference': 4.0, 'increasing': {'color': '#00c882'}, 'decreasing': {'color': '#ff5050'}},
            gauge={
                'axis': {'range': [1, 5], 'tickcolor': '#aaa', 'tickfont': {'color': '#aaa'}},
                'bar': {'color': '#00c882'},
                'bgcolor': 'rgba(0,0,0,0)',
                'borderwidth': 1,
                'bordercolor': 'rgba(108,99,255,0.3)',
                'steps': [
                    {'range': [1, 2.5], 'color': 'rgba(255,48,48,0.2)'},
                    {'range': [2.5, 3.5], 'color': 'rgba(255,217,61,0.15)'},
                    {'range': [3.5, 5], 'color': 'rgba(0,200,130,0.15)'}
                ],
                'threshold': {'line': {'color': '#ffd93d', 'width': 3}, 'thickness': 0.75, 'value': 4.0}
            }
        ))
        # TRANSPARENCY: plot_bgcolor e paper_bgcolor transparentes
        fig_gauge.update_layout(
            height=300, 
            plot_bgcolor='rgba(0,0,0,0)', 
            paper_bgcolor='rgba(0,0,0,0)'
        )
        st.markdown("<div style='text-align:center; color:#d9d9d9; font-family:Poppins; padding-bottom:10px;'>Nota Média Global</div>", unsafe_allow_html=True)
        st.plotly_chart(fig_gauge, use_container_width=True)

    with col_dist:
        score_dist = df['review_score'].value_counts().sort_index().reset_index()
        score_dist.columns = ['Nota', 'Quantidade']
        score_dist['Pct'] = score_dist['Quantidade'] / score_dist['Quantidade'].sum() * 100

        fig_dist = px.bar(
            score_dist, x='Nota', y='Quantidade',
            color='Nota',
            color_continuous_scale='RdYlGn',
            range_color=[1, 5],
            text='Pct',
            hover_data={'Quantidade': ':,', 'Pct': ':.1f'},
            title="Distribuição Completa de Notas (1 a 5)"
        )
        fig_dist.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
        fig_dist.update_layout(
            plot_bgcolor='rgba(0,0,0,0)', 
            paper_bgcolor='rgba(0,0,0,0)',
            coloraxis_showscale=True,
            coloraxis_colorbar=dict(title="Nota"),
            xaxis={'type': 'category'} 
        )
        st.plotly_chart(fig_dist, use_container_width=True)

    st.markdown("---")


    # ── GRÁFICO HEATMAP ESTADO X STATUS ────────────────────────────────────
    st.markdown("### Resiliência à Falha: Nota Média por Estado × Atraso")
    heatmap_data = df.groupby(['customer_state', 'flag_atraso'])['review_score'].mean().reset_index()
    heatmap_data['Status'] = heatmap_data['flag_atraso'].map({0: 'No Prazo', 1: 'Atrasado'})
    heatmap_pivot = heatmap_data.pivot(index='customer_state', columns='Status', values='review_score').reset_index()

    fig_heatmap = px.imshow(
        heatmap_pivot.set_index('customer_state').T,
        color_continuous_scale='RdYlGn', range_color=[1, 5], aspect='auto',
        title="Impacto do Atraso por UF Cliente",
        labels=dict(x='Estado', y='Status da Entrega', color='Nota Média')
    )
    fig_heatmap.update_layout(**PLOTLY_LAYOUT)
    st.plotly_chart(fig_heatmap, use_container_width=True)

    st.markdown("---")

    # ── GRÁFICO SENSIBILIDADE AO FRETE ────────────────────────────────────
    st.markdown("### O Peso do Custo de Envio")
    df['freight_bin'] = pd.cut(df['freight_value'], bins=[0, 10, 20, 30, 50, 100, 500],
                               labels=['R$ 0–10', 'R$ 10–20', 'R$ 20–30', 'R$ 30–50', 'R$ 50–100', 'R$ 100+'])
    freight_impact = df.groupby('freight_bin', observed=True)['review_score'].agg(['mean', 'count']).reset_index()
    freight_impact.columns = ['Faixa de Frete', 'Nota Média', 'Qtd Reviews']

    fig_freight = px.bar(
        freight_impact, x='Faixa de Frete', y='Nota Média', text='Nota Média',
        color='Nota Média', color_continuous_scale='RdYlGn', range_color=[1, 5],
        title="Nota Média vs Preço de Frete",
        hover_data={'Qtd Reviews': ':,', 'Nota Média': ':.2f'}
    )
    fig_freight.update_traces(texttemplate='%{text:.2f}', textposition='outside')
    fig_freight.update_layout(**PLOTLY_LAYOUT)
    st.plotly_chart(fig_freight, use_container_width=True)

    st.markdown("---")

    # ── GRÁFICO TAXA DE ATRASO VS NOTA MÉDIA (NOVO) ───────────────────────
    st.markdown("### Correlação Regional: Atraso Operacional × Sentimento do Cliente")
    state_delay_stats = df.groupby('customer_state').agg(
        taxa_atraso=('flag_atraso', 'mean'), nota_media=('review_score', 'mean'), total=('order_id', 'count')
    ).reset_index()
    state_delay_stats['taxa_atraso_pct'] = state_delay_stats['taxa_atraso'] * 100
    state_delay_stats = state_delay_stats.sort_values('taxa_atraso_pct', ascending=False)

    fig_delay_nps = px.bar(
        state_delay_stats, x='customer_state', y='taxa_atraso_pct',
        color='nota_media', color_continuous_scale='RdYlGn', range_color=[1, 5],
        text='taxa_atraso_pct',
        labels={'taxa_atraso_pct': 'Atraso (%)', 'nota_media': 'NPS médio'},
        title="Ranking de Atraso por Estado (Cor = Nota Média)"
    )
    fig_delay_nps.update_traces(texttemplate='%{text:.1f}%', textposition='outside', textfont_size=9)
    fig_delay_nps.update_layout(**PLOTLY_LAYOUT)
    st.plotly_chart(fig_delay_nps, use_container_width=True)

    st.markdown("---")

# ── GRÁFICO TOP DETRATORES E PROMOTORES CATEGORIAS ─────────────────────
    st.markdown("### Rankings de Categoria: Onde Focar e Onde Aprender")
    st.markdown("<span style='font-family:\"DM Sans\",sans-serif; color:#888; font-size:0.9rem;'>As categorias estão avaliadas na escala de 1 a 5. Notas abaixo de 3.5 exigem revisão urgente da malha de fornecedores.</span>", unsafe_allow_html=True)

    col_a, col_b = st.columns(2)
    with col_a:
        cat_counts = df['product_category_name'].value_counts()
        relevant_cats = cat_counts[cat_counts > 100].index
        bad_cats = (df[df['product_category_name'].isin(relevant_cats)]
                    .groupby('product_category_name')
                    .agg(nota_media=('review_score', 'mean'), total=('order_id', 'count'))
                    .sort_values('nota_media').head(10).reset_index())
        fig_bad = px.bar(
            bad_cats, x='nota_media', y='product_category_name', orientation='h',
            title="Top 10 Categorias com Maior Insatisfação",
            color='nota_media', color_continuous_scale='RdYlGn', range_color=[1, 5],
            hover_data={'total': ':,', 'nota_media': ':.2f'},
            labels={'nota_media': 'Nota Média', 'product_category_name': 'Categoria', 'total': 'Qtd Pedidos'},
            text='nota_media'
        )
        fig_bad.update_traces(texttemplate='%{text:.2f}', textposition='outside')
        fig_bad.update_layout(**PLOTLY_LAYOUT)
        st.plotly_chart(fig_bad, use_container_width=True)

    with col_b:
        good_cats = (df[df['product_category_name'].isin(relevant_cats)]
                     .groupby('product_category_name')
                     .agg(nota_media=('review_score', 'mean'), total=('order_id', 'count'))
                     .sort_values('nota_media', ascending=False).head(10).reset_index())
        fig_good = px.bar(
            good_cats, x='nota_media', y='product_category_name', orientation='h',
            title="Top 10 Categorias Promotoras (Melhor NPS)",
            color='nota_media', color_continuous_scale='RdYlGn', range_color=[1, 5],
            hover_data={'total': ':,', 'nota_media': ':.2f'},
            labels={'nota_media': 'Nota Média', 'product_category_name': 'Categoria', 'total': 'Qtd Pedidos'},
            text='nota_media'
        )
        fig_good.update_traces(texttemplate='%{text:.2f}', textposition='outside')
        fig_good.update_layout(**PLOTLY_LAYOUT)
        st.plotly_chart(fig_good, use_container_width=True)

    insight_box("Categorias como <strong>móveis de escritório</strong> e <strong>eletrônicos</strong> lideram a insatisfação — associadas a danos por volume e prazo de entrega especial.")

    st.markdown("---")