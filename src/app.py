import streamlit as st
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from style_utils import (
    inject_global_css,
    render_sidebar_logo,
    page_header,
    ACCENT_COLORS,
)
from utils import get_analytical_df

st.set_page_config(
    page_title="Olist - O peso do Atraso",
    page_icon=os.path.join(os.path.dirname(__file__), "..", "public", "Radar.svg"),
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_global_css()
render_sidebar_logo()

# Sidebar nav label
st.sidebar.markdown(
    "<p style=\"font-family:'Poppins',sans-serif; font-size:0.7rem; letter-spacing:0.15em; color:#6c63ff; text-transform:uppercase; font-weight:700; padding: 0 0 0.5rem 0;\">Navegação</p>",
    unsafe_allow_html=True,
)

# ── HERO ──────────────────────────────────────────────
st.markdown(
    """
<div style="text-align: center; padding: 3rem 0 2rem 0;">
    <p style="
        font-family: 'Poppins', sans-serif;
        font-size: 3.2rem;
        font-weight: 800;
        background: linear-gradient(90deg, #6c63ff, #a89bff, #00c882);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        line-height: 1.2;
        margin: 0;
    ">Olist - O peso do Atraso</p>
    <p style="
        font-family: 'DM Sans', sans-serif;
        font-size: 1.2rem;
        color: #aaa;
        margin-top: 0.5rem;
    ">Inteligência Estratégica no E-commerce Olist</p>
</div>
""",
    unsafe_allow_html=True,
)

# ── KPIs RÁPIDOS ──────────────────────────────────────
with st.spinner("Carregando base analítica..."):
    df = get_analytical_df()

if not df.empty:
    total_pedidos = df["order_id"].nunique()
    gmv = df["receita_liquida"].sum()
    avg_score = df["review_score"].mean()
    delay_rate = df["flag_atraso"].mean()

    st.markdown("---")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("📦 Total de Pedidos", f"{total_pedidos:,}")
    col2.metric("💰 GMV Total", f"R$ {gmv / 1e6:.1f}M")
    col3.metric("⭐ Nota Média", f"{avg_score:.2f} / 5")
    col4.metric("⚠️ Taxa de Atraso", f"{delay_rate * 100:.1f}%")

    st.markdown("---")

# ── INTRO NARRATIVE ───────────────────────────────────
st.markdown(
    """
<div style="max-width: 860px; margin: 0 auto; text-align: center; padding: 1rem 0 2rem 0;">
    <h2 style="font-family: 'Poppins', sans-serif; font-weight: 700; font-size: 1.7rem; color: #d9d9d9;">
        Navegue pelas análises no menu lateral
    </h2>
    <p style="font-family: 'DM Sans', sans-serif; font-size: 1rem; color: #aaa; line-height: 1.8;">
        Este dashboard consolida a análise exploratória completa do ecossistema Olist —
        cobrindo <strong>logística</strong>, <strong>regionalidade</strong>, <strong>satisfação</strong>,
        <strong>finanças</strong> e <strong>sazonalidade</strong> — com foco em gerar
        <em>insights acionáveis</em> e propostas de melhoria concretas.
    </p>
</div>
""",
    unsafe_allow_html=True,
)

# ── CARDS DE NAVEGAÇÃO ────────────────────────────────
pages = [
    ("📖", "Introdução", "Contexto do projeto e do dataset Olist", "01_Introducao"),
    ("🔬", "Metodologia", "Como a análise foi conduzida", "02_Metodologia"),
    ("❓", "O Problema", "A dor de negócio central investigada", "03_O_Problema"),
    (
        "🧹",
        "Qualidade dos Dados",
        "Saneamento e completitude",
        "04_Qualidade_dos_Dados",
    ),
    ("🌎", "Regionalidade", "Impacto geográfico no e-commerce", "05_Regionalidade"),
    ("🚚", "Logística", "Performance de entrega e last-mile", "06_Logistica_e_Entrega"),
    (
        "⭐",
        "Satisfação",
        "NPS, categorias e percepção de valor",
        "07_Satisfacao_do_Cliente",
    ),
    (
        "💰",
        "Financeiro",
        "GMV, ticket médio e pagamentos",
        "08_Financeiro_e_Pagamentos",
    ),
    ("📅", "Sazonalidade", "Tendências temporais e Black Friday", "09_Sazonalidade"),
    ("🏆", "Propostas Globais", "Soluções consolidadas", "10_Propostas_Globais"),
    ("🤖", "Machine Learning", "Próximos passos preditivos", "11_Machine_Learning"),
]

cols = st.columns(3)
for i, (icon, title, desc, _) in enumerate(pages):
    with cols[i % 3]:
        st.markdown(
            f"""
        <div style="
            background: rgba(108, 99, 255, 0.09);
            border: 1px solid rgba(108, 99, 255, 0.25);
            border-radius: 14px;
            padding: 1.2rem 1.2rem 1rem 1.2rem;
            margin-bottom: 1rem;
            transition: transform 0.2s ease;
        ">
            <div style="font-size: 2rem; margin-bottom: 0.4rem;">{icon}</div>
            <div style="font-family: 'Poppins', sans-serif; font-weight: 700; font-size: 1rem; color: #d9d9d9;">{title}</div>
            <div style="font-family: 'DM Sans', sans-serif; font-size: 0.85rem; color: #888; margin-top: 0.2rem;">{desc}</div>
        </div>
        """,
            unsafe_allow_html=True,
        )

st.markdown(
    """
<div style="text-align: center; margin-top: 2rem; padding-bottom: 1rem;">
    <p style="font-family:'DM Sans',sans-serif; font-size:0.8rem; color:#555;">
        Desenvolvido por <strong style="color:#6c63ff;">Equipe 4 (Turma NYX)</strong> · Dataset: Olist Brazilian E-Commerce
    </p>
</div>
""",
    unsafe_allow_html=True,
)
