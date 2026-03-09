import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from style_utils import inject_global_css, render_sidebar_logo, page_header, problema_box, insight_box, proposta_box, PLOTLY_LAYOUT, ACCENT_COLORS
from utils import get_analytical_df, treat_outliers_iqr

st.set_page_config(page_title="Olist - Financeiro", page_icon=os.path.join(os.path.dirname(__file__), "..", "public", "Radar.svg"), layout="wide")
inject_global_css()
render_sidebar_logo()

page_header("💰 Capítulo 4: O Custo Real do Problema", "GMV, ticket médio e o impacto financeiro dos gargalos")

# ── INTRO NARRATIVO ─────────────────────────────────────────────────────────────
st.markdown("""
<div style="background: rgba(108,99,255,0.07); border-left: 4px solid #6c63ff; border-radius: 0 12px 12px 0; padding: 1.2rem 1.5rem; margin-bottom: 1.5rem; font-family: 'DM Sans', sans-serif; color: #ccc; font-size: 0.95rem; line-height: 1.8;">
    Um cliente detrator custa mais para reativar do que um cliente promotor vale em compras repetidas.
    E enquanto a plataforma não incentiva o parcelamento em categorias de alto valor,
    está deixando um <strong>uplift de 20-25% no ticket médio</strong> na mesa — sem aquisição de nenhum novo cliente.
</div>
""", unsafe_allow_html=True)

problema_box("O faturamento bruto mascara a realidade: outliers inflam o ticket, o parcelamento é sub-explorado e categorias de alto valor carecem de incentivos para a conversão de pedidos maiores.")

