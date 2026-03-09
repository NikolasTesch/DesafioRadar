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

# ── CONTEXTO ─────────────────────────────────────────────────────────────────
st.markdown(
    """
<div style="max-width:900px; font-family:'DM Sans',sans-serif; color:#c0c0c0; font-size:1rem; line-height:1.9;">
O Brasil tem um dos e-commerces que mais cresce no mundo. Mas cresce <em>apesar</em> da sua logística — não graças a ela.
</div>
""",
    unsafe_allow_html=True,
)

st.markdown("---")
st.markdown("### 🌎 Desafio 1: Dimensões Continentais vs. Custo de Frete")

st.markdown(
    """
<p style="font-family:'DM Sans',sans-serif; color:#bbb; font-size:0.96rem; line-height:1.85; max-width:860px;">
O Brasil possui 8,5 milhões de km² de território e apenas <strong>três grandes hubs logísticos concentrados no Sudeste</strong>
(São Paulo, Rio de Janeiro e Minas Gerais). Isso cria uma assimetria brutal:
um produto vendido por R$ 50 em São Paulo pode ter um frete de R$ 8.
O mesmo produto enviado para Roraima pode custar <strong>R$ 30–40 de frete</strong> — ou seja,
o custo logístico pode superar o valor do produto.
</p>
""",
    unsafe_allow_html=True,
)

st.warning("""
⚠️ **Impacto Direto:** Para categorias de produtos de baixo ticket médio (R$ 20–60), o frete regional no Norte e Nordeste torna a venda economicamente inviável — seja para o vendedor, para o comprador, ou para os dois simultaneamente.
""")

st.markdown("---")
st.markdown("### ⏱️ Desafio 2: Tempo de Entrega como Driver de Satisfação")

col_a, col_b = st.columns([3, 2])

with col_a:
    st.markdown(
        """
    <p style="font-family:'DM Sans',sans-serif; color:#bbb; font-size:0.96rem; line-height:1.85;">
    A satisfação no e-commerce moderno é ditada não apenas pelo produto em si, mas pela
    <strong>experiência de compra completa</strong> — e o prazo de entrega é o componente mais crítico dessa experiência.
    </p>
    <p style="font-family:'DM Sans',sans-serif; color:#bbb; font-size:0.96rem; line-height:1.85;">
    Quando um cliente finaliza uma compra, ele cria uma expectativa de prazo. Cada dia além desse prazo
    não é percebido de forma linear: o cliente não fica <em>um pouco</em> mais frustrado — ele fica
    <em>exponencialmente</em> mais insatisfeito. Esta é a <strong>"curva de frustração de entrega"</strong>,
    e os dados da Olist a confirmam de forma contundente.
    </p>
    <p style="font-family:'DM Sans',sans-serif; color:#bbb; font-size:0.96rem; line-height:1.85;">
    A análise mostra que pedidos entregues <strong>com atraso têm nota média de 2.1/5</strong>,
    enquanto pedidos entregues <strong>no prazo alcançam 4.2/5</strong>.
    Isso representa uma queda de <strong>50% no NPS</strong> — a diferença entre um promotor da marca e um detrator ativo.
    </p>
    """,
        unsafe_allow_html=True,
    )

with col_b:
    df = get_analytical_df()
    if not df.empty:
        total = df["order_id"].nunique()
        delayed = df[df["flag_atraso"] == 1]["order_id"].nunique()
        avg_score_delay = df[df["flag_atraso"] == 1]["review_score"].mean()
        avg_score_ok = df[df["flag_atraso"] == 0]["review_score"].mean()

        st.metric(
            "Pedidos com Atraso",
            f"{delayed:,}",
            f"{delayed / total * 100:.1f}% do total",
            delta_color="inverse",
        )
        st.metric(
            "Nota c/ Atraso",
            f"{avg_score_delay:.2f} ⭐",
            f"-{avg_score_ok - avg_score_delay:.2f} vs no prazo",
            delta_color="inverse",
        )
        st.metric(
            "Queda no NPS",
            f"{(avg_score_ok - avg_score_delay) / avg_score_ok * 100:.1f}%",
            "impacto negativo",
            delta_color="inverse",
        )

st.markdown("---")
st.markdown("### 💸 Desafio 3: Consequências Financeiras para o E-commerce")

st.markdown(
    """
<p style="font-family:'DM Sans',sans-serif; color:#bbb; font-size:0.96rem; line-height:1.85; max-width:900px;">
A cadeia de consequências de um atraso vai muito além da insatisfação imediata. Ela corrói sistematicamente
o valor financeiro do negócio em três dimensões:
</p>
""",
    unsafe_allow_html=True,
)

