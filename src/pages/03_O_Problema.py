import streamlit as st
import plotly.graph_objects as go
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from style_utils import inject_global_css, render_sidebar_logo, page_header, problema_box, proposta_box, PLOTLY_LAYOUT
from utils import get_analytical_df

st.set_page_config(page_title="Olist - O peso do Atraso", page_icon=os.path.join(os.path.dirname(__file__), "..", "public", "Radar.svg"), layout="wide")
inject_global_css()
render_sidebar_logo()

page_header("❓ O Problema: O Peso do Atraso", "Por que a logística define o sucesso ou o fracasso no e-commerce")

# ── CONTEXTO ─────────────────────────────────────────────────────────────────
st.markdown(
    """
<div style="max-width:900px; font-family:'DM Sans',sans-serif; color:#c0c0c0; font-size:1rem; line-height:1.9;">
O Brasil tem um dos e-commerces que mais cresce no mundo. Mas cresce <em>apesar</em> da sua logística — não graças a ela.
</div>
""",
    unsafe_allow_html=True,
)

# ── DADOS PARA AS MÉTRICAS ───────────────────────────────────────────────────
df = get_analytical_df()
delayed_metrics = {"delayed": 0, "avg_score_delay": 0, "avg_score_ok": 0, "drop": 0}

if not df.empty:
    total = df["order_id"].nunique()
    delayed = df[df["flag_atraso"] == 1]["order_id"].nunique()
    avg_score_delay = df[df["flag_atraso"] == 1]["review_score"].mean()
    avg_score_ok = df[df["flag_atraso"] == 0]["review_score"].mean()
    delayed_metrics = {
        "delayed": delayed,
        "delayed_pct": (delayed / total * 100),
        "avg_score_delay": avg_score_delay,
        "diff": avg_score_ok - avg_score_delay,
        "drop": (avg_score_ok - avg_score_delay) / avg_score_ok * 100
    }

# ── DESAFIO 1: EXPERIÊNCIA E SATISFAÇÃO ───────────────────────────────────────
st.markdown("---")
col1, col2 = st.columns([1, 1], gap="large")

with col1:
    img_1 = os.path.join(os.path.dirname(__file__), "..", "..", "public", "imagem1")
    if os.path.exists(img_1):
        st.image(img_1, use_container_width=True)
    else:
        st.error("Imagem 1 não encontrada.")

with col2:
    st.markdown("### Desafio 1: Frustração Exponencial")
    st.markdown(
        """
    No e-commerce moderno, a entrega **é** o produto. O atraso não é percebido de forma linear: cada dia extra gera uma queda drástica na percepção de valor.
    """
    )
    
    m1, m2 = st.columns(2)
    m1.metric("Nota Média (C/ Atraso)", f"{delayed_metrics['avg_score_delay']:.1f} ⭐")
    m2.metric("Queda no NPS", f"{delayed_metrics['drop']:.1f}%", f"-{delayed_metrics['diff']:.1f} pts", delta_color="inverse")
    
    st.markdown(
        """
    - **Expectativa vs Realidade:** O atraso quebra o contrato de confiança.
    - **Detratores Ativos:** Notas 1 e 2 dominam os pedidos atrasados.
    """
    )

# ── DESAFIO 2: IMPACTO FINANCEIRO ───────────────────────────────────────────
st.markdown("---")
col3, col4 = st.columns([1, 1], gap="large")

with col3:
    st.markdown("### Desafio 2: Erosão das Margens")
    st.markdown(
        """
    O custo do atraso vai muito além de um cliente irritado. Ele ataca diretamente a lucratividade através de custos ocultos.
    """
    )
    
    st.markdown(
        """
    <div style="background: rgba(255,80,80,0.1); padding: 1rem; border-radius: 10px; border-left: 5px solid #ff5050; margin-bottom: 1rem;">
    <strong>1. Churn Imediato:</strong> Até 50% dos clientes não retornam após um primeiro atraso.
    </div>
    <div style="background: rgba(255,217,61,0.1); padding: 1rem; border-radius: 10px; border-left: 5px solid #ffd93d; margin-bottom: 1rem;">
    <strong>2. Logística Reversa:</strong> Cancelamentos tardios geram custos de frete sem receita compensatória.
    </div>
    <div style="background: rgba(255,107,107,0.1); padding: 1rem; border-radius: 10px; border-left: 5px solid #ff6b6b;">
    <strong>3. CAC Elevado:</strong> A má reputação exige mais marketing para converter novos usuários.
    </div>
    """,
        unsafe_allow_html=True
    )

with col4:
    img_2 = os.path.join(os.path.dirname(__file__), "..", "..", "public", "imagem2")
    if os.path.exists(img_2):
        st.image(img_2, use_container_width=True)
    else:
        st.error("Imagem 2 não encontrada.")

st.markdown("---")
proposta_box(" O objetivo deste projeto é identificar **onde**, **como** e **quem** mais sofre com estes atrasos para propor soluções que salvem a satisfação do cliente e a margem de contribuição. ")
