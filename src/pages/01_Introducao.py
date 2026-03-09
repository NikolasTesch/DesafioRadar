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
    ### O que é o projeto?
    O projeto propõe uma análise profunda do dataset de e-commerce da Olist, com o objetivo de
    **traduzir dados em insights estratégicos** e entender o real impacto de variáveis logísticas no negócio.

    A missão é clara: **compreender o comportamento dos dados** e extrair inteligência real para apoiar a tomada
    de decisão em marketplaces de alta complexidade.

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
        background: rgba(108,99,255,0.08);
        border: 1px solid rgba(108,99,255,0.2);
        border-radius: 16px;
        padding: 1.8rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    ">
        <div style="font-family:'Poppins',sans-serif; font-weight:700; font-size:1.1rem; margin-bottom:1.2rem; color:#a89bff; text-align:center;">
            📊 Panorama do Dataset
        </div>
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px;">
            <div style="text-align: center; padding: 10px; background: rgba(255,255,255,0.03); border-radius: 8px;">
                <div style="font-size: 1.2rem; font-weight: 700; color: #fff;">~100k</div>
                <div style="font-size: 0.7rem; color: #888;">Pedidos</div>
            </div>
            <div style="text-align: center; padding: 10px; background: rgba(255,255,255,0.03); border-radius: 8px;">
                <div style="font-size: 1.2rem; font-weight: 700; color: #fff;">~99k</div>
                <div style="font-size: 0.7rem; color: #888;">Clientes</div>
            </div>
            <div style="text-align: center; padding: 10px; background: rgba(255,255,255,0.03); border-radius: 8px;">
                <div style="font-size: 1.2rem; font-weight: 700; color: #fff;">~3k</div>
                <div style="font-size: 0.7rem; color: #888;">Sellers</div>
            </div>
            <div style="text-align: center; padding: 10px; background: rgba(255,255,255,0.03); border-radius: 8px;">
                <div style="font-size: 1.2rem; font-weight: 700; color: #fff;">27</div>
                <div style="font-size: 0.7rem; color: #888;">Estados</div>
            </div>
        </div>
        <div style="margin-top: 1.2rem; font-size: 0.85rem; color: #ccc; text-align: center; font-family: 'DM Sans', sans-serif;">
            🗓️ <strong>Período:</strong> 2016 – 2018<br>
            📦 <strong>Produtos:</strong> ~33k SKUs
        </div>
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
            <div style="font-family:'Poppins',sans-serif; font-weight:700; font-size:1.1rem; color:#a89bff;">{title}</div>
            <div style="font-family:'DM Sans',sans-serif; font-size:0.85rem; color:#bbb; margin-top:0.3rem;">{desc}</div>
        </div>
        """,
            unsafe_allow_html=True,
        )
