import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from style_utils import inject_global_css, render_sidebar_logo, page_header, problema_box, insight_box, proposta_box, PLOTLY_LAYOUT, ACCENT_COLORS

st.set_page_config(
    page_title="Olist - Machine Learning",
    page_icon=os.path.join(os.path.dirname(__file__), "..", "public", "Radar.svg"),
    layout="wide"
)
inject_global_css()
render_sidebar_logo()

page_header("🤖 Machine Learning", "Modelos preditivos e de classificação para o e-commerce Olist")

# ── Introdução ──────────────────────────────────────────────────────────────
st.markdown("""
<p style="font-family:'DM Sans',sans-serif; color:#aaa; font-size:1rem; max-width:860px; line-height:1.8;">
A análise exploratória revelou padrões robustos que sustentam a aplicação de Machine Learning.
Esta seção apresenta <strong>o que são os modelos propostos</strong>, como funcionam e qual o valor
que cada um gera para a operação da Olist — da predição de atrasos à segmentação de clientes.
</p>
""", unsafe_allow_html=True)

st.markdown("---")

# ── O que é Machine Learning ─────────────────────────────────────────────
st.markdown("### 🧠 O que é Machine Learning?")

col_a, col_b = st.columns([1, 1], gap="large")

with col_a:
    st.markdown("""
    <div style="
        background: rgba(13,12,104,0.5);
        border: 1px solid rgba(108,99,255,0.2);
        border-radius: 16px;
        padding: 1.5rem 1.8rem;
    ">
        <div style="font-family:'Poppins',sans-serif; font-weight:700; color:#d9d9d9; font-size:1rem; margin-bottom:0.8rem;">
            📖 Definição Simples
        </div>
        <p style="font-family:'DM Sans',sans-serif; color:#bbb; font-size:0.9rem; line-height:1.8;">
            Machine Learning é ensinar o computador a <strong style="color:#a89bff;">aprender com exemplos do passado</strong>
            para prever o futuro — sem programar regra por regra manualmente.
        </p>
        <p style="font-family:'DM Sans',sans-serif; color:#bbb; font-size:0.9rem; line-height:1.8; margin-top:0.8rem;">
            É como um funcionário experiente que já viu milhares de pedidos e consegue dizer:
            <em style="color:#ffd93d;">"Esse aqui tem tudo para atrasar"</em> — porque reconhece o padrão.
            O modelo faz o mesmo, mas analisando 100.000 pedidos de uma vez.
        </p>
    </div>
    """, unsafe_allow_html=True)

with col_b:
    # Funil visual: dados → modelo → previsão
    fig_funil = go.Figure(go.Funnel(
        y=["Dados Históricos<br>(100k pedidos)", "Feature Engineering<br>(variáveis relevantes)",
           "Treinamento<br>(o modelo aprende)", "Validação<br>(testa com dados novos)", "Previsão em Produção"],
        x=[100, 80, 60, 45, 30],
        textinfo="label",
        marker=dict(color=["#6c63ff", "#7c74ff", "#a89bff", "#00c882", "#00e8a0"]),
        connector=dict(line=dict(color="rgba(108,99,255,0.3)", width=1)),
    ))
    fig_funil.update_layout(
        title="Pipeline de ML: Do Dado à Previsão",
        height=300,
        margin=dict(l=10, r=10, t=50, b=10),
    )
    st.plotly_chart(fig_funil, use_container_width=True)

st.markdown("---")

# ── Dois tipos de modelo ──────────────────────────────────────────────────
st.markdown("### 🔀 Os Dois Tipos de Modelo Aplicados ao Projeto")

