import streamlit as st
import plotly.express as px
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from style_utils import inject_global_css, render_sidebar_logo, page_header, problema_box, insight_box, proposta_box, PLOTLY_LAYOUT
from utils import get_analytical_df

st.set_page_config(page_title="Olist - O peso do Atraso", page_icon=os.path.join(os.path.dirname(__file__), "..", "public", "Radar.svg"), layout="wide")
inject_global_css()
render_sidebar_logo()

page_header("📅 Tendências e Sazonalidade", "O pulso temporal do e-commerce e o fenômeno Black Friday")

problema_box("A operação não é linear. Picos de demanda concentrados em eventos pontuais (Black Friday, Dia das Mães, Natal) sobrecarregam a logística de forma imprevisível. Sem planejamento sazonal, atrasos e insatisfação disparam justamente quando o volume e a expectativa estão no máximo.")

df = get_analytical_df()
if not df.empty:
    st.markdown("---")
    st.markdown("### 📈 Série Temporal de Faturamento")
    sales_trend = df.groupby('ano_mes')['receita_liquida'].sum().reset_index().sort_values('ano_mes')
    fig_line = px.line(
        sales_trend, x='ano_mes', y='receita_liquida',
        labels={'receita_liquida': 'Receita (R$)', 'ano_mes': 'Mês/Ano'},
        markers=True, title="Crescimento Mensal: Receita Líquida",
        color_discrete_sequence=['#00c882']
    )
    fig_line.update_traces(line_width=3, marker_size=8)
    fig_line.update_layout(**PLOTLY_LAYOUT)
    st.plotly_chart(fig_line, use_container_width=True)

    st.markdown("---")
    col1, col2 = st.columns(2)

    with col1:
        day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        pt_days = {'Monday': 'Segunda', 'Tuesday': 'Terça', 'Wednesday': 'Quarta',
                   'Thursday': 'Quinta', 'Friday': 'Sexta', 'Saturday': 'Sábado', 'Sunday': 'Domingo'}
        sales_day = df.groupby('dia_semana')['receita_liquida'].sum().reindex(day_order).reset_index()
        sales_day['dia_semana'] = sales_day['dia_semana'].map(pt_days)
        fig_day = px.bar(
            sales_day, x='dia_semana', y='receita_liquida',
            color='receita_liquida', color_continuous_scale='Greens',
            labels={'receita_liquida': 'Faturamento (R$)', 'dia_semana': 'Dia da Semana'},
            title="Concentração por Dia da Semana"
        )
        fig_day.update_layout(**PLOTLY_LAYOUT)
        st.plotly_chart(fig_day, use_container_width=True)

    with col2:
        sales_hour = df.groupby('hora_compra')['receita_liquida'].count().reset_index()
        sales_hour.columns = ['Hora', 'Volume de Pedidos']
        fig_hour = px.area(
            sales_hour, x='Hora', y='Volume de Pedidos',
            title="Picos de Acesso por Hora do Dia",
            color_discrete_sequence=['#6c63ff']
        )
        fig_hour.update_layout(**PLOTLY_LAYOUT)
        fig_hour.update_traces(fillcolor='rgba(108,99,255,0.2)')
        st.plotly_chart(fig_hour, use_container_width=True)

    insight_box("As compras concentram-se entre <strong>10h e 16h, de segunda a sexta</strong>. Esse padrão sugere um consumidor que compra durante o trabalho — um janela de oportunidade precisa para Ads e Push Notifications.")

    st.markdown("---")
    st.markdown("### 🗓️ Sazonalidade Mensal Acumulada")

    df_copy = df.copy()
    df_copy['mes_nome'] = df_copy['order_purchase_timestamp'].dt.month_name()
    month_order = ['January', 'February', 'March', 'April', 'May', 'June',
                   'July', 'August', 'September', 'October', 'November', 'December']
    pt_months = {'January': 'Jan', 'February': 'Fev', 'March': 'Mar', 'April': 'Abr',
                 'May': 'Mai', 'June': 'Jun', 'July': 'Jul', 'August': 'Ago',
                 'September': 'Set', 'October': 'Out', 'November': 'Nov', 'December': 'Dez'}

    sales_month = df_copy.groupby('mes_nome')['receita_liquida'].sum().reindex(month_order).reset_index()
    sales_month['mes_nome'] = sales_month['mes_nome'].map(pt_months)

    colors = ['#ff6b6b' if m == 'Nov' else '#6c63ff' for m in sales_month['mes_nome']]
    fig_month = px.bar(
        sales_month, x='mes_nome', y='receita_liquida',
        labels={'receita_liquida': 'Faturamento (R$)', 'mes_nome': 'Mês'},
        title="Sazonalidade Mensal Acumulada", text_auto=',.0f'
    )
    fig_month.update_traces(marker_color=colors, textposition='outside')
    fig_month.update_layout(**PLOTLY_LAYOUT)

    nov_val = sales_month[sales_month['mes_nome'] == 'Nov']['receita_liquida'].values
    if len(nov_val) > 0:
        fig_month.add_annotation(
            x='Nov', y=nov_val[0],
            text="🖤 Black Friday", showarrow=True, arrowhead=2, arrowcolor='#ffd93d',
            bgcolor='rgba(0,0,0,0.7)', font=dict(color='#ffd93d', size=12),
            bordercolor='#ffd93d', borderwidth=1, borderpad=5, yshift=15
        )
    st.plotly_chart(fig_month, use_container_width=True)

    proposta_box("1. <strong>Campanhas Programadas</strong>: Investir em Ads entre 9h–15h nos dias úteis para maximizar ROAS. 2. <strong>Preparação Logística Antecipada</strong>: Ampliar estoque de transportadoras a partir de outubro para absorver o pico de final de ano. 3. <strong>Calendário Comercial</strong>: Criar calendário de eventos sazonais (Dia das Mães, Dia dos Pais, BF, Natal) como base para planejamento de SKUs e campanhas.")
else:
    st.warning("Dados não carregados.")
