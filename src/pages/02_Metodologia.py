import streamlit as st
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from style_utils import inject_global_css, render_sidebar_logo, page_header

st.set_page_config(page_title="Olist - O peso do Atraso", page_icon=os.path.join(os.path.dirname(__file__), "..", "public", "Radar.svg"), layout="wide")
inject_global_css()
render_sidebar_logo()

page_header("🔬 Metodologia", "Como a análise foi conduzida — da origem ao insight")

st.markdown("""
### Etapas do Pipeline Analítico
A análise seguiu um processo estruturado em 5 fases, garantindo que cada conclusão fosse baseada em dados confiáveis.
""")

steimpacts = [
    (
        "📉",
        "Churn & LTV",
        "Clientes com atraso têm **30–50% menos probabilidade de recomprar**, destruindo o Lifetime Value.",
        "#ff5050",
    ),
    (
        "🔄",
        "Logística Reversa",
        "Atrasos elevam cancelamentos, gerando custos que frequentemente superam a margem do produto.",
        "#ffd93d",
    ),
    (
        "🗣️",
        "Reputação",
        "Detratores ativos aumentam o CAC futuro ao exigir mais investimento para limpar a imagem da marca.",
        "#ff6b6b",
    ),
]
steps = [
    ("1", "Coleta e Integração", "🗂️",
     "7 datasets CSV foram carregados e integrados via <strong>joins estruturais</strong> (inner/left merge com Pandas), criando uma visão única de 360° do pedido — do clique do cliente à avaliação pós-entrega.",
     "pd.merge, inner join, left join"),
    ("2", "Qualidade e Limpeza", "🧹",
     "Tratamento de valores nulos, conversão de datas e remoção de outliers via <strong>IQR (Intervalo Interquartil)</strong> para garantir que as médias de receita e frete não fossem distorcidas por casos extremos.",
     "IQR, to_datetime, dropna"),
    ("3", "Feature Engineering", "⚙️",
     "Criação de métricas derivadas: <code>tempo_entrega_real</code>, <code>flag_atraso</code>, <code>receita_liquida</code>, <code>ano_mes</code>, <code>dia_semana</code> e <code>hora_compra</code> — todas essenciais para as análises temporais e logísticas.",
     "dt.days, dt.to_period, .astype"),
    ("4", "Análise Exploratória", "🔍",
     "Geração de visualizações interativas com <strong>Plotly</strong> para identificar padrões, correlações e anomalias. Cada seção segue o ciclo: Problema → Gráfico → Insight → Proposta.",
     "Plotly Express, Graph Objects"),
    ("5", "Síntese Estratégica", "💡",
     "Consolidação dos insights em propostas de valor acionáveis e identificação de oportunidades de Machine Learning para evolução do projeto.",
     "K-Means, Regressão OLS, Cohort Analysis"),
]

for s in steps:
    num, title, icon, desc, tech = s
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
                {icon} {title}
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


# ── TEAM ───────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("### 👥 Nossa Equipe")
st.markdown(
    "<p style=\"font-family:'DM Sans',sans-serif; color:#888; font-size:0.9rem; margin-bottom:1.2rem;\">"
    "Analisado e desenvolvido por especialistas em dados da Turma NYX - Alpha Edtech.</p>",
    unsafe_allow_html=True,
)

members = [
    ("Davi Moura", "Análise Estratégica", "📅", "https://github.com/davims9"),
    ("Romulo Reis", "Insights de Mercado", "💡", "https://github.com/romulo.reis"),
    ("Fabily", "Insights de Mercado", "💡", "https://github.com/Fabily-Ideale"),
    ("Edvan Sabino", "Regionalidade", "🌎", "https://github.com/edvannps"),
    ("Nikolas Tesch", "Logística", "🚚", "https://github.com/NikolasTesch"),
    ("Samuel Veronezi", "Financeiro", "💰", "https://github.com/vicians"),
    ("Luis Gustavo", "Satisfação", "⭐", "https://github.com/vieiralg"),
]

m_cols = st.columns(len(members))
for i, (name, role, icon, url) in enumerate(members):
    with m_cols[i]:
        st.markdown(
            f"""
            <div style="text-align: center; background: rgba(108,99,255,0.05); border: 1px solid rgba(108,99,255,0.1); border-radius: 10px; padding: 10px;">
                <div style="font-size: 1.5rem;">{icon}</div>
                <div style="font-family:'Poppins',sans-serif; font-weight:700; font-size:0.75rem; color:#d9d9d9; margin-top:5px;">{name}</div>
                <a href="{url}" target="_blank" style="text-decoration:none; font-size:0.65rem; color:#6c63ff;">Profile</a>
            </div>
            """,
            unsafe_allow_html=True
        )