col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown("""
    <div style="
        background: rgba(108,99,255,0.08);
        border: 1px solid rgba(108,99,255,0.35);
        border-radius: 16px;
        padding: 1.5rem 1.8rem;
        height: 100%;
    ">
        <div style="font-size:2rem; margin-bottom:0.5rem;">🔮</div>
        <div style="font-family:'Poppins',sans-serif; font-weight:700; color:#a89bff; font-size:1.05rem; margin-bottom:0.5rem;">
            Modelo Preditivo (Regressão)
        </div>
        <div style="background:#6c63ff22; border:1px solid #6c63ff55; border-radius:20px; padding:0.15rem 0.8rem;
                    font-size:0.72rem; font-family:'DM Sans',sans-serif; font-weight:700; color:#a89bff;
                    display:inline-block; margin-bottom:1rem;">
            Pergunta: QUANTO? QUANDO?
        </div>
        <p style="font-family:'DM Sans',sans-serif; color:#bbb; font-size:0.88rem; line-height:1.8;">
            Responde com um <strong style="color:#d9d9d9;">número</strong>.
            No projeto: <em>"Este pedido vai levar <strong style="color:#ffd93d;">X dias</strong> para chegar."</em>
        </p>
        <p style="font-family:'DM Sans',sans-serif; color:#bbb; font-size:0.88rem; line-height:1.8;">
            Em vez de mostrar ao cliente uma estimativa genérica de "5 a 12 dias úteis",
            o modelo calcula um prazo individualizado com base nas características do pedido.
        </p>
        <div style="margin-top:1rem; font-family:'DM Sans',sans-serif; font-size:0.82rem; color:#888;">
            🤖 Algoritmo: <strong style="color:#a89bff;">Random Forest Regressor</strong><br>
            📐 Métrica: <strong style="color:#00c882;">MAE — erro médio em dias</strong>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style="
        background: rgba(255,107,107,0.06);
        border: 1px solid rgba(255,107,107,0.35);
        border-radius: 16px;
        padding: 1.5rem 1.8rem;
        height: 100%;
    ">
        <div style="font-size:2rem; margin-bottom:0.5rem;">🚦</div>
        <div style="font-family:'Poppins',sans-serif; font-weight:700; color:#ff9999; font-size:1.05rem; margin-bottom:0.5rem;">
            Modelo de Classificação
        </div>
        <div style="background:#ff6b6b22; border:1px solid #ff6b6b55; border-radius:20px; padding:0.15rem 0.8rem;
                    font-size:0.72rem; font-family:'DM Sans',sans-serif; font-weight:700; color:#ff9999;
                    display:inline-block; margin-bottom:1rem;">
            Pergunta: VAI ATRASAR? SIM ou NÃO?
        </div>
        <p style="font-family:'DM Sans',sans-serif; color:#bbb; font-size:0.88rem; line-height:1.8;">
            Responde com uma <strong style="color:#d9d9d9;">categoria</strong>.
            No projeto: <em>"Este pedido tem <strong style="color:#ffd93d;">X% de chance</strong> de atrasar."</em>
        </p>
        <p style="font-family:'DM Sans',sans-serif; color:#bbb; font-size:0.88rem; line-height:1.8;">
            Com isso, a Olist age de forma <strong>proativa</strong>: notifica o cliente antes que perceba,
            aciona o SAC ou oferece um cupom preventivo.
        </p>
        <div style="margin-top:1rem; font-family:'DM Sans',sans-serif; font-size:0.82rem; color:#888;">
            🤖 Algoritmo: <strong style="color:#ff9999;">Random Forest Classifier</strong><br>
            📐 Métrica: <strong style="color:#00c882;">F1-Score + AUC-ROC</strong>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ── Evidências da EDA ────────────────────────────────────────────────────
st.markdown("### 📊 O Que os Dados Já Provam")

m1, m2, m3, m4 = st.columns(4)
m1.metric("Nota com atraso", "2,47 ⭐", "-1,20 pts vs sem atraso")
m2.metric("Não recompram após atraso", "95,5%", "Perda permanente de LTV")
m3.metric("Avaliações ruins interestaduais", "70,1%", "Maior preditor de risco")
m4.metric("Top 20% vendedores", "82,3% receita", "Princípio de Pareto confirmado")

st.markdown("<br>", unsafe_allow_html=True)

# Gráfico de barras: nota por situação
fig_notas = go.Figure()
fig_notas.add_trace(go.Bar(
    x=["Entregue no Prazo", "Entregue com Atraso"],
    y=[3.67, 2.47],
    marker_color=["#00c882", "#ff6b6b"],
    text=["3,67 ⭐", "2,47 ⭐"],
    textposition="outside",
    textfont=dict(color="#d9d9d9", size=14, family="Poppins"),
    width=0.4,
))
fig_notas.update_layout(
    title="Impacto Direto do Atraso na Avaliação do Cliente",
    yaxis=dict(range=[0, 5], title="Review Score Médio", **PLOTLY_LAYOUT["yaxis"]),
    height=320,
    showlegend=False,
)
st.plotly_chart(fig_notas, use_container_width=True)

insight_box("""
    <p style="font-family:'DM Sans',sans-serif; color:#d9d9d9; font-size:0.9rem; margin:0;">
    A diferença de <strong>1,2 ponto</strong> na avaliação entre pedidos no prazo e atrasados é enorme numa escala de 1 a 5.
    Esse gap é exatamente o que os modelos de ML buscam minimizar — identificando o risco <em>antes</em> que o atraso aconteça.
    </p>
""")

st.markdown("---")

# ── Features dos modelos ─────────────────────────────────────────────────
st.markdown("### 🔧 Quais Informações os Modelos Usam para Prever?")

fig_feat = go.Figure()
features = ["Estado do cliente", "Estado do vendedor", "Rota interestadual",
            "Valor do frete", "Mês da compra", "Dia da semana", "Preço do produto"]
importancias = [0.28, 0.22, 0.18, 0.14, 0.08, 0.06, 0.04]
cores_feat = ["#6c63ff" if v >= 0.15 else "#3a3880" for v in importancias]

fig_feat.add_trace(go.Bar(
    y=features,
    x=importancias,
    orientation="h",
    marker_color=cores_feat,
    text=[f"{v*100:.0f}%" for v in importancias],
    textposition="outside",
    textfont=dict(color="#d9d9d9", size=11),
))
fig_feat.update_layout(
    title="Importância Relativa das Features (estimativa baseline)",
    xaxis=dict(title="Importância Relativa", **PLOTLY_LAYOUT["xaxis"]),
    height=330,
    showlegend=False,
    margin=dict(l=160, r=60, t=50, b=20),
)
st.plotly_chart(fig_feat, use_container_width=True)

proposta_box("""
    <p style="font-family:'DM Sans',sans-serif; color:#d9d9d9; font-size:0.9rem; margin:0;">
    <strong>Estado do cliente e rota interestadual</strong> dominam a previsão — confirmando o que a EDA já mostrou:
    o principal risco logístico no Brasil é a distância. Pedidos saindo de SP para o Norte/Nordeste têm
    probabilidade de atraso estruturalmente maior.
    </p>
""")

st.markdown("---")

# ── 4 Propostas de ML ────────────────────────────────────────────────────
st.markdown("### 🚀 Propostas de Modelos de ML para o Projeto")

ml_proposals = [
    {
        "icon": "🔮",
        "title": "Predição de Atraso de Entrega",
        "type": "Classificação Binária",
        "type_color": "#6c63ff",
        "target": "flag_atraso (0 = no prazo | 1 = atrasado)",
        "features": "customer_state, seller_state, rota_interestadual, freight_value, fim_de_semana, mes_compra",
        "models": "Random Forest Classifier, XGBoost, LightGBM",
        "metric": "F1-Score (foco em Recall — melhor avisar falso alarme do que perder atraso real)",
        "value": "Avisar proativamente clientes em risco antes que o problema ocorra — transformando atraso em transparência e protegendo o NPS.",
    },
    {
        "icon": "📅",
        "title": "Predição de Prazo de Entrega",
        "type": "Regressão",
        "type_color": "#a89bff",
        "target": "tempo_entrega_real (número de dias)",
        "features": "customer_state, seller_state, freight_value, product_weight_g, mes_compra, dia_semana_compra",
        "models": "Random Forest Regressor, XGBoost Regressor, Ridge Regression (baseline)",
        "metric": "MAE em dias — 'o modelo erra em média X dias no prazo de entrega'",
        "value": "Mostrar ao cliente, no momento da compra, uma estimativa de prazo precisa e individualizada — reduzindo reclamações por expectativa frustrada.",
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
        "value": "Simular o impacto de mudanças operacionais (ex: reduzir frete em 20%) na nota esperada — guiando decisões de investimento com base em dados.",
    },
    {
        "icon": "🗺️",
        "title": "Segmentação de Clientes por Comportamento",
        "type": "Clusterização (Não Supervisionado)",
        "type_color": "#ffd93d",
        "target": "Grupos de comportamento de compra (sem rótulo pré-definido)",
        "features": "frequencia, recencia, ticket_medio, categoria_preferida, sensibilidade_frete",
        "models": "K-Means (k=4–6), DBSCAN, Agrupamento Hierárquico",
        "metric": "Silhouette Score, Inertia, interpretabilidade dos clusters",
        "value": "Personalizar comunicação, ofertas e SLA logístico por perfil — do cliente VIP ao comprador único sensível a frete.",
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
                <div style="font-family:'Poppins',sans-serif; font-weight:700; font-size:1.05rem; color:#d9d9d9;">{p['title']}</div>
                <span style="background:{p['type_color']}22; border:1px solid {p['type_color']}88; color:{p['type_color']};
                             border-radius:20px; padding:0.12rem 0.7rem; font-size:0.72rem;
                             font-family:'DM Sans',sans-serif; font-weight:700;">
                    {p['type']}
                </span>
            </div>
        </div>
        <div style="display:grid; grid-template-columns: 1fr 1fr; gap:0.8rem;">
            <div style="font-family:'DM Sans',sans-serif; font-size:0.85rem; color:#bbb;">
                🎯 <strong style="color:#d9d9d9;">Target:</strong><br>
                <code style="color:#a89bff; font-size:0.8rem;">{p['target']}</code>
            </div>
            <div style="font-family:'DM Sans',sans-serif; font-size:0.85rem; color:#bbb;">
                📐 <strong style="color:#d9d9d9;">Métrica:</strong><br>
                <code style="color:#00c882; font-size:0.8rem;">{p['metric']}</code>
            </div>
            <div style="font-family:'DM Sans',sans-serif; font-size:0.85rem; color:#bbb; grid-column: span 2;">
                🔧 <strong style="color:#d9d9d9;">Features:</strong><br>
                <code style="color:#ffd93d; font-size:0.79rem;">{p['features']}</code>
            </div>
            <div style="font-family:'DM Sans',sans-serif; font-size:0.85rem; color:#bbb;">
                🤖 <strong style="color:#d9d9d9;">Algoritmos:</strong> {p['models']}
            </div>
            <div style="font-family:'DM Sans',sans-serif; font-size:0.85rem; color:#00c882;">
                💡 <strong>Valor para a Olist:</strong> {p['value']}
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ── Radar de prioridade ───────────────────────────────────────────────────
st.markdown("### 📊 Mapa de Prioridade dos Projetos de ML")

categories = ['Impacto no NPS', 'Complexidade\nde Implementação', 'Dados\nDisponíveis',
              'Velocidade p/ Produção', 'ROI Estimado']

fig_radar = go.Figure()
ml_colors = [
    ("#6c63ff", "rgba(108,99,255,0.15)"),
    ("#a89bff", "rgba(168,155,255,0.15)"),
    ("#00c882", "rgba(0,200,130,0.15)"),
    ("#ffd93d", "rgba(255,217,61,0.15)"),
]
projects = [
    ("Predição de Atraso",        [90, 55, 95, 85, 90]),
    ("Predição de Prazo",         [85, 55, 90, 85, 84]),
    ("NPS Predictor",             [80, 50, 88, 80, 78]),
    ("Segmentação de Clientes",   [72, 45, 80, 70, 74]),
]
for (name, vals), (line_color, fill_color) in zip(projects, ml_colors):
    fig_radar.add_trace(go.Scatterpolar(
        r=vals + [vals[0]],
        theta=categories + [categories[0]],
        fill="toself",
        fillcolor=fill_color,
        line=dict(color=line_color, width=2),
        name=name,
    ))

fig_radar.update_layout(
    **PLOTLY_LAYOUT,
    polar=dict(
        radialaxis=dict(visible=True, range=[0, 100], gridcolor='rgba(108,99,255,0.2)', color='#888'),
        angularaxis=dict(gridcolor='rgba(108,99,255,0.2)', color='#d9d9d9'),
        bgcolor='rgba(13,12,104,0.3)',
    ),
    title="Matriz de Avaliação dos Projetos de ML (escala 0–100)",
    height=500,
    legend=dict(**PLOTLY_LAYOUT["legend"]),
)
st.plotly_chart(fig_radar, use_container_width=True)

proposta_box("""
    <p style="font-family:'DM Sans',sans-serif; color:#d9d9d9; font-size:0.9rem; margin:0;">
    O ponto de partida recomendado é a <strong>Predição de Atraso</strong> — maior impacto no NPS,
    dados já disponíveis no projeto e pipeline relativamente simples.
    Em paralelo, a <strong>Predição de Prazo</strong> complementa diretamente,
    usando as mesmas features e gerando valor imediato na experiência do cliente.
    O notebook de pesquisa está em <code>notebooks/Luis/ml_modelo_preditivo_classificacao.ipynb</code>.
    </p>
""")