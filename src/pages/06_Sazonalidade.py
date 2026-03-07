import streamlit as st
import pandas as pd
import plotly.express as px
from utils import get_analytical_df

st.set_page_config(page_title="Sazonalidade - Olist", page_icon="📅", layout="wide")

st.title("📅 Tendências e Sazonalidade")

df = get_analytical_df()

if not df.empty:
    st.markdown("""
    ### 📈 O Pulso do Mercado
    Como as vendas se comportam ao longo do tempo? Identificamos picos de demanda e feriados comerciais.
    """)

    # Preparando dados temporais
    sales_trend = df.groupby('ano_mes')['receita_liquida'].sum().reset_index()
    sales_trend = sales_trend.sort_values('ano_mes')

    st.subheader("Série Temporal de Vendas (Faturamento Líquido)")
    fig_line = px.line(sales_trend, x='ano_mes', y='receita_liquida', 
                      labels={'receita_liquida': 'Receita (R$)', 'ano_mes': 'Mês/Ano'},
                      markers=True, title="Crescimento Mensal das Vendas",
                      color_discrete_sequence=['#2ecc71'])
    st.plotly_chart(fig_line, width="stretch")

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Vendas por Dia da Semana")
        day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        # Mapeando nomes para Português para melhor UX
        pt_days = {
            'Monday': 'Segunda', 'Tuesday': 'Terça', 'Wednesday': 'Quarta', 
            'Thursday': 'Quinta', 'Friday': 'Sexta', 'Saturday': 'Sábado', 'Sunday': 'Domingo'
        }
        
        sales_day = df.groupby('dia_semana')['receita_liquida'].sum().reindex(day_order).reset_index()
        sales_day['dia_semana'] = sales_day['dia_semana'].map(pt_days)
        
        fig_day = px.bar(sales_day, x='dia_semana', y='receita_liquida', 
                        color='receita_liquida', color_continuous_scale='Greens',
                        labels={'receita_liquida': 'Faturamento (R$)', 'dia_semana': 'Dia'},
                        title="Concentração de Compras por Dia")
        st.plotly_chart(fig_day, width="stretch")

    with col2:
        st.subheader("Concentração por Hora do Dia")
        sales_hour = df.groupby('hora_compra')['receita_liquida'].count().reset_index()
        sales_hour.columns = ['hora', 'volume_pedidos']
        
        # Plotando volume de pedidos (frequência) em vez de GMV para ver pico de acessos
        fig_hour = px.area(sales_hour, x='hora', y='volume_pedidos', 
                          labels={'volume_pedidos': 'Volume de Pedidos', 'hora': 'Hora do Dia'},
                          title="Picos de Acesso (Quantidade de Pedidos)",
                          color_discrete_sequence=['#3498db'])
        st.plotly_chart(fig_hour, width="stretch")

    st.info("💡 **Destaque:** As vendas concentram-se fortemente entre 10h e 16h em dias úteis. A queda significativa nos fins de semana sugere um perfil de consumidor B2B ou compras planejadas durante o horário de trabalho.")

    st.divider()

    st.subheader("🗓️ Visão Mensal e Eventos Críticos")
    st.markdown("Analisamos a distribuição de vendas por mês para identificar o 'batimento cardíaco' anual do e-commerce.")

    # Agregando por mês do ano (ignorando ano para ver sazonalidade sazonal)
    df['mes_nome'] = df['order_purchase_timestamp'].dt.month_name()
    month_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    pt_months = {
        'January': 'Jan', 'February': 'Fev', 'March': 'Mar', 'April': 'Abr',
        'May': 'Mai', 'June': 'Jun', 'July': 'Jul', 'August': 'Ago',
        'September': 'Set', 'October': 'Out', 'November': 'Nov', 'December': 'Dez'
    }

    sales_month = df.groupby('mes_nome')['receita_liquida'].sum().reindex(month_order).reset_index()
    sales_month['mes_nome'] = sales_month['mes_nome'].map(pt_months)

    fig_month = px.bar(sales_month, x='mes_nome', y='receita_liquida',
                      color='receita_liquida', color_continuous_scale='Blues',
                      labels={'receita_liquida': 'Faturamento (R$)', 'mes_nome': 'Mês'},
                      title="Sazonalidade Mensal Acumulada")
    
    # Destacando Novembro
    fig_month.add_annotation(x='Nov', y=sales_month[sales_month['mes_nome'] == 'Nov']['receita_liquida'].values[0],
                            text="🖤 Black Friday", showarrow=True, arrowhead=2, bgcolor="black", font=dict(color="white"))

    st.plotly_chart(fig_month, width="stretch")

    st.markdown("""
    ### 🕵️ O Fenômeno Black Friday
    Novembro se destaca como o mês de maior volume, impulsionado pela **Black Friday**. 
    * **Impacto Logístico:** Note que o aumento súbito de volume em novembro gera um stress na malha logística (conforme visto na página de Logística).
    * **Comportamento do Consumidor:** Há uma antecipação de compras de Natal, concentrando a receita do Q4 (quarto trimestre) quase inteiramente em um único evento.
    * **Oportunidade:** Categorias como 'Eletrônicos' e 'Relógios' dominam este período, exigindo estoque reforçado.
    """)
else:
    st.warning("Dados não carregados.")
