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

page_header("⭐ Capítulo 4: A Voz do Cliente", "Quem são os detratores e o que os transforma em promotores")

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

    # ── GRÁFICO 1: GAUGE DE NPS ───────────────────────────────────────────────
    st.markdown("### Termômetro de Satisfação Geral")
    col_gauge, col_dist = st.columns([1, 2])
    with col_gauge:
        # Gauge de nota média — leitura imediata de "saudável" vs "crítico"
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=avg_score,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Nota Média Global", 'font': {'color': '#d9d9d9', 'family': 'Poppins'}},
            delta={'reference': 4.0, 'increasing': {'color': '#00c882'}, 'decreasing': {'color': '#ff5050'}},
            gauge={
                'axis': {'range': [1, 5], 'tickcolor': '#aaa', 'tickfont': {'color': '#aaa'}},
                'bar': {'color': '#6c63ff'},
                'bgcolor': 'rgba(0,0,0,0)',
                'borderwidth': 1,
                'bordercolor': 'rgba(108,99,255,0.3)',
                'steps': [
                    {'range': [1, 2.5], 'color': 'rgba(255,80,80,0.2)'},
                    {'range': [2.5, 3.5], 'color': 'rgba(255,217,61,0.15)'},
                    {'range': [3.5, 5], 'color': 'rgba(0,200,130,0.15)'}
                ],
                'threshold': {'line': {'color': '#ffd93d', 'width': 3}, 'thickness': 0.75, 'value': 4.0}
            }
        ))
        fig_gauge.update_layout(**PLOTLY_LAYOUT, height=300)
        st.plotly_chart(fig_gauge, use_container_width=True)

    with col_dist:
        # Distribuição de notas
        score_dist = df['review_score'].value_counts().sort_index().reset_index()
        score_dist.columns = ['Nota', 'Quantidade']
        colors = {1: '#ff3030', 2: '#ff6b6b', 3: '#ffd93d', 4: '#4ecdc4', 5: '#00c882'}
        score_dist['Cor'] = score_dist['Nota'].map(colors)
        score_dist['Pct'] = score_dist['Quantidade'] / score_dist['Quantidade'].sum() * 100

        fig_dist = px.bar(
            score_dist, x='Nota', y='Quantidade',
            color='Nota', color_discrete_map=colors,
            text='Pct',
            hover_data={'Quantidade': ':,', 'Pct': ':.1f'},
            title="Distribuição Completa de Notas (1 a 5)"
        )
        fig_dist.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
        fig_dist.update_layout(**PLOTLY_LAYOUT, showlegend=False)
        st.plotly_chart(fig_dist, use_container_width=True)

    st.markdown("---")

    # ── GRÁFICO 2: TOP DETRATORES POR CATEGORIA ──────────────────────────────
    st.markdown("### Categorias Detratoras — Onde o Problema é Recorrente")
    st.markdown("<span style='font-family:\"DM Sans\",sans-serif; color:#888; font-size:0.9rem;'>Categorias com nota média abaixo de 3.5 são detratoras sistemáticas. Frequentemente associadas a produtos frágeis, volumosos ou de baixa qualidade percebida.</span>", unsafe_allow_html=True)

    col_a, col_b = st.columns(2)
    with col_a:
        cat_counts = df['product_category_name'].value_counts()
        relevant_cats = cat_counts[cat_counts > 100].index
        # Insight: categorias de alto volume porém baixa nota = maior impacto no NPS geral
        bad_cats = (df[df['product_category_name'].isin(relevant_cats)]
                    .groupby('product_category_name')
                    .agg(nota_media=('review_score', 'mean'), total=('order_id', 'count'))
                    .sort_values('nota_media').head(10).reset_index())
        fig_bad = px.bar(
            bad_cats, x='nota_media', y='product_category_name', orientation='h',
            title="Top 10 Categorias com Maior Insatisfação",
            color='nota_media', color_continuous_scale='Reds_r',
            range_color=[1, 4],
            hover_data={'total': ':,', 'nota_media': ':.2f'},
            labels={'nota_media': 'Nota Média', 'product_category_name': 'Categoria', 'total': 'Qtd Pedidos'},
            text='nota_media'
        )
        fig_bad.update_traces(texttemplate='%{text:.2f}', textposition='outside')
        fig_bad.update_layout(**PLOTLY_LAYOUT)
        st.plotly_chart(fig_bad, use_container_width=True)

    with col_b:
        # Top categorias PROMOTORAS — o contraponto positivo
        good_cats = (df[df['product_category_name'].isin(relevant_cats)]
                     .groupby('product_category_name')
                     .agg(nota_media=('review_score', 'mean'), total=('order_id', 'count'))
                     .sort_values('nota_media', ascending=False).head(10).reset_index())
        fig_good = px.bar(
            good_cats, x='nota_media', y='product_category_name', orientation='h',
            title="Top 10 Categorias Promotoras (Melhor NPS)",
            color='nota_media', color_continuous_scale='Greens',
            range_color=[3.5, 5],
            hover_data={'total': ':,', 'nota_media': ':.2f'},
            labels={'nota_media': 'Nota Média', 'product_category_name': 'Categoria', 'total': 'Qtd Pedidos'},
            text='nota_media'
        )
        fig_good.update_traces(texttemplate='%{text:.2f}', textposition='outside')
        fig_good.update_layout(**PLOTLY_LAYOUT)
        st.plotly_chart(fig_good, use_container_width=True)

    insight_box("Categorias como <strong>móveis de escritório</strong> e <strong>eletrônicos</strong> lideram a insatisfação — associadas a danos por volume e prazo de entrega especial. "
                "Em contraste, <strong>artigos de presente e flores</strong> têm NPS alto: produto pequeno, entrega simples, expectativa gerenciável.")

    st.markdown("---")

    # ── GRÁFICO 3: HEATMAP — NOTA POR ESTADO E STATUS DE ATRASO ─────────────
    st.markdown("### Análise Cruzada: Nota Média por Estado × Status de Entrega")
    st.markdown("<span style='font-family:\"DM Sans\",sans-serif; color:#888; font-size:0.9rem;'>Clientes de estados mais distantes sofrem duplamente: mais atrasos e notas mais baixas, mesmo nas entregas pontuais.</span>", unsafe_allow_html=True)

    heatmap_data = df.groupby(['customer_state', 'flag_atraso'])['review_score'].mean().reset_index()
    heatmap_data['Status'] = heatmap_data['flag_atraso'].map({0: 'No Prazo', 1: 'Atrasado'})
    heatmap_pivot = heatmap_data.pivot(index='customer_state', columns='Status', values='review_score').reset_index()

    fig_heatmap = px.imshow(
        heatmap_pivot.set_index('customer_state').T,
        color_continuous_scale='RdYlGn', range_color=[2.0, 5.0],
        aspect='auto',
        title="Nota Média por Estado × Status de Entrega",
        labels=dict(x='Estado', y='Status', color='Nota Média')
    )
    fig_heatmap.update_layout(**PLOTLY_LAYOUT)
    st.plotly_chart(fig_heatmap, use_container_width=True)

    st.markdown("---")

    # ── GRÁFICO 4: IMPACTO DO FRETE NA NOTA ──────────────────────────────────
    st.markdown("### Sensibilidade ao Custo de Frete")
    st.markdown("<span style='font-family:\"DM Sans\",sans-serif; color:#888; font-size:0.9rem;'>O cliente não separa o valor do frete do valor do produto. Quanto mais caro o frete, menor a nota — mesmo que o produto tenha chegado no prazo.</span>", unsafe_allow_html=True)

    df_copy = df.copy()
    df_copy['freight_bin'] = pd.cut(df_copy['freight_value'],
                                    bins=[0, 10, 20, 30, 50, 100, 500],
                                    labels=['R$ 0–10', 'R$ 10–20', 'R$ 20–30', 'R$ 30–50', 'R$ 50–100', 'R$ 100+'])
    freight_impact = df_copy.groupby('freight_bin', observed=True)['review_score'].agg(['mean', 'count']).reset_index()
    freight_impact.columns = ['Faixa de Frete', 'Nota Média', 'Qtd Reviews']

    fig_freight = px.line(
        freight_impact, x='Faixa de Frete', y='Nota Média',
        markers=True, text='Nota Média',
        title="Nota Média por Faixa de Frete Pago",
        hover_data={'Qtd Reviews': ':,', 'Nota Média': ':.2f'},
        color_discrete_sequence=['#6c63ff']
    )
    fig_freight.update_traces(texttemplate='%{text:.2f}', textposition='top center', line_width=3, marker_size=10)
    fig_freight.update_layout(**PLOTLY_LAYOUT)
    st.plotly_chart(fig_freight, use_container_width=True)

    st.markdown("---")

    proposta_box("""
    <strong>1. Frete Grátis Estratégico:</strong> Subsidiar o frete em categorias críticas (móveis, eletro) via seller fee ou programa de assinatura. O ganho de NPS supera o custo do subsídio em LTV.<br><br>
    <strong>2. Proteção de Itens Frágeis:</strong> Rating de embalagem por categoria. Sellers que vendem itens volumosos/frágeis devem cumprir padrões mínimos de embalagem, sob pena de perda de buy-box.<br><br>
    <strong>3. SLA de Qualidade (Seller Shield):</strong> Estabelecer taxa máxima de reviews 1-2 (ex: 10%) por seller como critério de permanência na plataforma. Sellers com NPS negativo sistêmico são removidos ou penalizados.
    """)

    # ── BRIDGE NARRATIVO ─────────────────────────────────────────────────────
    st.markdown("""
    <div style="margin-top:2rem; padding: 1.2rem 1.5rem; background: rgba(108,99,255,0.06); border-radius: 12px; border: 1px solid rgba(108,99,255,0.2); font-family: 'DM Sans', sans-serif; color: #aaa; font-size: 0.9rem; line-height: 1.7;">
        🔜 <strong style="color:#a89bff;">Próximo Capítulo: Financeiro e Pagamentos</strong><br>
        Problemas de NPS têm custo financeiro direto. No próximo capítulo, quantificamos esse impacto:
        quanto vale o GMV que está sendo perdido, como o parcelamento pode ampliar o ticket médio,
        e onde está a oportunidade financeira oculta para a plataforma.
    </div>
    """, unsafe_allow_html=True)

else:
    st.warning("Dados não carregados.")
