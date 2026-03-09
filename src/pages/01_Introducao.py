import streamlit as st
import sys, os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from style_utils import inject_global_css, render_sidebar_logo, page_header

st.set_page_config(page_title="Olist - O peso do Atraso", page_icon=os.path.join(os.path.dirname(__file__), "..", "public", "Radar.svg"), layout="wide")
inject_global_css()
render_sidebar_logo()

page_header("📖 Introdução", "Contexto do projeto e do dataset Olist")

col_a, col_b = st.columns([3, 2])

with col_a:
    st.markdown("""
    ### O que é o Desafio Radar?
    O **Desafio Radar** é uma iniciativa de análise exploratória e estratégica conduzida para extrair
    **inteligência de negócio** real do maior dataset público de e-commerce brasileiro.

    A missão da equipe foi clara: **transformar dados brutos em decisões de alto impacto**, respondendo
    às perguntas que os gestores de um marketplace realmente precisam responder antes de investir.

    ---
    ### 🏢 Sobre a Olist
    A **Olist** é um marketplace que conecta pequenos comerciantes a grandes plataformas de vendas (como
    Mercado Livre, B2W e Americanas). Ela opera como intermediária logística e de pagamentos,
    sendo responsável pelos dados que analisamos aqui.
    """)

with col_b:
    st.markdown(
        """
    <div style="
        background: rgba(108,99,255,0.1);
        border: 1px solid rgba(108,99,255,0.3);
        border-radius: 14px;
        padding: 1.5rem;
    ">
        <div style="font-family:'Poppins',sans-serif; font-weight:700; font-size:1rem; margin-bottom:1rem; color:#d9d9d9;">
            📊 Sobre o Dataset
        </div>
        <ul style="font-family:'DM Sans',sans-serif; color:#ccc; line-height:2; list-style:none; padding:0;">
            <li>🗓️ <strong>Período:</strong> 2016 – 2018</li>
            <li>📦 <strong>Pedidos:</strong> ~100.000</li>
            <li>🛍️ <strong>Produtos:</strong> ~33.000 SKUs</li>
            <li>🧑 <strong>Clientes únicos:</strong> ~99.000</li>
            <li>🏪 <strong>Vendedores:</strong> ~3.000</li>
            <li>📍 <strong>Estados:</strong> 27 UFs</li>
            <li>🗂️ <strong>Tabelas:</strong> 7 datasets integrados</li>
        </ul>
    </div>
    """,
        unsafe_allow_html=True,
    )

st.markdown("---")

st.markdown("### 🎯 Perguntas que Guiam esta Análise")
q_cols = st.columns(3)
questions = [
    (
        "🚚",
        "Logística",
        "Quanto o tempo de entrega impacta o NPS e a retenção de clientes?",
    ),
    (
        "💰",
        "Financeiro",
        "Qual o impacto real do frete no ticket médio e na conversão?",
    ),
    ("🌎", "Regional", "Quais estados concentram os maiores gargalos logísticos?"),
    ("📅", "Sazonalidade", "Como eventos como a Black Friday estressam a operação?"),
    (
        "⭐",
        "Satisfação",
        "Quais categorias são mais detratoras da experiência do cliente?",
    ),
    ("💳", "Pagamentos", "Como o parcelamento influencia o valor médio do pedido?"),
]
for i, (icon, title, desc) in enumerate(questions):
    with q_cols[i % 3]:
        st.markdown(
            f"""
        <div style="border:1px solid rgba(108,99,255,0.2); border-radius:10px; padding:1rem; margin-bottom:0.8rem; background:rgba(108,99,255,0.05);">
            <div style="font-size:1.5rem;">{icon}</div>
            <div style="font-family:'Poppins',sans-serif; font-weight:700; font-size:0.9rem; color:#a89bff;">{title}</div>
            <div style="font-family:'DM Sans',sans-serif; font-size:0.85rem; color:#bbb; margin-top:0.3rem;">{desc}</div>
        </div>
        """,
            unsafe_allow_html=True,
        )
