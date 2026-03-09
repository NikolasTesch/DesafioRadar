import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from style_utils import inject_global_css, render_sidebar_logo, page_header, problema_box, insight_box, proposta_box, PLOTLY_LAYOUT, ACCENT_COLORS
from utils import get_analytical_df, treat_outliers_iqr

st.set_page_config(page_title="Olist - O peso do Atraso", page_icon=os.path.join(os.path.dirname(__file__), "..", "public", "Radar.svg"), layout="wide")
inject_global_css()
render_sidebar_logo()

page_header("💰 Financeiro e Análise de Pagamentos", "GMV, ticket médio e comportamento de compra")

problema_box("O faturamento total bruto mascara uma realidade complexa: outliers inflam o ticket médio, compras parceladas têm comportamento radicalmente distinto das à vista, e categorias de alto valor são sub-exploradas do ponto de vista de incentivos de parcelamento.")

df = get_analytical_df()
if not df.empty:
    df_clean = treat_outliers_iqr(df, 'receita_liquida')
    total_revenue = df_clean['receita_liquida'].sum()
    total_orders = df_clean['order_id'].nunique()
    avg_ticket = total_revenue / total_orders

    col1, col2, col3 = st.columns(3)
    col1.metric("💵 GMV Total (Saneado)", f"R$ {total_revenue/1e6:.1f}M")
    col2.metric("🧾 Ticket Médio", f"R$ {avg_ticket:.2f}")
    col3.metric("📦 Pedidos Analisados", f"{total_orders:,}")

    st.markdown("---")
    st.markdown("### 💳 Impacto do Parcelamento no Ticket Médio")
    st.markdown("Compras parceladas tendem a ter ticket significativamente maior. Explorar isso estrategicamente é crescimento sem aquisição de novos clientes.")

    installments_analysis = df_clean.groupby('payment_installments').agg(
        volume_pedidos=('order_id', 'nunique'),
        ticket_medio=('receita_liquida', 'mean')
    ).reset_index()
    installments_analysis = installments_analysis[installments_analysis['payment_installments'] <= 12]

    fig_dual = go.Figure()
    fig_dual.add_trace(go.Bar(
        x=installments_analysis['payment_installments'],
        y=installments_analysis['volume_pedidos'],
        name='Volume de Pedidos', marker_color='#6c63ff', yaxis='y1'
    ))
    fig_dual.add_trace(go.Scatter(
        x=installments_analysis['payment_installments'],
        y=installments_analysis['ticket_medio'],
        name='Ticket Médio (R$)', mode='lines+markers',
        line=dict(color='#ffd93d', width=3), yaxis='y2'
    ))
    _layout = {k: v for k, v in PLOTLY_LAYOUT.items() if k not in ("xaxis", "yaxis")}
    fig_dual.update_layout(
        **_layout,
        title="Volume vs Ticket Médio por Número de Parcelas",
        xaxis=dict(
            title="Parcelas",
            gridcolor="rgba(108,99,255,0.15)",
            zerolinecolor="rgba(108,99,255,0.2)",
        ),
        yaxis=dict(
            title="Volume de Pedidos", side="left", gridcolor="rgba(108,99,255,0.15)"
        ),
        yaxis2=dict(
            title="Ticket Médio (R$)", side="right", overlaying="y", showgrid=False
        ),
        hovermode="x unified",
        barmode="overlay",
    )
    st.plotly_chart(fig_dual, use_container_width=True)

    insight_box("Compras em 10x têm ticket médio aproximadamente <strong>3x maior</strong> que compras à vista. Contudo, 60%+ do volume é gerado por pagamentos à vista — indicando oportunidade clara de incentivo ao parcelamento.")

    st.markdown("---")
    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown("### 💳 Mix de Meios de Pagamento")
        pay_type = df_clean['payment_type'].value_counts().reset_index()
        pay_type.columns = ['Tipo', 'Quantidade']
        fig_pay = px.pie(pay_type, values='Quantidade', names='Tipo', hole=0.5,
                         color_discrete_sequence=ACCENT_COLORS,
                         title="Distribuição por Tipo de Pagamento")
        fig_pay.update_layout(**PLOTLY_LAYOUT)
        fig_pay.update_traces(textinfo='percent+label')
        st.plotly_chart(fig_pay, use_container_width=True)

    with col_b:
        st.markdown("### 🏆 Top 10 Categorias por Faturamento")
        cat_rev = df_clean.groupby('product_category_name')['receita_liquida'].sum().sort_values(ascending=False).head(10).reset_index()
        fig_cat = px.bar(cat_rev, x='receita_liquida', y='product_category_name', orientation='h',
                         color='receita_liquida', color_continuous_scale='Viridis',
                         labels={'receita_liquida': 'Receita Total (R$)', 'product_category_name': 'Categoria'},
                         title="Categorias por GMV")
        fig_cat.update_layout(**PLOTLY_LAYOUT)
        st.plotly_chart(fig_cat, use_container_width=True)

    st.markdown("---")
    st.markdown("### 📈 Evolução Temporal da Receita (com destaque Black Friday)")

    timeline = df_clean.groupby('ano_mes').agg(
        receita=('receita_liquida', 'sum'), pedidos=('order_id', 'nunique')
    ).reset_index().sort_values('ano_mes')

    fig_tl = go.Figure()
    fig_tl.add_trace(go.Scatter(
        x=timeline['ano_mes'], y=timeline['receita'],
        mode='lines+markers', name='Receita Mensal',
        line=dict(color='#6c63ff', width=3),
        fill='tozeroy', fillcolor='rgba(108,99,255,0.15)'
    ))
    bf = timeline[timeline['ano_mes'] == '2017-11']
    if not bf.empty:
        fig_tl.add_annotation(
            x='2017-11', y=bf['receita'].values[0],
            text="🖤 Black Friday 2017<br>Pico Histórico",
            showarrow=True, arrowhead=2, arrowcolor='#ffd93d',
            bgcolor='rgba(255,80,0,0.7)', font=dict(color='white', size=11),
            bordercolor='#ffd93d', borderwidth=1, borderpad=6
        )
    _layout_tl = {k: v for k, v in PLOTLY_LAYOUT.items() if k not in ("xaxis", "yaxis")}
    fig_tl.update_layout(
        **_layout_tl,
        title="Receita Líquida Mensal",
        xaxis_title="Período",
        yaxis_title="Receita (R$)",
        hovermode="x unified",
    )
    st.plotly_chart(fig_tl, use_container_width=True)

    proposta_box("""
    1. <strong>Campanhas de Parcelamento Sem Juros</strong> para categorias de alto valor (Eletrônicos, Relógios). <br><br>
    2. <strong>Incentivo ao Cartão de Crédito</strong> via cashback — hoje sub-representado vs boleto. <br><br>
    3. <strong>Estratégia de Q4</strong>: Black Friday + pré-Natal como janela principal de push de volume, com infraestrutura logística reforçada.
""")
else:
    st.warning("Dados não carregados.")
