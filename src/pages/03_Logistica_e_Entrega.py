import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from utils import get_analytical_df

st.set_page_config(page_title="Logística - Olist", page_icon="🚚", layout="wide")

st.title("🚚 Performance Logística e Last-Mile")

df = get_analytical_df()

if not df.empty:
    st.markdown("""
    ### ⏱️ O Tempo é Dinheiro (e Avaliação)
    Analisamos aqui o tempo real de entrega e como ele impacta diretamente a percepção do cliente.
    """)

    # Filtrando apenas pedidos entregues para análise de tempo
    df_del = df[df['order_status'] == 'delivered'].copy()

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Distribuição do Tempo de Entrega Real")
        fig_hist = px.histogram(df_del, x="tempo_entrega_real", 
                               nbins=50, title="Frequência de Prazos (Dias)",
                               labels={'tempo_entrega_real': 'Dias para Entrega'},
                               color_discrete_sequence=['#636EFA'])
        fig_hist.update_layout(xaxis_range=[0, 45])
        st.plotly_chart(fig_hist, width="stretch")

    with col2:
        st.subheader("Taxa de Atraso por Estado")
        delay_by_state = df_del.groupby('customer_state')['flag_atraso'].mean().sort_values(ascending=False).reset_index()
        fig_delay = px.bar(delay_by_state, x='customer_state', y='flag_atraso',
                          labels={'flag_atraso': '% Atraso', 'customer_state': 'Estado'},
                          color='flag_atraso', color_continuous_scale='Reds')
        st.plotly_chart(fig_delay, width="stretch")

    st.divider()

    st.subheader("⭐ O Impacto do Atraso na Satisfação")
    st.markdown("Pedidos com atraso têm notas significativamente menores. O gráfico abaixo compara a média de `review_score` para pedidos no prazo vs atrasados.")
    
    sat_analysis = df_del.groupby('flag_atraso')['review_score'].mean().reset_index()
    sat_analysis['Status'] = sat_analysis['flag_atraso'].map({0: 'No Prazo', 1: 'Com Atraso'})
    
    fig_sat = px.bar(sat_analysis, x='Status', y='review_score', 
                    color='Status', color_discrete_map={'No Prazo': 'green', 'Com Atraso': 'red'},
                    text_auto='.2f', title="Média de Avaliação por Status de Entrega")
    st.plotly_chart(fig_sat, width="stretch")

    st.divider()

    st.subheader("⚡ Eficiência: Postagem vs Transporte")
    st.markdown("Qual etapa consome mais tempo no ciclo de entrega?")
    
    # Calculando tempos médios
    df_del['tempo_postagem'] = (df_del['order_delivered_carrier_date'] - df_del['order_approved_at']).dt.days
    df_del['tempo_transporte'] = (df_del['order_delivered_customer_date'] - df_del['order_delivered_carrier_date']).dt.days

    metrics_df = pd.DataFrame({
        'Etapa': ['Postagem (Vendedor)', 'Transporte (Logística)'],
        'Média de Dias': [df_del['tempo_postagem'].mean(), df_del['tempo_transporte'].mean()]
    })
    
    fig_comp = px.pie(metrics_df, values='Média de Dias', names='Etapa', 
                     hole=.4, color_discrete_sequence=px.colors.qualitative.Pastel)
    st.plotly_chart(fig_comp, width="stretch")

    st.info("💡 **Conclusão:** Atrasos de entrega são o principal detrator do NPS. Reduzir o tempo de transporte em estados como AL e MA (com maiores taxas de atraso) é crítico para melhorar a retenção de clientes.")

    st.divider()

    # --- Nova Seção: Correlação Frete vs Velocidade ---
    st.subheader("💸 Pagar mais caro garante entrega mais rápida?")
    st.markdown("Investigamos a relação entre o `valor do frete` e o `tempo de entrega real`. Em um cenário ideal, haveria uma correlação negativa (frete caro = entrega rápida).")

    # Amostragem para evitar lentidão no gráfico de dispersão
    df_sample = df_del.sample(n=min(5000, len(df_del)))
    
    fig_corr = px.scatter(df_sample, x="freight_value", y="tempo_entrega_real",
                         trendline="ols", title="Correlação: Valor do Frete vs Dias de Entrega",
                         labels={'freight_value': 'Valor do Frete (R$)', 'tempo_entrega_real': 'Dias de Entrega'},
                         opacity=0.5, color_discrete_sequence=['orange'])
    st.plotly_chart(fig_corr, width="stretch")

    st.markdown("""
    **Observação Crítica:**
    A linha de tendência (OLS) mostra uma correlação fraca. Isso sugere que o custo do frete no Olist é mais influenciado pela **distância geográfica** do que pela **modalidade de urgência** (express vs standard).
    """)

    st.divider()

    # --- Nova Seção: Evolução Temporal da Logística ---
    st.subheader("📅 Evolução da Eficiência Logística")
    st.markdown("Como a performance de entrega se comportou ao longo do tempo?")

    logistic_timeline = df_del.groupby('ano_mes').agg(
        prazo_medio=('tempo_entrega_real', 'mean'),
        atraso_rate=('flag_atraso', 'mean')
    ).reset_index()

    fig_log_line = go.Figure()
    fig_log_line.add_trace(go.Scatter(x=logistic_timeline['ano_mes'], y=logistic_timeline['prazo_medio'],
                                    mode='lines+markers', name='Prazo Médio (Dias)',
                                    line=dict(color='blue', width=3)))
    
    fig_log_line.add_trace(go.Scatter(x=logistic_timeline['ano_mes'], y=logistic_timeline['atraso_rate'],
                                    mode='lines+markers', name='Taxa de Atraso (%)',
                                    line=dict(color='red', dash='dot'), yaxis='y2'))

    fig_log_line.update_layout(
        title="Prazo Médio vs Taxa de Atraso por Mês",
        xaxis_title="Mês",
        yaxis=dict(title="Dias Médios"),
        yaxis2=dict(title="Taxa de Atraso (%)", overlaying='y', side='right', showgrid=False),
        legend=dict(x=0.01, y=0.99)
    )
    st.plotly_chart(fig_log_line, width="stretch")

    st.warning("⚠️ **Alerta Operacional:** Note que em períodos de alta (como Nov/2017), a taxa de atraso tende a subir drasticamente, indicando gargalos estruturais na rede de transportadoras parceiras durante picos de demanda.")
else:
    st.warning("Dados não disponíveis.")
