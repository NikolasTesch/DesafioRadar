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
    # Filtrar xaxis/yaxis do PLOTLY_LAYOUT para evitar conflito com kwargs explícitos
    _layout = {k: v for k, v in PLOTLY_LAYOUT.items() if k not in ("xaxis", "yaxis")}
    fig_log.update_layout(
        **_layout,
        title="Prazo Médio vs Taxa de Atraso ao Longo do Tempo",
        xaxis=dict(
            title="Mês",
            gridcolor="rgba(108,99,255,0.15)",
            zerolinecolor="rgba(108,99,255,0.2)",
        ),
        yaxis=dict(title="Dias Médios", gridcolor="rgba(108,99,255,0.15)"),
        yaxis2=dict(
            title="Taxa de Atraso (%)", overlaying="y", side="right", showgrid=False
        ),
        hovermode="x unified",
    )
    st.plotly_chart(fig_log, use_container_width=True)

    st.markdown("### 📦 Impacto das Dimensões no Custo de Frete")
    
    col_dims = ['product_weight_g', 'product_length_cm', 'product_height_cm', 'product_width_cm', 'freight_value']
    if all(col in df_del.columns for col in col_dims):
        # Criando coluna de volume (cm³)
        df_del['volume_cm3'] = df_del['product_length_cm'] * df_del['product_height_cm'] * df_del['product_width_cm']
        
        # Pegando uma amostra para o scatter plot não ficar muito pesado no Streamlit
        df_sample = df_del.dropna(subset=['volume_cm3', 'freight_value']).sample(n=min(5000, len(df_del)), random_state=42)
        
        fig_vol = px.scatter(
            df_sample, x='volume_cm3', y='freight_value', 
            trendline='ols',
            opacity=0.5,
            color_discrete_sequence=['#6c63ff'],
            labels={'volume_cm3': 'Volume do Pacote (cm³)', 'freight_value': 'Valor do Frete (R$)'},
            title="Correlação: Volume Cúbico vs Custo de Transporte"
        )
        fig_vol.update_layout(**PLOTLY_LAYOUT)
        st.plotly_chart(fig_vol, use_container_width=True)
    else:
        st.info("💡 Colunas de dimensões do produto não encontradas no dataset para gerar o cruzamento com frete.")

    st.markdown("---")
    st.markdown("### 🎯 Proposta de Valor Final")
    
    # Nova proposta de valor contemplando os insights do notebook
    proposta_box("""
    Transformar a logística de um passivo operacional para um motor de lealdade exige ações preditivas:<br><br>
    1. <strong>Detector de Anomalias em Trânsito (SAC Proativo):</strong> Implementar monitoramento nos logs de rastreio para identificar pacotes retidos em hubs lentos. O sistema deve acionar o SAC para notificar o cliente <em>antes</em> dele reclamar, mitigando avaliações negativas.<br><br>
    2. <strong>SLA Rígido de Postagem:</strong> Vendedores representam a primeira metade do gargalo. É preciso gamificar ou penalizar quem excede 2 dias para despacho.<br><br>
    3. <strong>Otimização Volumétrica:</strong> O frete é penalizado pelo volume. Incentivar a compra de cestas mais densas e menores dilui o custo e protege a margem no Last-Mile.
""")
    
else:
    st.warning("Dados não disponíveis.")