df = get_analytical_df()
if not df.empty:
    df_clean = treat_outliers_iqr(df, 'receita_liquida')
    total_revenue = df_clean['receita_liquida'].sum()
    total_orders = df_clean['order_id'].nunique()
    avg_ticket = total_revenue / total_orders
    avg_freight_pct = (df_clean['freight_value'].mean() / df_clean['receita_liquida'].mean()) * 100

    # ── KPI BANNER ─────────────────────────────────────────────────────────────
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("💵 GMV Total (Saneado)", f"R$ {total_revenue/1e6:.1f}M")
    k2.metric("🧾 Ticket Médio", f"R$ {avg_ticket:.2f}")
    k3.metric("📦 Pedidos Únicos", f"{total_orders:,}")
    k4.metric("🚚 Frete como % do Ticket", f"{avg_freight_pct:.1f}%", delta="alto → impacto no NPS", delta_color="inverse")

    st.markdown("---")

    # ── GRÁFICO 1: PARCELAMENTO VS TICKET MÉDIO ───────────────────────────────
    st.markdown("### O Potencial Oculto do Parcelamento")
    st.markdown("<span style='font-family:\"DM Sans\",sans-serif; color:#888; font-size:0.9rem;'>Compras parceladas têm ticket significativamente maior. O gráfico revela a oportunidade: alto volume em 1x, alto valor em 10x — incentivo de crédito pode capturar os dois.</span>", unsafe_allow_html=True)

    installments_analysis = df_clean.groupby('payment_installments').agg(
        volume_pedidos=('order_id', 'nunique'),
        ticket_medio=('receita_liquida', 'mean'),
        frete_medio=('freight_value', 'mean')
    ).reset_index()
    installments_analysis = installments_analysis[(installments_analysis['payment_installments'] >= 1) & (installments_analysis['payment_installments'] <= 12)]

    _layout = {k: v for k, v in PLOTLY_LAYOUT.items() if k not in ("xaxis", "yaxis")}
    fig_dual = go.Figure()
    fig_dual.add_trace(go.Bar(
        x=installments_analysis['payment_installments'],
        y=installments_analysis['volume_pedidos'],
        name='Volume de Pedidos',
        marker_color='#6c63ff', yaxis='y1',
        hovertemplate='<b>%{x}x</b><br>Volume: %{y:,}<extra></extra>'
    ))
    fig_dual.add_trace(go.Scatter(
        x=installments_analysis['payment_installments'],
        y=installments_analysis['ticket_medio'],
        name='Ticket Médio (R$)', mode='lines+markers',
        line=dict(color='#ffd93d', width=3), yaxis='y2',
        hovertemplate='<b>%{x}x</b><br>Ticket Médio: R$ %{y:.2f}<extra></extra>'
    ))
    # Anotação mostrando o uplift de 10x vs 1x
    ticket_1x = installments_analysis[installments_analysis['payment_installments'] == 1]['ticket_medio'].values
    ticket_10x = installments_analysis[installments_analysis['payment_installments'] == 10]['ticket_medio'].values
    if len(ticket_1x) > 0 and len(ticket_10x) > 0:
        uplift = ticket_10x[0] / ticket_1x[0]
        fig_dual.add_annotation(
            x=10, y=ticket_10x[0],
            yref='y2', text=f"🚀 {uplift:.1f}x maior que 1x",
            showarrow=True, arrowhead=2, arrowcolor='#ffd93d',
            bgcolor='rgba(255,217,61,0.2)', font=dict(color='#ffd93d', size=11),
            bordercolor='#ffd93d', borderwidth=1, borderpad=5
        )
    fig_dual.update_layout(
        **_layout,
        title="Volume de Pedidos vs Ticket Médio por Número de Parcelas",
        xaxis=dict(title="Parcelas", gridcolor="rgba(108,99,255,0.15)"),
        yaxis=dict(title="Volume de Pedidos", side="left", gridcolor="rgba(108,99,255,0.15)"),
        yaxis2=dict(title="Ticket Médio (R$)", side="right", overlaying="y", showgrid=False),
        hovermode="x unified",
    )
    st.plotly_chart(fig_dual, use_container_width=True)

    insight_box("Compras parceladas em <strong>10x</strong> têm ticket médio aproximadamente <strong>3x maior</strong> que compras à vista. "
                "Contudo, a maioria dos pedidos é realizada à vista — demonstrando uma oportunidade clara de crescimento de GMV via incentivo de crédito sem aquisição de novos clientes.")

    st.markdown("---")
    col_a, col_b = st.columns(2)

    with col_a:
        # ── GRÁFICO 2: MIX DE PAGAMENTO ──────────────────────────────────────
        st.markdown("### Mix de Meios de Pagamento")
        pay_type = df_clean['payment_type'].value_counts().reset_index()
        pay_type.columns = ['Tipo', 'Quantidade']
        pay_type['Percentual'] = pay_type['Quantidade'] / pay_type['Quantidade'].sum() * 100
        fig_pay = px.pie(
            pay_type, values='Quantidade', names='Tipo', hole=0.55,
            color_discrete_sequence=ACCENT_COLORS,
            hover_data={'Percentual': ':.1f'},
            title="Distribuição por Tipo de Pagamento"
        )
        fig_pay.update_layout(**PLOTLY_LAYOUT)
        fig_pay.update_traces(textinfo='percent+label')
        st.plotly_chart(fig_pay, use_container_width=True)

    with col_b:
        # ── GRÁFICO 3: TOP 10 CATEGORIAS POR GMV ────────────────────────────
        st.markdown("### Top 10 Categorias por Faturamento")
        cat_rev = (df_clean.groupby('product_category_name')['receita_liquida']
                   .agg(['sum', 'count', 'mean']).sort_values('sum', ascending=False).head(10).reset_index())
        cat_rev.columns = ['Categoria', 'Receita Total', 'Pedidos', 'Ticket Médio']
        fig_cat = px.bar(
            cat_rev, x='Receita Total', y='Categoria', orientation='h',
            color='Ticket Médio', color_continuous_scale='RdYlGn',
            hover_data={'Pedidos': ':,', 'Ticket Médio': ':.2f', 'Receita Total': ':,.0f'},
            title="Categorias por GMV (cor = ticket médio)"
        )
        fig_cat.update_layout(**PLOTLY_LAYOUT)
        st.plotly_chart(fig_cat, use_container_width=True)

    st.markdown("---")

    # ── GRÁFICO 4: TICKET MÉDIO POR ESTADO ───────────────────────────────────
    st.markdown("### Desigualdade de Ticket Médio por Região")
    st.markdown("<span style='font-family:\"DM Sans\",sans-serif; color:#888; font-size:0.9rem;'>O poder de compra varia dramaticamente por estado. Estados com maior frete tendem a ter maior ticket médio — pois apenas compras de alto valor compensam o custo de frete.</span>", unsafe_allow_html=True)

    regional_ticket = df_clean.groupby('customer_state').agg(
        ticket_medio=('receita_liquida', 'mean'),
        frete_medio=('freight_value', 'mean'),
        pedidos=('order_id', 'count'),
        nota_media=('review_score', 'mean')
    ).reset_index()

    fig_regional = px.bar(
        regional_ticket.sort_values('ticket_medio', ascending=False),
        x='customer_state', y='ticket_medio',
        color='frete_medio', color_continuous_scale='YlOrRd',
        hover_data={'frete_medio': ':.2f', 'pedidos': ':,', 'nota_media': ':.2f'},
        labels={'ticket_medio': 'Ticket Médio (R$)', 'customer_state': 'Estado', 'frete_medio': 'Frete Médio'},
        title="Ticket Médio por Estado (cor = custo de frete)"
    )
    fig_regional.update_layout(**PLOTLY_LAYOUT)
    st.plotly_chart(fig_regional, use_container_width=True)

else:
    st.warning("Dados não carregados.")
