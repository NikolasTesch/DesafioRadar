import streamlit as st
import sys, os
import base64 # Added for base64 encoding of images

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from style_utils import inject_global_css, render_sidebar_logo, page_header

st.set_page_config(
    page_title="Olist - Agradecimentos",
    page_icon=os.path.join(os.path.dirname(__file__), "..", "public", "Radar.svg"),
    layout="wide"
)
inject_global_css()
render_sidebar_logo()

page_header("🙏 Agradecimentos", "Reconhecimento aos parceiros e recursos do projeto")

# ── MENSAGEM PRINCIPAL ────────────────────────────────────────────────────────
st.markdown("""
<div style="max-width: 800px; text-align: center; margin: 0.5rem auto 1.5rem auto;">
    <p style="font-family:'DM Sans',sans-serif; font-size:1rem; color:#c0c0c0; line-height:1.6;">
        Este trabalho é o resultado de uma jornada de aprendizado intensivo e colaboração. 
        Agradecemos imensamente às organizações que viabilizaram este desenvolvimento.
    </p>
</div>
""", unsafe_allow_html=True)

# Helper function to get base64 image
def get_image_base64(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode('utf-8')
    return "" # Return empty string if file not found

# ── AGRADECIMENTOS EM COLUNAS ──────────────────────────────────────────────────
col_alpha, col_cummins = st.columns(2, gap="large")

with col_alpha:
    logo_alpha_path = os.path.join(os.path.dirname(__file__), "..", "..", "public", "logo_alpha.png")
    logo_alpha_base64 = get_image_base64(logo_alpha_path)
    st.markdown(f"""
    <div style="background: rgba(13,12,104,0.45); border: 1px solid rgba(108,99,255,0.25); border-radius: 16px; padding: 1.5rem; height: 320px; text-align: center;">
        <img src="data:image/png;base64,{logo_alpha_base64}" style="margin-bottom: 1rem; border-radius: 8px; width: 120px;">
        <h3 style="color:#d9d9d9; font-family:'Poppins', sans-serif; font-size: 1.1rem; margin-top: 10px;">Alpha Edtech</h3>
        <p style="color:#aaa; font-family:'DM Sans', sans-serif; font-size: 0.88rem; line-height: 1.6;">
            Pela oportunidade de formação intensiva, mentoria de excelência e por fomentar um ambiente de inovação e aprendizado prático em dados.
        </p>
    </div>
    """, unsafe_allow_html=True)

with col_cummins:
    logo_cummins_path = os.path.join(os.path.dirname(__file__), "..", "..", "public", "logo_cummins.png")
    logo_cummins_base64 = get_image_base64(logo_cummins_path)
    st.markdown(f"""
    <div style="background: rgba(13,12,104,0.45); border: 1px solid rgba(108,99,255,0.25); border-radius: 16px; padding: 1.5rem; height: 320px; text-align: center;">
        <img src="data:image/png;base64,{logo_cummins_base64}" style="margin-bottom: 1rem; border-radius: 8px; width: 120px;">
        <h3 style="color:#d9d9d9; font-family:'Poppins', sans-serif; font-size: 1.1rem; margin-top: 10px;">Cummins</h3>
        <p style="color:#aaa; font-family:'DM Sans', sans-serif; font-size: 0.88rem; line-height: 1.6;">
            Pelo patrocínio estratégico e compromisso com o desenvolvimento de talentos tech, impulsionando a cultura de dados na prática.
        </p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ── FONTES E RECURSOS (RESUMIDO) ──────────────────────────────────────────────
st.markdown("### 📚 Fontes e Ferramentas")

col_src1, col_src2 = st.columns(2)

with col_src1:
    st.markdown("🎯 **[Kaggle Dataset — Olist](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)** (+100k pedidos)")
    st.markdown("🗺️ **IBGE** (Dados Geoespaciais)")

with col_src2:
    st.markdown("📊 **Streamlit & Plotly** (Interface e Visuais)")
    st.markdown("🐼 **Pandas & NumPy** (Pipeline de Dados)")

st.markdown("---")

# ── MENSAGEM FINAL ────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align: center; padding: 1rem;">
    <p style="font-family: 'Poppins', sans-serif; font-size: 1.3rem; font-weight: 700; background: linear-gradient(90deg, #6c63ff, #00c882); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
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