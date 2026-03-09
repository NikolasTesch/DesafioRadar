import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from style_utils import inject_global_css, render_sidebar_logo, page_header, problema_box, insight_box, proposta_box, PLOTLY_LAYOUT, ACCENT_COLORS
from utils import get_analytical_df

st.set_page_config(page_title="Olist - Logística", page_icon=os.path.join(os.path.dirname(__file__), "..", "public", "Radar.svg"), layout="wide")
inject_global_css()
render_sidebar_logo()

page_header("🚚 Capítulo 3: O Gargalo Logístico", "Onde o pedido se perde antes de chegar ao cliente")

# ── INTRO NARRATIVO ─────────────────────────────────────────────────────────────
st.markdown("""
<div style="background: rgba(108,99,255,0.07); border-left: 4px solid #6c63ff; border-radius: 0 12px 12px 0; padding: 1.2rem 1.5rem; margin-bottom: 1.5rem; font-family: 'DM Sans', sans-serif; color: #ccc; font-size: 0.95rem; line-height: 1.8;">
    Entendemos que a geography cria custos diferentes. Agora, uma pergunta mais cirúrgica:
    <strong style="color:#a89bff;">quem é o verdadeiro responsável pelo atraso?</strong><br><br>
    O processo de entrega tem dois atores distintos: o <strong>vendedor</strong>, que precisa postar o pedido,
    e a <strong>transportadora</strong>, que precisa levá-lo até a porta do cliente.
    Os dados revelam uma divisão de responsabilidade que muda completamente a estratégia de intervenção.
</div>
""", unsafe_allow_html=True)

problema_box("Pedidos com atraso têm nota média de <strong>2.1/5</strong> vs <strong>4.2/5</strong> para pedidos pontuais — uma queda de 50% no NPS. Em períodos de pico como a Black Friday, a taxa de atraso explode, expondo que a malha opera no limite da capacidade.")

