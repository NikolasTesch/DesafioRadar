import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from style_utils import inject_global_css, render_sidebar_logo, page_header, problema_box, insight_box, proposta_box, PLOTLY_LAYOUT, ACCENT_COLORS
from utils import get_analytical_df, treat_outliers_iqr

st.set_page_config(page_title="Olist - Regionalidade", page_icon=os.path.join(os.path.dirname(__file__), "..", "public", "Radar.svg"), layout="wide")
inject_global_css()
render_sidebar_logo()

page_header("🌎 Capítulo 2: Dois Brasis", "A geografia como barreira de crescimento no e-commerce")

# ── INTRO NARRATIVO ─────────────────────────────────────────────────────────────
st.markdown("""
<div style="background: rgba(108,99,255,0.07); border-left: 4px solid #6c63ff; border-radius: 0 12px 12px 0; padding: 1.2rem 1.5rem; margin-bottom: 1.5rem; font-family: 'DM Sans', sans-serif; color: #ccc; font-size: 0.95rem; line-height: 1.8;">
    O Brasil é um continente disfarçado de país. A distância de São Paulo a Manaus é maior que a de Lisboa a Moscou.
    Essa realidade geográfica cria <strong style="color:#ff5050;">dois e-commerces radicalmente diferentes</strong> operando sob a mesma plataforma:
    um privilegiado no eixo Sul-Sudeste, e outro sub-servido no Norte-Nordeste.
</div>
""", unsafe_allow_html=True)

problema_box("Clientes no Norte/Nordeste pagam fretes até <strong>400% maiores</strong> e aguardam prazos <strong>2x mais longos</strong> que clientes em SP. Isso destrói a percepção de valor e o NPS em regiões com enorme demanda reprimida.")

df = get_analytical_df()

