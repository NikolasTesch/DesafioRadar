import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from style_utils import inject_global_css, render_sidebar_logo, page_header, problema_box, insight_box, proposta_box, PLOTLY_LAYOUT

st.set_page_config(page_title="Olist - O peso do Atraso", page_icon=os.path.join(os.path.dirname(__file__), "..", "public", "Radar.svg"), layout="wide")
inject_global_css()
render_sidebar_logo()

page_header("🤖 Propostas de Machine Learning", "Próximos passos preditivos e de clusterização")

st.markdown("""
<p style="font-family:'DM Sans',sans-serif; color:#aaa; font-size:1rem; max-width:800px; line-height:1.8;">
A análise exploratória revelou padrões robustos que podem ser amplificados com modelos de Machine Learning.
Esta seção documenta os <strong>próximos passos técnicos</strong> para transformar o dashboard descritivo em
uma ferramenta preditiva de alto valor.
</p>
""", unsafe_allow_html=True)

st.markdown("---")

ml_proposals = [
    {
        "icon": "🔮",
        "title": "Predição de Atraso de Entrega",
        "type": "Classificação Binária",
        "type_color": "#6c63ff",
        "target": "flag_atraso (0/1)",
        "features": "customer_state, freight_value, seller_state, product_weight, dia_semana, mes, ano_mes",
        "models": "Random Forest, XGBoost, LightGBM",
        "metric": "F1-Score (foco em Recall para evitar falsos negativos)",
        "value": "Avisar proativamente clientes em risco de atraso, reduzindo o impacto no NPS antes que o problema ocorra.",
    },
    {
        "icon": "🎯",
        "title": "Predição de Review Score (NPS Predictor)",
        "type": "Regressão / Classificação",
        "type_color": "#00c882",
        "target": "review_score (1–5) ou binário: score >= 4",
        "features": "flag_atraso, freight_value, tempo_entrega_real, payment_installments, product_category_name",
        "models": "OLS (baseline), Gradient Boosting, Regressão Logística",
        "metric": "RMSE para regressão | AUC-ROC para classificação",
        "value": "Simular o impacto de mudanças operacionais (ex: reduzir o frete em 20%) na nota esperada, guiando decisões de investimento.",
    },
    {
        "icon": "🗺️",
        "title": "Segmentação de Clientes por Comportamento",
        "type": "Clusterização (Não Supervisionado)",
        "type_color": "#ffd93d",
        "target": "Segmentos de comportamento de compra",
        "features": "frequencia, recencia, ticket_medio, categoria_preferida, sensibilidade_frete",
        "models": "K-Means (k=4–6), DBSCAN, Agrupamento Hierárquico",
        "metric": "Silhouette Score, Inertia, interpretabilidade dos clusters",
        "value": "Personalizar comunicação, ofertas e SLA logístico por perfil de cliente — da base do funil ao cliente VIP.",
    },
    {
        "icon": "📦",
        "title": "Previsão de Demanda por Categoria (Forecasting)",
        "type": "Série Temporal",
        "type_color": "#4ecdc4",
        "target": "volume_pedidos por categoria por mês",
        "features": "lags temporais, sazonalidade anual, flag Black Friday, tendência linear",
        "models": "Prophet (Meta), ARIMA, LSTM (para categorias de alto volume)",
        "metric": "MAPE (Mean Absolute Percentage Error)",
        "value": "Planejar estoque e capacidade logística com antecedência, especialmente para picos sazonais como Black Friday.",
    },
]

for p in ml_proposals:
    st.markdown(f"""
    <div style="
        background: rgba(13,12,104,0.5);
        border: 1px solid rgba(108,99,255,0.2);
        border-radius: 16px;
        padding: 1.5rem 1.8rem;
        margin-bottom: 1.2rem;
    ">
        <div style="display:flex; align-items:center; gap:1rem; margin-bottom:1rem;">
            <span style="font-size:2rem;">{p['icon']}</span>
            <div>
                <div style="font-family:'Poppins',sans-serif; font-weight:700; font-size:1.1rem; color:#d9d9d9;">{p['title']}</div>
                <span style="background:{p['type_color']}22; border:1px solid {p['type_color']}88; color:{p['type_color']}; border-radius:20px; padding:0.12rem 0.7rem; font-size:0.72rem; font-family:'DM Sans',sans-serif; font-weight:700;">
                    {p['type']}
                </span>
            </div>
        </div>
        <div style="display:grid; grid-template-columns: 1fr 1fr; gap:0.8rem;">
            <div style="font-family:'DM Sans',sans-serif; font-size:0.85rem; color:#bbb;">
                🎯 <strong style="color:#d9d9d9;">Target:</strong><br><code style="color:#a89bff;">{p['target']}</code>
            </div>
            <div style="font-family:'DM Sans',sans-serif; font-size:0.85rem; color:#bbb;">
                📐 <strong style="color:#d9d9d9;">Métrica de Avaliação:</strong><br><code style="color:#00c882;">{p['metric']}</code>
            </div>
            <div style="font-family:'DM Sans',sans-serif; font-size:0.85rem; color:#bbb; grid-column: span 2;">
                🔧 <strong style="color:#d9d9d9;">Features Principais:</strong><br><code style="color:#ffd93d; font-size:0.8rem;">{p['features']}</code>
            </div>
            <div style="font-family:'DM Sans',sans-serif; font-size:0.85rem; color:#bbb;">
                🤖 <strong style="color:#d9d9d9;">Modelos:</strong> {p['models']}
            </div>
            <div style="font-family:'DM Sans',sans-serif; font-size:0.85rem; color:#00c882;">
                💡 <strong>Valor:</strong> {p['value']}
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")
st.markdown("### 📊 Mapa de Prioridade dos Projetos de ML")

# Radar chart de impacto vs complexidade
categories = ['Impacto no NPS', 'Complexidade\nde Implementação', 'Dados\nDisponíveis',
               'Velocidade p/ Produção', 'ROI Estimado']

fig_radar = go.Figure()
colors_ml = ['#6c63ff', '#00c882', '#ffd93d', '#4ecdc4']
projects = [
    ("Predição de Atraso", [90, 60, 95, 80, 88]),
    ("NPS Predictor", [85, 55, 90, 85, 82]),
    ("Segmentação de Clientes", [75, 50, 80, 70, 78]),
    ("Forecasting de Demanda", [70, 80, 75, 55, 72]),
]

for (name, vals), color in zip(projects, colors_ml):
    fig_radar.add_trace(go.Scatterpolar(
        r=vals + [vals[0]],
        theta=categories + [categories[0]],
        fill='toself',
        fillcolor=color.replace('#', 'rgba(') + ',0.1)' if color.startswith('#') else color,
        line=dict(color=color, width=2),
        name=name
    ))

fig_radar.update_layout(
    **PLOTLY_LAYOUT,
    polar=dict(
        radialaxis=dict(visible=True, range=[0, 100], gridcolor='rgba(108,99,255,0.2)', color='#888'),
        angularaxis=dict(gridcolor='rgba(108,99,255,0.2)', color='#d9d9d9'),
        bgcolor='rgba(13,12,104,0.3)',
    ),
    title="Matriz de Avaliação dos Projetos de ML (0–100)",
    height=500,
)
st.plotly_chart(fig_radar, use_container_width=True)

proposta_box("O ponto de partida recomendado é a <strong>Predição de Atraso</strong> — maior impacto no NPS, dados já disponíveis e pipeline relativamente simples. Em paralelo, a <strong>Segmentação de Clientes</strong> pode ser implementada usando as features já geradas neste projeto.")
