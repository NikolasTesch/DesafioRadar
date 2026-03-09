import streamlit as st
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from style_utils import (
    inject_global_css,
    render_sidebar_logo,
    page_header,
    load_image_base64,
)

st.set_page_config(
    page_title="Olist - O peso do Atraso",
    page_icon=os.path.join(
        os.path.dirname(__file__), "..", "..", "public", "Radar.svg"
    ),
    layout="wide",
)
inject_global_css()
render_sidebar_logo()

page_header("🔬 Metodologia", "Como a análise foi conduzida — da origem ao insight")

st.markdown("### Nossa Equipe")
st.markdown(
    "<p style=\"font-family:'DM Sans',sans-serif; color:#888; font-size:0.9rem; margin-bottom:1.2rem;\">"
    "Desenvolvido por estudantes da Turma 7 (NYX) da Alpha Edtech.</p>",
    unsafe_allow_html=True,
)

# Mapping members to their local profiles and photos
PUBLIC_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "public")

members = [
    ("Davi Moura", "davims9", "DAVI.png"),
    ("Romulo Reis", "romulo.reis", "ROMULO.png"),
    ("Fabily", "Fabily-Ideale", "FABILY.jpg"),
    ("Edvan Sabino", "edvannps", "edvan.png"),
    ("Nikolas Tesch", "NikolasTesch", "NIKOLAS.png"),
    ("Samuel Veronezi", "vicians", "SAMUEL.jpg"),
    ("Luis Gustavo", "vieiralg", "LUIS.png"),
]

cols = st.columns(4)
for i, (name, handle, filename) in enumerate(members):
    with cols[i % 4]:
        github_url = f"https://github.com/{handle.lstrip('/')}"
        photo_path = os.path.join(PUBLIC_DIR, filename)
        photo_b64 = load_image_base64(photo_path)

        # Determine image format (png/jpg)
        ext = filename.split(".")[-1].lower()
        mime = f"image/{'jpeg' if ext == 'jpg' else ext}"
        img_src = f"data:{mime};base64,{photo_b64}" if photo_b64 else ""

        st.markdown(
            f"""
        <a href="{github_url}" target="_blank" style="text-decoration:none;">
        <div style="
            background: rgba(108,99,255,0.08);
            border: 1px solid rgba(108,99,255,0.25);
            border-radius: 14px;
            padding: 1.5rem 0.8rem;
            margin-bottom: 0.9rem;
            text-align: center;
            transition: transform 0.2s ease, box-shadow 0.2s ease;
            cursor: pointer;
        ">
            <img src="{img_src}" style="width: 80px; height: 80px; border-radius: 50%; border: 2px solid rgba(108,99,255,0.5); object-fit: cover; margin-bottom: 0.8rem;">
            <div style="font-family:'Poppins',sans-serif; font-weight:700; font-size:0.88rem; color:#d9d9d9;">{name}</div>
            <div style="font-family:'DM Sans',sans-serif; font-size:0.75rem; color:#888; margin-top:0.2rem;">@{handle.lstrip("/")}</div>
            <div style="font-family:'DM Sans',sans-serif; font-size:0.72rem; color:#6c63ff; margin-top:0.6rem;">
                🔗 Perfil GitHub
            </div>
        </div>
        </a>
        """,
            unsafe_allow_html=True,
        )


st.markdown("""
### Etapas do Pipeline Analítico
A análise seguiu um processo estruturado em 5 fases, garantindo que cada conclusão fosse baseada em dados confiáveis.
""")

steps = [
    ("1", "Coleta e Integração",
     "7 datasets CSV foram carregados e integrados via <strong>joins estruturais</strong> (inner/left merge com Pandas), criando uma visão única de 360° do pedido — do clique do cliente à avaliação pós-entrega.",
     "pd.merge, inner join, left join"),
    ("2", "Qualidade e Limpeza",
     "Tratamento de valores nulos, conversão de datas e remoção de outliers via <strong>IQR (Intervalo Interquartil)</strong> para garantir que as médias de receita e frete não fossem distorcidas por casos extremos.",
     "IQR, to_datetime, dropna"),
    ("3", "Feature Engineering",
     "Criação de métricas derivadas: <code>tempo_entrega_real</code>, <code>flag_atraso</code>, <code>receita_liquida</code>, <code>ano_mes</code>, <code>dia_semana</code> e <code>hora_compra</code> — todas essenciais para as análises temporais e logísticas.",
     "dt.days, dt.to_period, .astype"),
    ("4", "Análise Exploratória",
     "Geração de visualizações interativas com <strong>Plotly</strong> para identificar padrões, correlações e anomalias. Cada seção segue o ciclo: Problema → Gráfico → Insight → Proposta.",
     "Plotly Express, Graph Objects"),
    ("5", "Síntese Estratégica",
     "Consolidação dos insights em propostas de valor acionáveis e identificação de oportunidades de Machine Learning para evolução do projeto.",
     "K-Means, Regressão OLS, Cohort Analysis"),
]

for s in steps:
    num, title, desc, tech = s
    st.markdown(f"""
    <div style="
        display: flex;
        gap: 1.5rem;
        align-items: flex-start;
        background: rgba(13,12,104,0.4);
        border: 1px solid rgba(108,99,255,0.2);
        border-radius: 14px;
        padding: 1.2rem 1.5rem;
        margin-bottom: 1rem;
    ">
        <div style="
            background: linear-gradient(135deg, #6c63ff, #a89bff);
            color: white;
            font-family: 'Poppins', sans-serif;
            font-weight: 800;
            font-size: 1.3rem;
            min-width: 48px;
            height: 48px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            flex-shrink: 0;
        ">{num}</div>
        <div>
            <div style="font-family:'Poppins',sans-serif; font-weight:700; font-size:1rem; color:#d9d9d9;">
            {title}
            </div>
            <div style="font-family:'DM Sans',sans-serif; font-size:0.9rem; color:#bbb; margin-top:0.3rem; line-height:1.6;">
                {desc}
            </div>
            <div style="margin-top:0.5rem;">
                <span style="background:rgba(108,99,255,0.2); border:1px solid rgba(108,99,255,0.4); border-radius:20px; padding:0.2rem 0.7rem; font-family:'DM Sans',sans-serif; font-size:0.75rem; color:#a89bff;">
                    🛠️ {tech}
                </span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


