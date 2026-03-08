"""
Módulo de utilitários de estilo para o Dashboard Radar.
Injeta CSS global, fontes Google e logo na sidebar.
"""
import streamlit as st
import base64
import os

LOGO_PATH = os.path.join(os.path.dirname(__file__), '..', 'public', 'Radar.svg')
FAVICON_PATH = os.path.join(os.path.dirname(__file__), '..', 'public', 'Radar.svg')


def load_svg_base64(path: str) -> str:
    """Carrega um arquivo SVG e retorna como base64."""
    try:
        with open(path, 'rb') as f:
            return base64.b64encode(f.read()).decode()
    except FileNotFoundError:
        return ""


def inject_global_css():
    """Injeta CSS global com fontes Google e customizações de UI."""
    st.markdown("""
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&family=DM+Sans:wght@300;400;500&display=swap" rel="stylesheet">

    <style>
        /* === TIPOGRAFIA === */
        html, body, [class*="css"] {
            font-family: 'DM Sans', sans-serif;
        }
        h1, h2, h3, h4, h5, h6 {
            font-family: 'Poppins', sans-serif !important;
            font-weight: 700 !important;
        }
        .stMarkdown h1 { font-size: 2.4rem; }
        .stMarkdown h2 { font-size: 1.8rem; }
        .stMarkdown h3 { font-size: 1.3rem; }

        /* === FUNDO COM GRADIENTE === */
        .stApp {
            background: linear-gradient(160deg, #00001f 0%, #0d0c68 50%, #00001f 100%);
            background-attachment: fixed;
        }

        /* === SIDEBAR === */
        [data-testid="stSidebar"] {
            background: rgba(13, 12, 104, 0.85) !important;
            backdrop-filter: blur(12px);
            border-right: 1px solid rgba(108, 99, 255, 0.3);
        }
        [data-testid="stSidebar"] .stMarkdown p,
        [data-testid="stSidebar"] label {
            color: #d9d9d9 !important;
        }
        [data-testid="stSidebarNav"] a span {
            font-family: 'DM Sans', sans-serif;
            font-size: 0.95rem;
        }

        /* === CARDS / MÉTRICAS === */
        [data-testid="stMetric"] {
            background: rgba(108, 99, 255, 0.12);
            border: 1px solid rgba(108, 99, 255, 0.3);
            border-radius: 12px;
            padding: 1rem 1.2rem;
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }
        [data-testid="stMetric"]:hover {
            transform: translateY(-3px);
            box-shadow: 0 8px 24px rgba(108, 99, 255, 0.25);
        }
        [data-testid="stMetricLabel"] {
            font-family: 'DM Sans', sans-serif !important;
            color: #aaa !important;
            font-size: 0.85rem;
        }
        [data-testid="stMetricValue"] {
            font-family: 'Poppins', sans-serif !important;
            font-size: 1.6rem !important;
            font-weight: 700 !important;
            color: #d9d9d9 !important;
        }

        /* === TÍTULO DE PÁGINA (h1) === */
        .page-title {
            font-family: 'Poppins', sans-serif;
            font-size: 2.5rem;
            font-weight: 800;
            background: linear-gradient(90deg, #6c63ff, #a89bff);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 0.2rem;
        }
        .page-subtitle {
            font-family: 'DM Sans', sans-serif;
            color: #aaa;
            font-size: 1rem;
            margin-top: 0;
            margin-bottom: 2rem;
        }

        /* === SEÇÃO DE INSIGHT/PROPOSTA === */
        .insight-card {
            background: rgba(108, 99, 255, 0.08);
            border-left: 4px solid #6c63ff;
            border-radius: 0 8px 8px 0;
            padding: 1rem 1.2rem;
            margin: 1rem 0;
        }
        .problema-card {
            background: rgba(255, 80, 80, 0.07);
            border-left: 4px solid #ff5050;
            border-radius: 0 8px 8px 0;
            padding: 1rem 1.2rem;
            margin: 1rem 0;
        }
        .proposta-card {
            background: rgba(0, 200, 130, 0.07);
            border-left: 4px solid #00c882;
            border-radius: 0 8px 8px 0;
            padding: 1rem 1.2rem;
            margin: 1rem 0;
        }
        .section-label {
            font-family: 'Poppins', sans-serif;
            font-size: 0.7rem;
            font-weight: 700;
            letter-spacing: 0.15em;
            text-transform: uppercase;
            opacity: 0.6;
            margin-bottom: 0.3rem;
        }

        /* === DIVISORES === */
        hr {
            border-color: rgba(108, 99, 255, 0.2) !important;
        }

        /* === BOTÕES === */
        .stButton button {
            background: linear-gradient(90deg, #6c63ff, #a89bff);
            color: white;
            border: none;
            font-family: 'Poppins', sans-serif;
            font-weight: 600;
            border-radius: 8px;
        }

        /* === PLOTLY CHART CONTAINER === */
        .js-plotly-plot .plotly {
            border-radius: 12px;
        }

        /* === INFO / WARNING Streamlit boxes === */
        .stAlert {
            border-radius: 10px;
        }
    </style>
    """, unsafe_allow_html=True)


