import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils import get_analytical_df, treat_outliers_iqr

st.set_page_config(page_title="Financeiro - Olist", page_icon="💰", layout="wide")

st.title("💰 Financeiro e Pagamentos")

df = get_analytical_df()

if not df.empty:
    # --- Limpeza de Outliers para KPIs Preciso ---
    # Usando receita_liquida (price + freight) conforme notebook do Samuel
    df_clean = treat_outliers_iqr(df, 'receita_liquida')
    
    # KPIs Principais
    total_revenue = df_clean['receita_liquida'].sum()
    total_orders = df_clean['order_id'].nunique()
    avg_ticket = total_revenue / total_orders
    
    col_kpi1, col_kpi2, col_kpi3 = st.columns(3)
    col_kpi1.metric("Faturamento Total (Limpo)", f"R$ {total_revenue:,.2f}", help="Soma de price + freight após remoção de outliers via IQR.")
    col_kpi2.metric("Ticket Médio", f"R$ {avg_ticket:,.2f}", help="Receita total dividida pelo número de pedidos únicos.")
    col_kpi3.metric("Volume de Pedidos", f"{total_orders:,}")

    st.divider()

    # --- Análise de Parcelamento ---
    st.markdown("### 💳 Impacto do Parcelamento no Ticket Médio")
    st.info("Investigamos se o número de parcelas influencia o valor gasto pelo cliente. Conforme os dados, compras parceladas tendem a ter tickets significativamente maiores.")

    # Agregando por parcelas
    installments_analysis = df_clean.groupby('payment_installments').agg(
        volume_pedidos=('order_id', 'nunique'),
        ticket_medio=('receita_liquida', 'mean')
    ).reset_index()
    
    # Filtro para evitar ruído de parcelas raras (ex: > 12)
    installments_analysis = installments_analysis[installments_analysis['payment_installments'] <= 12]

    fig_dual = go.Figure()

    # Barras: Volume de Pedidos
    fig_dual.add_trace(go.Bar(
        x=installments_analysis['payment_installments'],
        y=installments_analysis['volume_pedidos'],
        name='Volume de Pedidos',
        marker_color='royalblue',
        yaxis='y1'
    ))

    # Linha: Ticket Médio
    fig_dual.add_trace(go.Scatter(
        x=installments_analysis['payment_installments'],
        y=installments_analysis['ticket_medio'],
        name='Ticket Médio (R$)',
        mode='lines+markers',
        line=dict(color='firebrick', width=3),
        yaxis='y2'
    ))

    fig_dual.update_layout(
        title="Volume de Pedidos vs Ticket Médio por Parcelas",
        xaxis=dict(title="Número de Parcelas"),
        yaxis=dict(title="Volume de Pedidos", side='left'),
        yaxis2=dict(title="Ticket Médio (R$)", side='right', overlaying='y', showgrid=False),
        legend=dict(x=1.1, y=1),
        hovermode="x unified"
    )
    st.plotly_chart(fig_dual, width="stretch")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Distribuição por Tipo de Pagamento")
        pay_type = df_clean['payment_type'].value_counts().reset_index()
        pay_type.columns = ['Tipo', 'Quantidade']
        fig_pay = px.pie(pay_type, values='Quantidade', names='Tipo', hole=0.4,
                         color_discrete_sequence=px.colors.qualitative.Pastel)
        st.plotly_chart(fig_pay, width="stretch")

    with col2:
        st.subheader("Top 10 Categorias por Faturamento")
        cat_rev = df_clean.groupby('product_category_name')['receita_liquida'].sum().sort_values(ascending=False).head(10).reset_index()
        fig_cat = px.bar(cat_rev, x='receita_liquida', y='product_category_name', orientation='h',
                        color='receita_liquida', color_continuous_scale='Viridis',
                        labels={'receita_liquida': 'Receita (R$)', 'product_category_name': 'Categoria'})
        st.plotly_chart(fig_cat, width="stretch")

    st.info("💡 **Insight de Negócio:** Compras em 1x (à vista) representam o maior volume, porém o ticket médio aumenta linearmente com o número de parcelas. Incentivar o parcelamento para categorias de alto valor ('relogios_presentes', 'eletroportateis') é uma estratégia clara para elevar o faturamento total.")

    st.divider()

    # --- Análise Temporal e Eventos ---
    st.subheader("📈 Evolução da Receita e Picos de Demanda")
    st.markdown("A série temporal revela o crescimento explosivo da plataforma e o impacto massivo de eventos promocionais.")

    # Agregando por mês
    timeline = df_clean.groupby('ano_mes').agg(
        receita=('receita_liquida', 'sum'),
        pedidos=('order_id', 'nunique')
    ).reset_index()
    timeline = timeline.sort_values('ano_mes')

    fig_timeline = go.Figure()

    fig_timeline.add_trace(go.Scatter(
        x=timeline['ano_mes'], y=timeline['receita'],
        mode='lines+markers', name='Receita Mensal',
        line=dict(color='#1f77b4', width=4),
        fill='tozeroy'
    ))

    # Destaque Black Friday 2017
    bf_2017 = timeline[timeline['ano_mes'] == '2017-11']
    if not bf_2017.empty:
        fig_timeline.add_annotation(
            x='2017-11', y=bf_2017['receita'].values[0],
            text="🔥 Black Friday 2017<br>Pico Histórico de Faturamento",
            showarrow=True, arrowhead=1,
            bgcolor="rgba(255, 0, 0, 0.5)",
            bordercolor="red",
            borderwidth=1,
            borderpad=4
        )

    fig_timeline.update_layout(
        title="Receita Líquida Mensal (IQR Cleaned)",
        xaxis_title="Ano-Mês",
        yaxis_title="Receita (R$)",
        hovermode="x unified"
    )
    st.plotly_chart(fig_timeline, width="stretch")

    st.markdown("""
    **Análise Técnica Temporária:**
    1. **Novembro/2017**: O faturamento saltou drasticamente devido à Black Friday, validando a capacidade de escala da operação.
    2. **Tendência de Alta**: Observa-se um crescimento orgânico sustentado pós-evento, indicando retenção de novos clientes atraídos pela promoção.
    3. **Sazonalidade Varejista**: Picos menores em Maio (Dia das Mães) e Dezembro (Natal) são visíveis, mas a BF domina a estratégia de volume.
    """)
else:
    st.warning("Dados não carregados. Verifique a fonte de dados.")