impacts = [
    (
        "📉",
        "Aumento do Churn e Queda no LTV",
        "Clientes que recebem pedidos atrasados têm <strong>30–50% menos probabilidade de recomprar</strong>. Em um marketplace, onde o custo de aquisição de cliente (CAC) é alto, perder um cliente na primeira compra por falha logística é o pior cenário possível. O Lifetime Value (LTV) desse cliente é essencialmente zero.",
        "#ff5050",
    ),
    (
        "🔄",
        "Custos de Logística Reversa (Devoluções)",
        "Atrasos elevam significativamente a taxa de cancelamento e devolução. Cada devolução gera um custo de <strong>logística reversa</strong> que frequentemente supera a margem do produto — além de exigir reprocessamento, reestoque e, às vezes, descarte do item.",
        "#ffd93d",
    ),
    (
        "🗣️",
        "Impacto na Reputação e Custo de Aquisição Futuro",
        "Clientes insatisfeitos com nota 1 ou 2 são <strong>detratores ativos</strong>: compartilham experiências negativas em redes sociais e em plataformas de avaliação. Isso aumenta o custo de aquisição de novos clientes (CAC), pois a reputação negativa exige investimento maior em advertising para superar a percepção pública.",
        "#ff6b6b",
    ),
]

for icon, title, text, color in impacts:
    st.markdown(
        f"""
    <div style="
        display: flex; gap: 1.2rem; align-items: flex-start;
        background: rgba(13,12,104,0.4);
        border-left: 4px solid {color};
        border-radius: 0 12px 12px 0;
        padding: 1.1rem 1.4rem; margin-bottom: 0.9rem;
    ">
        <div style="font-size:1.8rem; flex-shrink:0; margin-top:0.1rem;">{icon}</div>
        <div>
            <div style="font-family:'Poppins',sans-serif; font-weight:700; font-size:0.95rem; color:#d9d9d9; margin-bottom:0.4rem;">{title}</div>
            <div style="font-family:'DM Sans',sans-serif; font-size:0.88rem; color:#bbb; line-height:1.7;">{text}</div>
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

st.info(
    "📌 **Conclusão:** O atraso logístico não é um problema operacional isolado. É uma ameaça sistêmica ao crescimento sustentável do negócio — que começa no frete e termina no balanço financeiro."
)

st.markdown("---")

# Sankey diagram
st.markdown("### 🌀 A Cadeia Completa de Causa e Efeito")

fig = go.Figure(
    go.Sankey(
        arrangement="snap",
        node=dict(
            pad=20,
            thickness=25,
            line=dict(color="rgba(108,99,255,0.5)", width=1),
            label=[
                "Concentração Logística\nno Sudeste",
                "Alto Custo de Frete\n(Norte/Nordeste)",
                "Atrasos na Entrega",
                "Baixa Satisfação (NPS↓)",
                "Churn de Clientes",
                "Aumento do CAC",
                "Queda no GMV",
            ],
            color=[
                "#6c63ff",
                "#ff6b6b",
                "#ff5050",
                "#ffd93d",
                "#ff5050",
                "#ff8c00",
                "#ff3030",
            ],
            x=[0.01, 0.25, 0.50, 0.65, 0.80, 0.80, 0.99],
            y=[0.3, 0.2, 0.5, 0.5, 0.3, 0.7, 0.5],
        ),
        link=dict(
            source=[0, 0, 1, 2, 3, 4, 3],
            target=[1, 2, 3, 3, 4, 6, 5],
            value=[35, 65, 60, 70, 85, 90, 60],
            color=[
                "rgba(108,99,255,0.15)",
                "rgba(255,107,107,0.15)",
                "rgba(255,107,107,0.2)",
                "rgba(255,80,80,0.2)",
                "rgba(255,80,80,0.25)",
                "rgba(255,48,48,0.25)",
                "rgba(255,140,0,0.2)",
            ],
        ),
    )
)
fig.update_layout(
    **PLOTLY_LAYOUT,
    title="Mapa de Impacto: Da Concentração Logística ao Custo de Negócio",
    height=380,
)
st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
proposta_box(" A resposta não é única. As próximas análises demonstram que a solução exige uma abordagem <strong>multidimensional</strong>: descentralização logística, incentivos de parcelamento, campanhas no horário de pico e monitoramento preditivo de atrasos via Machine Learning. ")