df = get_analytical_df()
if not df.empty:
    df_del = df[df['order_status'] == 'delivered'].copy()

    st.markdown("---")
    st.markdown("### ⏱️ Distribuição e Gargalos de Prazo")
    # Métricas de tempo calculadas
    df_del['tempo_postagem'] = (df_del['order_delivered_carrier_date'] - df_del['order_approved_at']).dt.days
    df_del['tempo_transporte'] = (df_del['order_delivered_customer_date'] - df_del['order_delivered_carrier_date']).dt.days

    # ── KPI BANNER ─────────────────────────────────────────────────────────────
    pct_delayed = df_del['flag_atraso'].mean() * 100
    avg_delay_days = df_del[df_del['flag_atraso'] == 1]['dias_atraso'].mean()
    avg_delivery = df_del['tempo_entrega_real'].mean()
    worst_state = df_del.groupby('customer_state')['flag_atraso'].mean().idxmax()

    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Prazo Médio Real", f"{avg_delivery:.1f} dias")
    k2.metric("% Pedidos Atrasados", f"{pct_delayed:.1f}%", delta="vs 0% ideal", delta_color="inverse")
    k3.metric("Média de Dias de Atraso", f"{avg_delay_days:.1f} dias", delta="quando atrasa", delta_color="inverse")
    k4.metric("Estado Mais Afetado", worst_state, "maior taxa de atraso")

    st.markdown("---")

    # ── GRÁFICO 1: ONDE O TEMPO É PERDIDO? (FUNIL DE RESPONSABILIDADE) ────────
    st.markdown("### Onde o Tempo é Perdido? — Análise de Responsabilidade")
    st.markdown("<span style='font-family:\"DM Sans\",sans-serif; color:#888; font-size:0.9rem;'>O atraso começa antes da transportadora tocar no pacote. Veja a divisão entre responsabilidade do vendedor e da transportadora.</span>", unsafe_allow_html=True)

    avg_post = df_del['tempo_postagem'].mean()
    avg_trans = df_del['tempo_transporte'].mean()

    col_pie, col_bar = st.columns([1, 1.5])
    with col_pie:
        # Insight: ~40% do tempo total é responsabilidade do vendedor (postagem)
        metrics_df = pd.DataFrame({
            'Etapa': [f'Vendedor → Transportadora\n({avg_post:.1f} dias)', f'Transportadora → Cliente\n({avg_trans:.1f} dias)'],
            'Média de Dias': [avg_post, avg_trans]
        })
        fig_comp = px.pie(
            metrics_df, values='Média de Dias', names='Etapa',
            hole=0.55, color_discrete_sequence=['#6c63ff', '#ff6b6b'],
            title="Composição do Prazo Total de Entrega"
        )
        fig_comp.update_layout(**PLOTLY_LAYOUT)
        fig_comp.update_traces(textinfo='percent+label', textfont_size=10)
        st.plotly_chart(fig_comp, use_container_width=True)

    with col_bar:
        # Distribuição do tempo de entrega real com média anotada
        fig_hist = px.histogram(
            df_del, x="tempo_entrega_real", nbins=50,
            labels={'tempo_entrega_real': 'Dias para Entrega', 'count': 'Frequência'},
            color_discrete_sequence=['#6c63ff'],
            title="Distribuição do Prazo Real de Entrega"
        )
        fig_hist.update_layout(**PLOTLY_LAYOUT, xaxis_range=[0, 45])
        fig_hist.add_vline(
            x=avg_delivery, line_dash='dash', line_color='#ffd93d',
            annotation_text=f"Média: {avg_delivery:.1f}d",
            annotation_position="top right",
            annotation_font_color='#ffd93d'
        )
        fig_hist.add_vline(
            x=df_del['tempo_entrega_real'].quantile(0.9), line_dash='dot', line_color='#ff5050',
            annotation_text=f"P90: {df_del['tempo_entrega_real'].quantile(0.9):.1f}d",
            annotation_position="top left",
            annotation_font_color='#ff5050'
        )
        st.plotly_chart(fig_hist, use_container_width=True)

    insight_box(f"<strong>{avg_post / (avg_post + avg_trans) * 100:.0f}%</strong> do tempo total de entrega é consumido ainda na fase de postagem (responsabilidade do vendedor). "
                f"A transportadora recebe o pacote em média em <strong>{avg_post:.1f} dias</strong> e leva mais <strong>{avg_trans:.1f} dias</strong> para entregar. Intervir no SLA do vendedor é a ação de maior impacto.")

    st.markdown("---")

    # ── GRÁFICO 2: IMPACTO DO ATRASO NA NOTA ─────────────────────────────────
    st.markdown("### Impacto Direto do Atraso na Avaliação")

    sat_analysis = df_del.groupby('flag_atraso')['review_score'].agg(['mean', 'count']).reset_index()
    sat_analysis['Status'] = sat_analysis['flag_atraso'].map({0: '✅ No Prazo', 1: '❌ Com Atraso'})
    sat_analysis.columns = ['flag_atraso', 'Nota Média', 'Total Reviews', 'Status']

    nota_pontual = sat_analysis[sat_analysis['flag_atraso'] == 0]['Nota Média'].values[0]
    nota_atrasado = sat_analysis[sat_analysis['flag_atraso'] == 1]['Nota Média'].values[0]
    diff = nota_pontual - nota_atrasado

    fig_sat = px.bar(
        sat_analysis, x='Status', y='Nota Média',
        color='Status',
        color_discrete_map={'✅ No Prazo': '#00c882', '❌ Com Atraso': '#ff5050'},
        text='Nota Média',
        hover_data={'Total Reviews': ':,'},
        title=f"Avaliação Média: Pontual ({nota_pontual:.2f}) vs Atrasado ({nota_atrasado:.2f})",
        labels={'Nota Média': 'Nota Média (1-5)', 'Status': ''}
    )
    fig_sat.update_layout(**PLOTLY_LAYOUT, showlegend=False)
    fig_sat.update_traces(texttemplate='%{text:.2f}', textfont_size=18, textposition='outside')
    st.plotly_chart(fig_sat, use_container_width=True)

    insight_box(f"A diferença de <strong>{diff:.2f} pontos</strong> na avaliação entre entregas pontuais e atrasadas é a distância entre um <strong>Promotor (NPS+)</strong> e um <strong>Detrator (NPS-)</strong>. "
                f"Cada pedido atrasado tem potencial de gerar reviews negativos que impactam diretamente o CAC futuro da plataforma.")

    st.markdown("---")

    # ── GRÁFICO 3: TAXA DE ATRASO POR ESTADO ─────────────────────────────────
    st.markdown("### Taxa de Atraso por Estado")
    delay_by_state = df_del.groupby('customer_state').agg(
        taxa_atraso=('flag_atraso', 'mean'),
        num_pedidos=('order_id', 'count'),
        nota_media=('review_score', 'mean'),
        prazo_medio=('tempo_entrega_real', 'mean')
    ).reset_index()
    delay_by_state['taxa_atraso_pct'] = delay_by_state['taxa_atraso'] * 100

    fig_delay = px.bar(
        delay_by_state.sort_values('taxa_atraso_pct', ascending=False),
        x='customer_state', y='taxa_atraso_pct',
        labels={'taxa_atraso_pct': '% Pedidos Atrasados', 'customer_state': 'Estado'},
        color='nota_media',
        color_continuous_scale='RdYlGn',
        range_color=[2.5, 5.0],
        hover_data={'num_pedidos': ':,', 'nota_media': ':.2f', 'prazo_medio': ':.1f'},
        title="Taxa de Atraso por Estado (cor = nota média)"
    )
    fig_delay.update_layout(**PLOTLY_LAYOUT)
    st.plotly_chart(fig_delay, use_container_width=True)

    st.markdown("---")

    # ── GRÁFICO 4: EVOLUÇÃO TEMPORAL ─────────────────────────────────────────
    st.markdown("### Evolução da Eficiência Logística ao Longo do Tempo")
    st.markdown("<span style='font-family:\"DM Sans\",sans-serif; color:#888; font-size:0.9rem;'>A performance logística melhorou com o tempo — mas os picos sazonais continuam expondo a fragilidade do sistema.</span>", unsafe_allow_html=True)

    logistic_timeline = df_del.groupby('ano_mes').agg(
        prazo_medio=('tempo_entrega_real', 'mean'),
        atraso_rate=('flag_atraso', 'mean'),
        pedidos=('order_id', 'count')
    ).reset_index()

    _layout = {k: v for k, v in PLOTLY_LAYOUT.items() if k not in ("xaxis", "yaxis")}
    fig_log = go.Figure()
    fig_log.add_trace(go.Scatter(
        x=logistic_timeline['ano_mes'], y=logistic_timeline['prazo_medio'],
        mode='lines+markers', name='Prazo Médio (Dias)',
        line=dict(color='#6c63ff', width=3), fill='tozeroy',
        fillcolor='rgba(108,99,255,0.1)',
        hovertemplate='<b>%{x}</b><br>Prazo: %{y:.1f} dias<extra></extra>'
    ))
    fig_log.add_trace(go.Scatter(
        x=logistic_timeline['ano_mes'], y=logistic_timeline['atraso_rate'] * 100,
        mode='lines+markers', name='Taxa de Atraso (%)',
        line=dict(color='#ff5050', dash='dot', width=2),
        yaxis='y2',
        hovertemplate='<b>%{x}</b><br>Atraso: %{y:.1f}%<extra></extra>'
    ))
    # Anotação Black Friday
    bf_data = logistic_timeline[logistic_timeline['ano_mes'] == '2017-11']
    if not bf_data.empty:
        fig_log.add_annotation(
            x='2017-11', y=bf_data['prazo_medio'].values[0],
            text="🖤 Black Friday<br>Pico de Atraso",
            showarrow=True, arrowhead=2, arrowcolor='#ffd93d',
            bgcolor='rgba(255,80,0,0.8)', font=dict(color='white', size=10),
            bordercolor='#ffd93d', borderwidth=1, borderpad=5
        )
    fig_log.update_layout(
        **_layout,
        title="Prazo Médio vs Taxa de Atraso ao Longo do Tempo",
        xaxis=dict(title="Mês", gridcolor="rgba(108,99,255,0.15)", zerolinecolor="rgba(108,99,255,0.2)"),
        yaxis=dict(title="Dias Médios", gridcolor="rgba(108,99,255,0.15)"),
        yaxis2=dict(title="Taxa de Atraso (%)", overlaying="y", side="right", showgrid=False),
        hovermode="x unified",
    )
    st.plotly_chart(fig_log, use_container_width=True)

    st.markdown("---")

    # ── GRÁFICO 5: FRETE VS VOLUME DO PACOTE ─────────────────────────────────
    col_dims = ['product_weight_g', 'product_length_cm', 'product_height_cm', 'product_width_cm', 'freight_value']
    if all(col in df_del.columns for col in col_dims):
        st.markdown("### Dimensão do Produto vs Custo de Frete")
        st.markdown("<span style='font-family:\"DM Sans\",sans-serif; color:#888; font-size:0.9rem;'>Produtos maiores custam mais para enviar. Incentivar compras de produtos leves e de alto valor dilui o custo logístico.</span>", unsafe_allow_html=True)
        df_del['volume_cm3'] = df_del['product_length_cm'] * df_del['product_height_cm'] * df_del['product_width_cm']
        df_sample = df_del.dropna(subset=['volume_cm3', 'freight_value', 'review_score']).sample(n=min(5000, len(df_del)), random_state=42)
        fig_vol = px.scatter(
            df_sample, x='volume_cm3', y='freight_value',
            trendline='ols', opacity=0.4,
            color='review_score', color_continuous_scale='RdYlGn',
            hover_data={'customer_state': True, 'product_category_name': True, 'freight_value': ':.2f'},
            labels={'volume_cm3': 'Volume do Pacote (cm³)', 'freight_value': 'Frete (R$)', 'review_score': 'Nota'},
            title="Correlação: Volume Cúbico × Custo de Frete (cor = satisfação)"
        )
        fig_vol.update_layout(**PLOTLY_LAYOUT)
        st.plotly_chart(fig_vol, use_container_width=True)
        st.markdown("---")

    # ── PROPOSTA ───────────────────────────────────────────────────────────────
    proposta_box("""
    <strong>1. Detector de Anomalias em Trânsito (SAC Proativo):</strong> Monitorar logs de rastreio para identificar pacotes travados em hubs lentos. Notificar o cliente <em>antes</em> que ele perceba o atraso — mitigando reviews negativos.<br><br>
    <strong>2. SLA Rígido de Postagem (Gamificação de Vendedores):</strong> Penalizar/incentivar vendedores com base no tempo de postagem. A análise mostra que >40% do atraso começa ainda no vendedor.<br><br>
    <strong>3. Otimização Volumétrica:</strong> Incentivar bundles de produtos menores e de alto ticket para diluir o custo de frete por pedido, protegendo a margem no Last-Mile.
    """)

    # ── BRIDGE NARRATIVO ─────────────────────────────────────────────────────
    st.markdown("""
    <div style="margin-top:2rem; padding: 1.2rem 1.5rem; background: rgba(108,99,255,0.06); border-radius: 12px; border: 1px solid rgba(108,99,255,0.2); font-family: 'DM Sans', sans-serif; color: #aaa; font-size: 0.9rem; line-height: 1.7;">
        🔜 <strong style="color:#a89bff;">Próximo Capítulo: Satisfação do Cliente</strong><br>
        Sabemos que o atraso derruba a nota. Mas será que é só isso? O próximo capítulo vai além do prazo
        e analisa todas as variáveis que transformam um comprador em promotor — ou em detrator ativo da marca.
    </div>
    """, unsafe_allow_html=True)

else:
    st.warning("Dados não disponíveis.")
