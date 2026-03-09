import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from style_utils import inject_global_css, render_sidebar_logo, page_header, problema_box, insight_box, proposta_box, PLOTLY_LAYOUT, ACCENT_COLORS
from utils import get_analytical_df

st.set_page_config(page_title="Olist - Sazonalidade", page_icon=os.path.join(os.path.dirname(__file__), "..", "public", "Radar.svg"), layout="wide")
inject_global_css()
render_sidebar_logo()

page_header("📅 Capítulo 6: O Pulso Temporal", "Sazonalidade, picos de demanda e janelas de oportunidade")

# ── INTRO NARRATIVO ─────────────────────────────────────────────────────────────
st.markdown("""
<div style="background: rgba(108,99,255,0.07); border-left: 4px solid #6c63ff; border-radius: 0 12px 12px 0; padding: 1.2rem 1.5rem; margin-bottom: 1.5rem; font-family: 'DM Sans', sans-serif; color: #ccc; font-size: 0.95rem; line-height: 1.8;">
    Terminamos a análise financeira com um paradoxo: o <strong style="color:#ffd93d;">maior mês de receita é novembro</strong> — Black Friday —
    mas também é quando a logística mais falha e o NPS mais cai.<br><br>
    Este capítulo fecha a narrativa mostrando os <strong style="color:#a89bff;">padrões temporais completos</strong>:
    quando o cliente compra, em qual hora do dia, como o crescimento se distribui ao longo dos meses
    e como a sazonalidade pode ser usada como <strong>alavanca estratégica</strong> de marketing e operações.
</div>
""", unsafe_allow_html=True)

problema_box("Eventos pontuais como a Black Friday concentram volume enorme em poucos dias, sobrecarregando uma logística que não foi planejada para picos. Sem antecipação operacional, cada novembro se torna uma crise de NPS disfarçada de sucesso de vendas.")

