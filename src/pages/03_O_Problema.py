import streamlit as st
import plotly.graph_objects as go
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from style_utils import inject_global_css, render_sidebar_logo, page_header, problema_box, proposta_box, PLOTLY_LAYOUT
from utils import get_analytical_df

st.set_page_config(page_title="Olist - O peso do Atraso", page_icon=os.path.join(os.path.dirname(__file__), "..", "public", "Radar.svg"), layout="wide")
inject_global_css()
render_sidebar_logo()

page_header("❓ O Problema Central", "A dor de negócio que motivou esta investigação")

problema_box(" O Olist enfrenta um paradoxo operacional: à medida que a plataforma cresce, os <strong>gargalos logísticos</strong> e as <strong>disparidades regionais</strong> criam uma experiência de compra cada vez mais desigual. O resultado? Clientes insatisfeitos que não retornam, e vendedores que perdem competitividade por culpa de um elo da cadeia (transporte) que não controlam. ")

st.markdown("---")

st.markdown("### 🔗 O Ciclo Vicioso Identificado")

df = get_analytical_df()

if not df.empty:
    total = df['order_id'].nunique()
    delayed = df[df['flag_atraso'] == 1]['order_id'].nunique()
    avg_score_delay = df[df['flag_atraso'] == 1]['review_score'].mean()
    avg_score_ok = df[df['flag_atraso'] == 0]['review_score'].mean()

    col1, col2, col3 = st.columns(3)
    col1.metric("Pedidos com Atraso", f"{delayed:,}", f"{delayed/total*100:.1f}% do total", delta_color="inverse")
    col2.metric("Nota Média (Com Atraso)", f"{avg_score_delay:.2f} ⭐", f"-{avg_score_ok - avg_score_delay:.2f} vs no prazo", delta_color="inverse")
    col3.metric("Queda no NPS por Atraso", f"{(avg_score_ok - avg_score_delay) / avg_score_ok * 100:.1f}%", "de impacto negativo", delta_color="inverse")

st.markdown("---")

# Diagrama de ciclo vicioso com sankey simplificado
st.markdown("### 🌀 Diagrama: A Cadeia de Causa e Efeito")

fig = go.Figure(go.Sankey(
    arrangement="snap",
    node=dict(
        pad=20,
        thickness=25,
        line=dict(color="rgba(108,99,255,0.5)", width=1),
        label=[
            "Disparidade Regional",
            "Alto Custo de Frete",
            "Atrasos na Entrega",
            "Baixa Satisfação (NPS↓)",
            "Churn de Clientes",
            "Queda no GMV",
        ],
        color=["#6c63ff", "#ff6b6b", "#ff6b6b", "#ffd93d", "#ff5050", "#ff3030"],
        x=[0.01, 0.25, 0.25, 0.55, 0.75, 0.99],
        y=[0.2,  0.1,  0.5,  0.5,  0.5,  0.5],
    ),
    link=dict(
        source=[0, 0, 1, 2, 3, 4],
        target=[1, 2, 3, 3, 4, 5],
        value=[40, 60, 55, 70, 85, 90],
        color=[
            "rgba(108,99,255,0.2)",
            "rgba(255,107,107,0.2)",
            "rgba(255,107,107,0.2)",
            "rgba(255,107,107,0.25)",
            "rgba(255,80,80,0.25)",
            "rgba(255,48,48,0.25)",
        ]
    )
))
fig.update_layout(**PLOTLY_LAYOUT, title="Cadeia de Impacto: Do Problema ao Custo de Negócio", height=350)
st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

proposta_box(" A resposta não é única. As próximas análises demonstram que a solução exige uma abordagem <strong>multidimensional</strong>: descentralização logística, incentivos de parcelamento, campanhas no horário de pico e monitoramento preditivo de atrasos via Machine Learning. ")
