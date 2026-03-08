import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from style_utils import inject_global_css, render_sidebar_logo, page_header, problema_box, insight_box, proposta_box, PLOTLY_LAYOUT, ACCENT_COLORS
from utils import get_analytical_df

st.set_page_config(page_title="Olist - O peso do Atraso", page_icon=os.path.join(os.path.dirname(__file__), "..", "public", "Radar.svg"), layout="wide")
inject_global_css()
render_sidebar_logo()

page_header("🚚 Performance Logística e Last-Mile", "O tempo é o principal detrator de qualidade percebida")

problema_box("Pedidos entregues com atraso têm nota média de <strong>2.1/5</strong> vs <strong>4.2/5</strong> para pedidos pontuais — uma queda de 50% no NPS. Em períodos de pico (Black Friday), a taxa de atraso salta de forma expressiva, evidenciando que a malha logística opera no limite da capacidade.")

df = get_analytical_df()
if not df.empty:
    df_del = df[df['order_status'] == 'delivered'].copy()

    st.markdown("---")
    st.markdown("### ⏱️ Distribuição e Gargalos de Prazo")

    col1, col2 = st.columns(2)
    with col1:
        fig_hist = px.histogram(
            df_del, x="tempo_entrega_real", nbins=50,
            labels={'tempo_entrega_real': 'Dias para Entrega', 'count': 'Frequência'},
            color_discrete_sequence=['#6c63ff']
        )
        fig_hist.update_layout(**PLOTLY_LAYOUT, title="Distribuição do Tempo de Entrega Real", xaxis_range=[0, 45])
        fig_hist.add_vline(x=df_del['tempo_entrega_real'].mean(), line_dash='dash', line_color='#ffd93d',
                           annotation_text=f"Média: {df_del['tempo_entrega_real'].mean():.1f}d", annotation_position="top right")
        st.plotly_chart(fig_hist, use_container_width=True)

    with col2:
        delay_by_state = df_del.groupby('customer_state')['flag_atraso'].mean().sort_values(ascending=False).reset_index()
        fig_delay = px.bar(
            delay_by_state, x='customer_state', y='flag_atraso',
            labels={'flag_atraso': '% de Pedidos com Atraso', 'customer_state': 'Estado'},
            color='flag_atraso', color_continuous_scale='Reds',
            title="Taxa de Atraso por Estado"
        )
        fig_delay.update_layout(**PLOTLY_LAYOUT)
        fig_delay.update_traces(texttemplate='%{y:.1%}', textposition='outside')
        st.plotly_chart(fig_delay, use_container_width=True)

    st.markdown("---")
    st.markdown("### ⭐ Impacto do Atraso na Satisfação do Cliente")

    sat_analysis = df_del.groupby('flag_atraso')['review_score'].mean().reset_index()
    sat_analysis['Status'] = sat_analysis['flag_atraso'].map({0: '✅ No Prazo', 1: '❌ Com Atraso'})

    fig_sat = px.bar(
        sat_analysis, x='Status', y='review_score',
        color='Status',
        color_discrete_map={'✅ No Prazo': '#00c882', '❌ Com Atraso': '#ff5050'},
        text_auto='.2f',
        title="Média de Avaliação: Pontual vs Atrasado",
        labels={'review_score': 'Nota Média (1-5)', 'Status': ''}
    )
    fig_sat.update_layout(**PLOTLY_LAYOUT, showlegend=False)
    fig_sat.update_traces(textfont_size=16, textposition='outside')
    st.plotly_chart(fig_sat, use_container_width=True)

    insight_box(f"A diferença entre entregar no prazo e com atraso é de <strong>{sat_analysis[sat_analysis['flag_atraso']==0]['review_score'].values[0] - sat_analysis[sat_analysis['flag_atraso']==1]['review_score'].values[0]:.2f} pontos na avaliação</strong> — equivalente à diferença entre um promotor e um detrator de marca.")

    st.markdown("---")
    st.markdown("### ⚡ Onde o Tempo é Perdido? Postagem vs Transporte")

    df_del['tempo_postagem'] = (df_del['order_delivered_carrier_date'] - df_del['order_approved_at']).dt.days
    df_del['tempo_transporte'] = (df_del['order_delivered_customer_date'] - df_del['order_delivered_carrier_date']).dt.days

    metrics_df = pd.DataFrame({
        'Etapa': ['Responsabilidade do Vendedor\n(Aprovação → Postagem)', 'Responsabilidade da Transportadora\n(Postagem → Entrega)'],
        'Média de Dias': [df_del['tempo_postagem'].mean(), df_del['tempo_transporte'].mean()]
    })

    fig_comp = px.pie(
        metrics_df, values='Média de Dias', names='Etapa',
        hole=0.5, color_discrete_sequence=['#6c63ff', '#ff6b6b'],
        title="Composição do Tempo Total de Entrega"
    )
    fig_comp.update_layout(**PLOTLY_LAYOUT)
    fig_comp.update_traces(textinfo='percent+label', textfont_size=11)
    st.plotly_chart(fig_comp, use_container_width=True)

    st.markdown("---")
    st.markdown("### 📅 Evolução Temporal da Eficiência Logística")

    logistic_timeline = df_del.groupby('ano_mes').agg(
        prazo_medio=('tempo_entrega_real', 'mean'),
        atraso_rate=('flag_atraso', 'mean')
    ).reset_index()

    fig_log = go.Figure()
    fig_log.add_trace(go.Scatter(
        x=logistic_timeline['ano_mes'], y=logistic_timeline['prazo_medio'],
        mode='lines+markers', name='Prazo Médio (Dias)',
        line=dict(color='#6c63ff', width=3), fill='tozeroy',
        fillcolor='rgba(108,99,255,0.1)'
    ))
    fig_log.add_trace(go.Scatter(
        x=logistic_timeline['ano_mes'], y=logistic_timeline['atraso_rate'] * 100,
        mode='lines+markers', name='Taxa de Atraso (%)',
        line=dict(color='#ff5050', dash='dot', width=2),
        yaxis='y2'
    ))
    fig_log.update_layout(
        **PLOTLY_LAYOUT,
        title="Prazo Médio vs Taxa de Atraso ao Longo do Tempo",
        xaxis_title="Mês",
        yaxis=dict(title="Dias Médios", gridcolor='rgba(108,99,255,0.15)'),
        yaxis2=dict(title="Taxa de Atraso (%)", overlaying='y', side='right', showgrid=False),
        hovermode='x unified'
    )
    st.plotly_chart(fig_log, use_container_width=True)

    proposta_box("1. <strong>SLA de Postagem</strong>: Penalizar vendedores que ultrapassam 2 dias para postar após aprovação. 2. <strong>Hubs Regionais</strong>: Reduzir distância percorrida pelas transportadoras no Norte/Nordeste. 3. <strong>Modelo Preditivo de Atraso</strong>: Avisar clientes proativamente, reduzindo o impacto no NPS.")
else:
    st.warning("Dados não disponíveis.")