df = get_analytical_df()
if not df.empty:
    # ── SÉRIE TEMPORAL PRINCIPAL ──────────────────────────────────────────────
    st.markdown("---")
    st.markdown("### 📈 Série Temporal de Faturamento")
    st.markdown("<span style='font-family:\"DM Sans\",sans-serif; color:#888; font-size:0.9rem;'>O crescimento é consistente ao longo do período — mas November/2017 revela a dependência da operação em picos sazonais.</span>", unsafe_allow_html=True)

    sales_trend = df.groupby('ano_mes').agg(
        receita=('receita_liquida', 'sum'),
        pedidos=('order_id', 'count'),
        atraso_rate=('flag_atraso', 'mean')
    ).reset_index().sort_values('ano_mes')

    _layout = {k: v for k, v in PLOTLY_LAYOUT.items() if k not in ("xaxis", "yaxis")}
    fig_timeline = go.Figure()
    fig_timeline.add_trace(go.Scatter(
        x=sales_trend['ano_mes'], y=sales_trend['receita'],
        mode='lines+markers', name='Receita Mensal',
        line=dict(color='#00c882', width=3),
        fill='tozeroy', fillcolor='rgba(0,200,130,0.1)',
        hovertemplate='<b>%{x}</b><br>Receita: R$ %{y:,.0f}<extra></extra>'
    ))
    fig_timeline.add_trace(go.Scatter(
        x=sales_trend['ano_mes'], y=sales_trend['atraso_rate'] * 100,
        mode='lines+markers', name='Taxa de Atraso (%)',
        line=dict(color='#ff5050', dash='dot', width=2),
        yaxis='y2',
        hovertemplate='<b>%{x}</b><br>Atraso: %{y:.1f}%<extra></extra>'
    ))
    bf_data = sales_trend[sales_trend['ano_mes'] == '2017-11']
    if not bf_data.empty:
        fig_timeline.add_annotation(
            x='2017-11', y=bf_data['receita'].values[0],
            text="🖤 Black Friday<br>Pico de Receita<br>+ Pico de Atraso",
            showarrow=True, arrowhead=2, arrowcolor='#ffd93d',
            bgcolor='rgba(0,0,0,0.8)', font=dict(color='#ffd93d', size=10),
            bordercolor='#ffd93d', borderwidth=1, borderpad=5
        )
    fig_timeline.update_layout(
        **_layout,
        title="Receita Mensal vs Taxa de Atraso",
        xaxis=dict(title="Mês/Ano", gridcolor="rgba(108,99,255,0.15)"),
        yaxis=dict(title="Receita (R$)", gridcolor="rgba(108,99,255,0.15)"),
        yaxis2=dict(title="Taxa de Atraso (%)", overlaying="y", side="right", showgrid=False),
        hovermode="x unified",
    )
    st.plotly_chart(fig_timeline, use_container_width=True)

    insight_box("O gráfico dual revela o paradoxo da Black Friday: <strong>receita máxima e taxa de atraso máxima no mesmo mês</strong>. "
                "Cresce o GMV e cai o NPS — exatamente quando o cliente está mais engajado e suscetível a se tornar um detrator.")

    st.markdown("---")

    # ── GRÁFICO 2: DIA DA SEMANA + HORA DO DIA ───────────────────────────────
    st.markdown("### Quando o Cliente Compra?")
    st.markdown("<span style='font-family:\"DM Sans\",sans-serif; color:#888; font-size:0.9rem;'>Identificar a janela de maior engajamento é a base para alocação eficiente de budget de mídia.</span>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        pt_days = {'Monday': 'Segunda', 'Tuesday': 'Terça', 'Wednesday': 'Quarta',
                   'Thursday': 'Quinta', 'Friday': 'Sexta', 'Saturday': 'Sábado', 'Sunday': 'Domingo'}
        sales_day = df.groupby('dia_semana').agg(
            receita=('receita_liquida', 'sum'),
            pedidos=('order_id', 'count')
        ).reindex(day_order).reset_index()
        sales_day['dia_semana'] = sales_day['dia_semana'].map(pt_days)

        # Insight: dias úteis dominam — consumidor que compra durante o expediente
        fig_day = px.bar(
            sales_day, x='dia_semana', y='receita',
            color='receita', color_continuous_scale='Greens',
            text='pedidos',
            hover_data={'pedidos': ':,', 'receita': ':,.0f'},
            labels={'receita': 'Faturamento (R$)', 'dia_semana': 'Dia da Semana', 'pedidos': 'Pedidos'},
            title="Faturamento por Dia da Semana"
        )
        fig_day.update_traces(texttemplate='%{text:,} pedidos', textposition='outside', textfont_size=9)
        fig_day.update_layout(**PLOTLY_LAYOUT)
        st.plotly_chart(fig_day, use_container_width=True)

    with col2:
        sales_hour = df.groupby('hora_compra').agg(
            pedidos=('order_id', 'count'),
            receita=('receita_liquida', 'sum')
        ).reset_index()
        sales_hour.columns = ['Hora', 'Volume de Pedidos', 'Receita']

        # Insight: pico entre 10h-16h → window para push/ads
        fig_hour = px.area(
            sales_hour, x='Hora', y='Volume de Pedidos',
            title="Volume de Pedidos por Hora do Dia",
            hover_data={'Receita': ':,.0f'},
            color_discrete_sequence=['#6c63ff']
        )
        fig_hour.update_layout(**PLOTLY_LAYOUT)
        fig_hour.update_traces(fillcolor='rgba(108,99,255,0.2)')
        # Destaque da janela de oportunidade 10h-16h
        fig_hour.add_vrect(
            x0=10, x1=16,
            fillcolor="rgba(0,200,130,0.1)", opacity=0.8, layer="below", line_width=0,
            annotation_text="🎯 Prime-Time<br>10h – 16h",
            annotation_position="top left",
            annotation_font_color="#00c882", annotation_font_size=10
        )
        st.plotly_chart(fig_hour, use_container_width=True)

    insight_box("As compras concentram-se entre <strong>10h e 16h, de segunda a sexta</strong>. "
                "Esse padrão evidencia um consumidor que compra no trabalho — uma janela de oportunidade precisa para campanhas de Ads e Push Notifications com custo de leilão menor.")

    st.markdown("---")

    # ── GRÁFICO 3: HEATMAP MÊS × DIA DA SEMANA ────────────────────────────────
    st.markdown("### Mapa de Calor: Volume por Mês × Dia da Semana")
    st.markdown("<span style='font-family:\"DM Sans\",sans-serif; color:#888; font-size:0.9rem;'>A concentração de vendas vai além do calendário. A combinação de mês e dia revela padrões de comportamento que guiam a estratégia de conteúdo e estoque.</span>", unsafe_allow_html=True)

    df_copy = df.copy()
    df_copy['mes'] = df_copy['order_purchase_timestamp'].dt.month
    df_copy['dia_sem'] = df_copy['order_purchase_timestamp'].dt.day_name()
    day_order_pt = ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado', 'Domingo']
    pt_days_all = {'Monday': 'Segunda', 'Tuesday': 'Terça', 'Wednesday': 'Quarta',
                   'Thursday': 'Quinta', 'Friday': 'Sexta', 'Saturday': 'Sábado', 'Sunday': 'Domingo'}
    pt_months_map = {1: 'Jan', 2: 'Fev', 3: 'Mar', 4: 'Abr', 5: 'Mai', 6: 'Jun',
                     7: 'Jul', 8: 'Ago', 9: 'Set', 10: 'Out', 11: 'Nov', 12: 'Dez'}
    df_copy['dia_sem_pt'] = df_copy['dia_sem'].map(pt_days_all)
    df_copy['mes_nome'] = df_copy['mes'].map(pt_months_map)

    heatmap_data = df_copy.groupby(['mes_nome', 'mes', 'dia_sem_pt'])['order_id'].count().reset_index()
    heatmap_data.columns = ['Mês', 'mes_num', 'Dia', 'Pedidos']
    heatmap_data = heatmap_data.sort_values('mes_num')
    heatmap_pivot = heatmap_data.pivot(index='Dia', columns='Mês', values='Pedidos')
    # Reordenar linhas de dias
    valid_days = [d for d in day_order_pt if d in heatmap_pivot.index]
    heatmap_pivot = heatmap_pivot.reindex(valid_days)
    # Reordenar colunas de meses
    month_order = [pt_months_map[i] for i in range(1, 13) if pt_months_map[i] in heatmap_pivot.columns]
    heatmap_pivot = heatmap_pivot[month_order]

    fig_heat = px.imshow(
        heatmap_pivot,
        color_continuous_scale='Viridis',
        aspect='auto',
        title="Volume de Pedidos: Mês × Dia da Semana",
        labels=dict(x='Mês', y='Dia da Semana', color='Pedidos')
    )
    fig_heat.update_layout(**PLOTLY_LAYOUT)
    st.plotly_chart(fig_heat, use_container_width=True)

    st.markdown("---")

    # ── GRÁFICO 4: SAZONALIDADE MENSAL ────────────────────────────────────────
    st.markdown("### Sazonalidade Mensal Acumulada")
    st.markdown("<span style='font-family:\"DM Sans\",sans-serif; color:#888; font-size:0.9rem;'>Novembro é o mês-chave. Mas a queda em dezembro mostra que o ciclo do cliente ainda não está otimizado para o pré-Natal.</span>", unsafe_allow_html=True)

    df_copy2 = df.copy()
    df_copy2['mes_nome'] = df_copy2['order_purchase_timestamp'].dt.month
    month_order_en = {1: 'Jan', 2: 'Fev', 3: 'Mar', 4: 'Abr', 5: 'Mai', 6: 'Jun',
                      7: 'Jul', 8: 'Ago', 9: 'Set', 10: 'Out', 11: 'Nov', 12: 'Dez'}
    df_copy2['mes_nome'] = df_copy2['mes_nome'].map(month_order_en)
    sales_month = df_copy2.groupby('mes_nome').agg(
        receita=('receita_liquida', 'sum'),
        pedidos=('order_id', 'count'),
        atraso_rate=('flag_atraso', 'mean')
    ).reset_index()
    month_seq = list(month_order_en.values())
    sales_month = sales_month.set_index('mes_nome').reindex(month_seq).reset_index()

    colors_bar = ['#ff6b6b' if m == 'Nov' else '#00c882' if m == 'Dez' else '#6c63ff' for m in sales_month['mes_nome']]
    fig_month = px.bar(
        sales_month, x='mes_nome', y='receita',
        text='pedidos',
        hover_data={'pedidos': ':,', 'atraso_rate': ':.1%', 'receita': ':,.0f'},
        labels={'receita': 'Faturamento (R$)', 'mes_nome': 'Mês', 'pedidos': 'Pedidos', 'atraso_rate': 'Taxa de Atraso'},
        title="Sazonalidade Mensal Acumulada (Nov = Black Friday)"
    )
    fig_month.update_traces(marker_color=colors_bar, texttemplate='%{text:,}', textposition='outside', textfont_size=9)
    fig_month.update_layout(**PLOTLY_LAYOUT)

    nov_val = sales_month[sales_month['mes_nome'] == 'Nov']['receita'].values
    if len(nov_val) > 0 and not (nov_val[0] != nov_val[0]):  # não NaN
        fig_month.add_annotation(
            x='Nov', y=nov_val[0],
            text="🖤 Black Friday", showarrow=True, arrowhead=2, arrowcolor='#ffd93d',
            bgcolor='rgba(0,0,0,0.7)', font=dict(color='#ffd93d', size=12),
            bordercolor='#ffd93d', borderwidth=1, borderpad=5, yshift=15
        )
    st.plotly_chart(fig_month, use_container_width=True)

    st.markdown("---")

    proposta_box("""
    <strong>1. Dayparting Algorítmico (Prime-Time Marketing):</strong> Alocar 75% do budget de Ads na janela de 10h-16h, dias úteis. Redução imediata do CPC e aumento do ROAS sem mudar o investimento total.<br><br>
    <strong>2. Blindagem Logística Preventiva (Outubro = Preparação):</strong> Renegociar SLAs com transportadoras em outubro, expandir estoque em CDs regionais e contratar temporários antes do pico de novembro. Proteger o NPS no momento de maior volume.<br><br>
    <strong>3. Ciclo de Pré-Natal (Dezembro como Oportunidade):</strong> Os dados mostram queda em dezembro após o pico de novembro. Campanhas de pré-natal com frete diferenciado podem capturar o volume de presente que está sendo perdido para concorrentes.
    """)

    # ── FECHAMENTO NARRATIVO ─────────────────────────────────────────────────
    st.markdown("""
    <div style="margin-top:2rem; padding: 1.5rem 2rem; background: linear-gradient(135deg, rgba(108,99,255,0.12), rgba(0,200,130,0.08)); border-radius: 16px; border: 1px solid rgba(108,99,255,0.3); font-family: 'DM Sans', sans-serif; color: #ccc; font-size: 0.95rem; line-height: 1.9;">
        <div style="font-family:'Poppins',sans-serif; font-size:1.1rem; font-weight:700; color:#a89bff; margin-bottom:0.8rem;">
            🏁 Fim da Análise — O Que Descobrimos?
        </div>
        Ao longo desta jornada, conectamos os pontos entre <strong style="color:#d9d9d9;">geography → logística → satisfação → financeiro → tempo</strong>:<br><br>
        ① O Brasil continental cria <strong>dois e-commerces</strong> com custos radicalmente diferentes.<br>
        ② O atraso na entrega é o <strong>maior destruidor de NPS</strong> — mais que o produto em si.<br>
        ③ O vendedor é responsável por <strong>+40% do tempo de entrega</strong> antes da transportadora ser envolvida.<br>
        ④ O frete é percebido pelo cliente como parte do produto — e destrói a avaliação quando é alto.<br>
        ⑤ A Black Friday é o pico de receita <strong>e</strong> o pico de falha operacional — um paradoxo que pode ser resolvido.<br><br>
        <strong style="color:#00c882;">A solução não é um único projeto, mas um conjunto de alavancas coordenadas em logística, produto e marketing.</strong>
        Veja as propostas no próximo capítulo.
    </div>
    """, unsafe_allow_html=True)

else:
    st.warning("Dados não carregados.")