def render_sidebar_logo():
    """Renderiza a logo na sidebar."""
    logo_b64 = load_svg_base64(LOGO_PATH)
    if logo_b64:
        st.sidebar.markdown(
            f"""
            <div style="
                display: flex;
                justify-content: center;
                padding: 1.5rem 0 1rem 0;
            ">
                <img src="data:image/svg+xml;base64,{logo_b64}"
                     style="width: 140px; filter: drop-shadow(0 0 12px rgba(108,99,255,0.5));"
                     alt="Radar Logo">
            </div>
            <hr style="border-color: rgba(108,99,255,0.3); margin-bottom: 1rem;">
            """,
            unsafe_allow_html=True
        )


def page_header(title: str, subtitle: str = ""):
    """Renderiza cabeçalho padronizado de página."""
    st.markdown(f'<p class="page-title">{title}</p>', unsafe_allow_html=True)
    if subtitle:
        st.markdown(f'<p class="page-subtitle">{subtitle}</p>', unsafe_allow_html=True)
    st.markdown("---")


def problema_box(text: str):
    """Renderiza um card de 'O Problema'."""
    st.markdown(f"""
    <div class="problema-card">
        <div class="section-label">🔴 O Problema</div>
        {text}
    </div>
    """, unsafe_allow_html=True)


def insight_box(text: str):
    """Renderiza um card de 'Insight'."""
    st.markdown(f"""
    <div class="insight-card">
        <div class="section-label">💡 Insight</div>
        {text}
    </div>
    """, unsafe_allow_html=True)


def proposta_box(text: str):
    """Renderiza um card de 'Proposta de Valor'."""
    st.markdown(f"""
    <div class="proposta-card">
        <div class="section-label">🚀 Proposta de Valor</div>
        {text}
    </div>
    """, unsafe_allow_html=True)


# Layout padrão de plotly para o tema escuro
PLOTLY_LAYOUT = dict(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(13, 12, 104, 0.3)',
    font=dict(family='DM Sans', color='#d9d9d9'),
    title_font=dict(family='Poppins', color='#d9d9d9', size=16),
    xaxis=dict(gridcolor='rgba(108,99,255,0.15)', zerolinecolor='rgba(108,99,255,0.2)'),
    yaxis=dict(gridcolor='rgba(108,99,255,0.15)', zerolinecolor='rgba(108,99,255,0.2)'),
    legend=dict(bgcolor='rgba(0,0,0,0.3)', bordercolor='rgba(108,99,255,0.3)', borderwidth=1),
    margin=dict(l=20, r=20, t=50, b=20),
    hoverlabel=dict(bgcolor='#0d0c68', font_family='DM Sans'),
)

ACCENT_COLORS = ['#6c63ff', '#a89bff', '#00c882', '#ff6b6b', '#ffd93d', '#4ecdc4']
