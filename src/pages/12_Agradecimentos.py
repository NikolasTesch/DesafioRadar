import streamlit as st
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from style_utils import inject_global_css, render_sidebar_logo, page_header

st.set_page_config(
    page_title="Olist - O peso do Atraso",
    page_icon=os.path.join(os.path.dirname(__file__), "..", "public", "Radar.svg"),
    layout="wide"
)
inject_global_css()
render_sidebar_logo()

page_header("🙏 Agradecimentos", "Com gratidão por cada pessoa e recurso que tornaram isso possível")

# ── MENSAGEM PRINCIPAL ────────────────────────────────────────────────────────
st.markdown("""
<div style="max-width: 800px; text-align: center; margin: 1.5rem auto 2rem auto;">
    <p style="font-family:'DM Sans',sans-serif; font-size:1.05rem; color:#c0c0c0; line-height:1.9;">
        Este projeto é fruto da dedicação coletiva de uma equipe diversa, unida pela curiosidade sobre os dados
        e pelo desejo de transformar informação em impacto real. Cada análise, gráfico e proposta presente
        neste dashboard só foi possível graças ao apoio de pessoas e organizações excepcionais.
    </p>
</div>
""", unsafe_allow_html=True)

# ── AGRADECIMENTOS ────────────────────────────────────────────────────────────
thanks = [
    ("🎓", "Alpha Edtech", "Agradecemos à Alpha Edtech pela oportunidade ímpar de desenvolvimento profissional e aprendizado intensivo. A estrutura do programa, a qualidade dos mentores e o ambiente colaborativo foram fundamentais para que cada membro da equipe avançasse de forma significativa nas suas habilidades de análise de dados e desenvolvimento de software."),
    ("🤝", "Cummins", "Um agradecimento especial à Cummins, parceira e patrocinadora oficial da nossa jornada. O suporte institucional e o compromisso com o desenvolvimento de talentos em tecnologia e dados refletem os valores de inovação e impacto que buscamos em cada linha de código."),
]

for icon, title, text in thanks:
    st.markdown(f"""
    <div style="
        background: rgba(13,12,104,0.45);
        border: 1px solid rgba(108,99,255,0.25);
        border-radius: 16px;
        padding: 1.5rem 1.8rem;
        margin-bottom: 1.2rem;
        display: flex;
        gap: 1.5rem;
        align-items: flex-start;
        max-width: 900px;
    ">
        <div style="font-size:2.5rem; flex-shrink:0;">{icon}</div>
        <div>
            <div style="font-family:'Poppins',sans-serif; font-weight:700; font-size:1.05rem; color:#d9d9d9; margin-bottom:0.5rem;">{title}</div>
            <div style="font-family:'DM Sans',sans-serif; font-size:0.9rem; color:#bbb; line-height:1.8;">{text}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ── FONTES E RECURSOS ─────────────────────────────────────────────────────────
st.markdown("### 📚 Fontes e Recursos Utilizados")

sources = [
    ("📦", "[Kaggle Dataset — Olist Brazilian E-Commerce](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)", "Dataset principal com +100k pedidos, 7 tabelas inter-relacionadas cobrindo 2016–2018."),
    ("🗺️", "IBGE — Dados Geoespaciais do Brasil", "Utilizado como referência para análise regional e validação de estados e municípios brasileiros."),
    ("📊", "Streamlit Documentation", "Framework utilizado para construção do dashboard interativo e multi-página."),
    ("📈", "Plotly Python Library", "Biblioteca responsável por todas as visualizações interativas com suporte a tooltips e zoom."),
    ("🐼", "Pandas & NumPy", "Pilares do processamento, limpeza e transformação dos dados ao longo de todo o pipeline analítico."),
    ("🤖", "Scikit-learn & Statsmodels", "Utilizados para modelagem estatística, clustering K-Means e regressões OLS nos notebooks de experimentação."),
]

for icon, name, desc in sources:
    st.markdown(f"""
    <div style="
        display: flex; gap: 1rem; align-items: flex-start;
        padding: 0.7rem 0;
        border-bottom: 1px solid rgba(108,99,255,0.12);
    ">
        <span style="font-size: 1.2rem; flex-shrink:0;">{icon}</span>
        <div>
            <div style="font-family:'DM Sans',sans-serif; font-size:0.9rem; color:#d9d9d9;">{name}</div>
            <div style="font-family:'DM Sans',sans-serif; font-size:0.8rem; color:#888; margin-top:0.15rem;">{desc}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ── MENSAGEM INSPIRADORA ───────────────────────────────────────────────────────
st.markdown("""
<div style="
    text-align: center;
    padding: 2.5rem 1rem 1rem 1rem;
    max-width: 750px;
    margin: 0 auto;
">
    <p style="
        font-family: 'Poppins', sans-serif;
        font-size: 1.5rem;
        font-weight: 700;
        background: linear-gradient(90deg, #6c63ff, #a89bff, #00c882);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        line-height: 1.5;
        margin-bottom: 1rem;
    ">
        "Os dados não mentem. Mas precisam de alguém disposto a ouvi-los."
    </p>
    <p style="font-family:'DM Sans',sans-serif; font-size:0.95rem; color:#888; line-height:1.7;">
        O verdadeiro poder dos dados não está nos números — está na capacidade de transformá-los em
        <strong style="color:#a89bff;">decisões melhores</strong>, em <strong style="color:#a89bff;">produtos mais justos</strong>
        e em <strong style="color:#a89bff;">experiências mais humanas</strong>.
        Que este trabalho inspire outros a olharem para os dados como uma ferramenta de empatia, não apenas de eficiência.
    </p>
    <div style="margin-top: 2rem; font-family:'DM Sans',sans-serif; font-size:0.85rem; color:#555; letter-spacing:0.05em;">
        Desenvolvido com 💜 pela <strong style="color:#6c63ff;">Equipe 4 · Turma 7 (NYX)</strong> · Alpha Edtech · 2026
    </div>
</div>
""", unsafe_allow_html=True)