if not df.empty:
    # ── FILTRO POR REGIÃO ──────────────────────────────────────────────────────
    st.sidebar.markdown("### 🔍 Filtros de Análise")
    regioes_disponiveis = sorted(df['customer_region'].dropna().unique().tolist())
    regiao_selecionada = st.sidebar.multiselect(
        "Selecione a(s) Região(ões):",
        options=regioes_disponiveis,
        default=regioes_disponiveis
    )

    # Aplicando o filtro
    df_filtered = df[df['customer_region'].isin(regiao_selecionada)]
    
    if df_filtered.empty:
        st.warning("Nenhum dado encontrado para a(s) região(ões) selecionada(s).")
        st.stop()

    df_clean = treat_outliers_iqr(df_filtered, 'receita_liquida')

    # Agregação enriquecida por estado
    estado_stats = df_clean.groupby('customer_state').agg(
        receita_liquida=('receita_liquida', 'sum'),
        freight_value=('freight_value', 'mean'),
        tempo_entrega_real=('tempo_entrega_real', 'mean'),
        num_pedidos=('order_id', 'count'),
        review_score=('review_score', 'mean'),
        taxa_atraso=('flag_atraso', 'mean'),
        customer_region=('customer_region', 'first')
    ).reset_index()
    estado_stats['taxa_atraso_pct'] = estado_stats['taxa_atraso'] * 100

    # ── KPI BANNER (Baseado nos dados filtrados) ──────────────────────────────
    top_revenue_state = estado_stats.nlargest(1, 'receita_liquida').iloc[0]
    top_freight_state = estado_stats.nlargest(1, 'freight_value').iloc[0]
    worst_delay_state = estado_stats.nlargest(1, 'taxa_atraso').iloc[0]

    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Receita (Filtro)", f"R$ {estado_stats['receita_liquida'].sum()/1e6:.1f}M")
    k2.metric(f"Líder de GMV: {top_revenue_state['customer_state']}", f"R$ {top_revenue_state['receita_liquida']/1e6:.1f}M")
    k3.metric(f"Frete Médio: {estado_stats['freight_value'].mean():.2f}", f"R$ {top_freight_state['freight_value']:.2f} (Max)")
    k4.metric("Taxa de Atraso Médio", f"{estado_stats['taxa_atraso_pct'].mean():.1f}%", delta=f"{worst_delay_state['taxa_atraso_pct']:.1f}% (Max)", delta_color="inverse")

    st.markdown("---")

    # ── GRÁFICO 1 & 2: FATURAMENTO vs CUSTO LOGÍSTICO ────────────────────────
    st.markdown("### Faturamento vs Custo Logístico por UF")
    st.markdown("<span style='font-family:\"DM Sans\",sans-serif; color:#888; font-size:0.9rem;'>Os mercados mais consolidados (Sudeste) operam com logística otimizada, enquanto o crescimento em novas fronteiras é penalizado pelo frete.</span>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        fig_rev = px.bar(
            estado_stats.sort_values('receita_liquida', ascending=False),
            x='customer_state', y='receita_liquida',
            labels={'receita_liquida': 'Receita Total (R$)', 'customer_state': 'Estado'},
            color='receita_liquida', color_continuous_scale='Viridis',
            hover_data={'num_pedidos': ':,', 'freight_value': ':.2f', 'review_score': ':.2f'},
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
            hover_data={'num_pedidos': ':,', 'tempo_entrega_real': ':.1f', 'taxa_atraso_pct': ':.1f'},
            title="Custo Médio de Frete por UF"
        )
        fig_freight.update_layout(**PLOTLY_LAYOUT)
        st.plotly_chart(fig_freight, use_container_width=True)

    st.markdown("---")


    # ── GRÁFICO 4: TAXA DE ATRASO POR ESTADO ────────────────────────────────
    st.markdown("### Taxa de Atraso por Estado")
    st.markdown("<span style='font-family:\"DM Sans\",sans-serif; color:#888; font-size:0.9rem;'>Estados distantes do eixo logístico concentram as maiores taxas de atraso — e as piores avaliações.</span>", unsafe_allow_html=True)

    # Insight: estados com maior taxa de atraso = menores notas de review
    fig_delay = px.bar(
        estado_stats.sort_values('taxa_atraso_pct', ascending=False),
        x='customer_state', y='taxa_atraso_pct',
        color='review_score',
        color_continuous_scale='RdYlGn',
        range_color=[2.5, 5.0],
        hover_data={'review_score': ':.2f', 'freight_value': ':.2f', 'num_pedidos': ':,'},
        labels={
            'taxa_atraso_pct': '% de Pedidos Atrasados',
            'customer_state': 'Estado',
            'review_score': 'Nota Média'
        },
        title="% de Pedidos com Atraso por UF (cor = satisfação)"
    )
    fig_delay.update_layout(**PLOTLY_LAYOUT)
    st.plotly_chart(fig_delay, use_container_width=True)

    st.markdown("---")

    # ── GRÁFICO 5: CATEGORIA CARRO-CHEFE POR ESTADO ─────────────────────────
    st.markdown("### Produto Carro-Chefe por Estado")
    st.markdown("<span style='font-family:\"DM Sans\",sans-serif; color:#888; font-size:0.9rem;'>O que cada região compra mais? Identificar o produto-chefe por UF permite otimizar estoques regionais.</span>", unsafe_allow_html=True)

    if 'product_category_name' in df_clean.columns:
        top_categorias = df_clean.groupby(['customer_state', 'product_category_name']).size().reset_index(name='total_pedidos')
        top_categorias = top_categorias.sort_values(['customer_state', 'total_pedidos'], ascending=[True, False])
        top_1_por_estado = top_categorias.drop_duplicates(subset=['customer_state'], keep='first')

        fig_cat = px.bar(
            top_1_por_estado.sort_values('total_pedidos', ascending=True),
            x='total_pedidos', y='customer_state',
            color='product_category_name',
            orientation='h',
            hover_data={'total_pedidos': ':,', 'product_category_name': True},
            title="Categoria Mais Vendida por Estado",
            color_discrete_sequence=ACCENT_COLORS,
            labels={'total_pedidos': 'Total de Pedidos', 'customer_state': 'Estado', 'product_category_name': 'Categoria'}
        )
        fig_cat.update_layout(**PLOTLY_LAYOUT, height=600)
        st.plotly_chart(fig_cat, use_container_width=True)

        with st.expander("📋 Ver Tabela Completa"):
            top_1_por_estado.columns = ['Estado', 'Categoria Mais Vendida', 'Total de Pedidos']
            st.dataframe(top_1_por_estado.reset_index(drop=True), use_container_width=True, hide_index=True)


else:
    st.warning("Dados não disponíveis.")
