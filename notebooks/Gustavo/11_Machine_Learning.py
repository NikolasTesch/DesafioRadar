import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from style_utils import (inject_global_css, render_sidebar_logo, page_header,
                          problema_box, insight_box, proposta_box,
                          PLOTLY_LAYOUT, ACCENT_COLORS)

st.set_page_config(
    page_title="Olist - Machine Learning",
    page_icon=os.path.join(os.path.dirname(__file__), "..", "public", "Radar.svg"),
    layout="wide"
)
inject_global_css()
render_sidebar_logo()

page_header("🤖 Machine Learning", "Regressão Linear para Prazo de Entrega & Classificação de Categorias em Crescimento")

# ── Intro ────────────────────────────────────────────────────────────────────
st.markdown("""
<p style="font-family:'DM Sans',sans-serif;color:#aaa;font-size:1rem;max-width:860px;line-height:1.9;">
A análise exploratória revelou dois problemas que têm solução direta via Machine Learning.
Esta seção apresenta as propostas do time: <strong>o que são os modelos, como funcionam e qual o impacto
real na operação da Olist</strong> — em linguagem acessível, sem abrir mão da profundidade técnica.
</p>
""", unsafe_allow_html=True)

# ── Cards de contexto ────────────────────────────────────────────────────────
c1, c2, c3, c4 = st.columns(4)
c1.metric("Nota com atraso",       "2,47 ⭐", "−1,20 pts vs no prazo")
c2.metric("Não recompram após atraso", "95,5%", "Perda permanente de LTV")
c3.metric("Avaliações ruins interestaduais", "70,1%", "Maior preditor de risco")
c4.metric("Clientes que compram 1x só", "97%", "Cada experiência é definitiva")

st.markdown("---")

# ════════════════════════════════════════════════════════════════════════════
# SEÇÃO 1 — O QUE É ML
# ════════════════════════════════════════════════════════════════════════════
st.markdown("### 🧠 O Que é Machine Learning — e Por Que Aqui?")

col_txt, col_viz = st.columns([1, 1], gap="large")

with col_txt:
    st.markdown("""
    <div style="background:rgba(13,12,104,0.5);border:1px solid rgba(108,99,255,0.25);
                border-radius:16px;padding:1.5rem 1.8rem;">
        <p style="font-family:'DM Sans',sans-serif;color:#bbb;font-size:0.92rem;line-height:1.9;margin:0;">
            Machine Learning é ensinar o computador a <strong style="color:#a89bff;">aprender padrões
            com dados históricos</strong> para tomar decisões ou fazer previsões em casos novos —
            sem programar cada regra manualmente.
        </p>
        <p style="font-family:'DM Sans',sans-serif;color:#bbb;font-size:0.92rem;line-height:1.9;margin-top:1rem;">
            No contexto da Olist, temos <strong style="color:#d9d9d9;">100.000 pedidos reais</strong>
            com histórico completo de prazos, fretes, regiões e avaliações. Esse volume é exatamente
            o que um modelo de ML precisa para aprender — e o que um analista humano jamais conseguiria
            processar manualmente.
        </p>
        <div style="margin-top:1.2rem;padding:0.8rem 1rem;background:rgba(108,99,255,0.1);
                    border-left:3px solid #6c63ff;border-radius:0 8px 8px 0;">
            <p style="font-family:'DM Sans',sans-serif;color:#a89bff;font-size:0.88rem;margin:0;">
                <strong>Analogia:</strong> é como um funcionário experiente que já viu 100 mil pedidos
                e consegue dizer <em>"esse aqui tem tudo para atrasar"</em> — porque reconhece o padrão.
                O modelo faz o mesmo, em milissegundos.
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col_viz:
    # Pipeline visual
    fig_pipe = go.Figure(go.Funnel(
        y=["100k Pedidos Históricos", "Feature Engineering<br>(variáveis relevantes)",
           "Treinamento<br>(o modelo aprende)", "Validação<br>(testa com dados novos)",
           "Previsão em Tempo Real"],
        x=[100, 80, 60, 45, 30],
        textinfo="label",
        marker=dict(color=["#6c63ff","#7c74ff","#a89bff","#00c882","#00e8a0"]),
        connector=dict(line=dict(color="rgba(108,99,255,0.3)", width=1)),
    ))
    fig_pipe.update_layout(
        **PLOTLY_LAYOUT, title="Pipeline: Do Dado à Previsão", height=310,
        margin=dict(l=10, r=10, t=45, b=10))
    st.plotly_chart(fig_pipe, use_container_width=True)

st.markdown("---")

# ════════════════════════════════════════════════════════════════════════════
# SEÇÃO 2 — OS DOIS MODELOS LADO A LADO
# ════════════════════════════════════════════════════════════════════════════
st.markdown("### 🔀 As Duas Propostas do Time")

col_m1, col_m2 = st.columns(2, gap="large")

with col_m1:
    st.markdown("""
    <div style="background:rgba(108,99,255,0.08);border:1px solid rgba(108,99,255,0.4);
                border-radius:16px;padding:1.5rem 1.8rem;height:100%;">
        <div style="font-size:2.2rem;margin-bottom:0.4rem;">📈</div>
        <div style="font-family:'Poppins',sans-serif;font-weight:700;color:#a89bff;
                    font-size:1.05rem;margin-bottom:0.4rem;">
            Modelo 1 — Regressão Linear
        </div>
        <div style="background:#6c63ff22;border:1px solid #6c63ff66;border-radius:20px;
                    padding:0.15rem 0.8rem;font-size:0.72rem;font-family:'DM Sans',sans-serif;
                    font-weight:700;color:#a89bff;display:inline-block;margin-bottom:1rem;">
            Pergunta: QUANTOS DIAS vai levar?
        </div>

        <p style="font-family:'DM Sans',sans-serif;color:#bbb;font-size:0.9rem;line-height:1.8;">
            <strong style="color:#d9d9d9;">Problema:</strong> a Olist hoje promete uma janela genérica
            de entrega (ex: "7 a 15 dias"). Essa imprecisão é o principal gatilho de avaliações ruins —
            o cliente se frustra não pelo atraso em si, mas pela expectativa errada.
        </p>
        <p style="font-family:'DM Sans',sans-serif;color:#bbb;font-size:0.9rem;line-height:1.8;">
            <strong style="color:#d9d9d9;">Solução:</strong> com base em origem, destino, valor do frete
            (proxy de peso/volume) e época do ano, o modelo calcula um prazo
            <strong>individualizado e preciso</strong> para cada pedido.
        </p>

        <div style="margin-top:1rem;font-family:'DM Sans',sans-serif;font-size:0.82rem;color:#888;">
            <div>🎯 <strong style="color:#d9d9d9;">Target:</strong>
                <code style="color:#a89bff;">tempo_entrega_real</code> (número de dias)</div>
            <div style="margin-top:0.4rem;">🔧 <strong style="color:#d9d9d9;">Features principais:</strong><br>
                <code style="color:#ffd93d;font-size:0.78rem;">
                customer_state, seller_state, freight_value,<br>
                rota_interestadual, mes_compra, fim_de_semana
                </code>
            </div>
            <div style="margin-top:0.4rem;">📐 <strong style="color:#d9d9d9;">Métrica:</strong>
                <code style="color:#00c882;">MAE em dias — "erra em média X dias"</code></div>
        </div>

        <div style="margin-top:1rem;padding:0.7rem 1rem;background:rgba(108,99,255,0.1);
                    border-left:3px solid #6c63ff;border-radius:0 8px 8px 0;">
            <p style="font-family:'DM Sans',sans-serif;color:#a89bff;font-size:0.85rem;margin:0;">
                <strong>Por que Regressão Linear?</strong> Os coeficientes são diretamente
                interpretáveis como insight de negócio: <em>"rota interestadual adiciona X dias ao prazo"</em>.
                Simples, rápida e explicável para qualquer stakeholder.
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col_m2:
    st.markdown("""
    <div style="background:rgba(0,200,130,0.06);border:1px solid rgba(0,200,130,0.4);
                border-radius:16px;padding:1.5rem 1.8rem;height:100%;">
        <div style="font-size:2.2rem;margin-bottom:0.4rem;">🚀</div>
        <div style="font-family:'Poppins',sans-serif;font-weight:700;color:#00c882;
                    font-size:1.05rem;margin-bottom:0.4rem;">
            Modelo 2 — Classificação de Categorias
        </div>
        <div style="background:#00c88222;border:1px solid #00c88266;border-radius:20px;
                    padding:0.15rem 0.8rem;font-size:0.72rem;font-family:'DM Sans',sans-serif;
                    font-weight:700;color:#00c882;display:inline-block;margin-bottom:1rem;">
            Pergunta: essa categoria vai dar BOOM?
        </div>

        <p style="font-family:'DM Sans',sans-serif;color:#bbb;font-size:0.9rem;line-height:1.8;">
            <strong style="color:#d9d9d9;">Problema:</strong> a Olist não sabe com antecedência
            quais categorias vão explodir em demanda. Isso gera estoque insuficiente nas categorias
            em crescimento e oportunidades perdidas de marketing e logística antecipada.
        </p>
        <p style="font-family:'DM Sans',sans-serif;color:#bbb;font-size:0.9rem;line-height:1.8;">
            <strong style="color:#d9d9d9;">Solução:</strong> o modelo analisa o histórico de volume
            de cada categoria e <strong>classifica as que têm perfil de crescimento acelerado</strong>
            — permitindo ação antes que a demanda chegue.
        </p>

        <div style="margin-top:1rem;font-family:'DM Sans',sans-serif;font-size:0.82rem;color:#888;">
            <div>🎯 <strong style="color:#d9d9d9;">Target:</strong>
                <code style="color:#00c882;">boom = 1</code> (top 25% crescimento) ou
                <code style="color:#ff6b6b;">boom = 0</code> (estável/declínio)</div>
            <div style="margin-top:0.4rem;">🔧 <strong style="color:#d9d9d9;">Features principais:</strong><br>
                <code style="color:#ffd93d;font-size:0.78rem;">
                volume_total, crescimento_pct,<br>
                volume por ano (série histórica)
                </code>
            </div>
            <div style="margin-top:0.4rem;">📐 <strong style="color:#d9d9d9;">Métrica:</strong>
                <code style="color:#00c882;">F1-Score + AUC-ROC</code></div>
        </div>

        <div style="margin-top:1rem;padding:0.7rem 1rem;background:rgba(0,200,130,0.08);
                    border-left:3px solid #00c882;border-radius:0 8px 8px 0;">
            <p style="font-family:'DM Sans',sans-serif;color:#00c882;font-size:0.85rem;margin:0;">
                <strong>Por que Classificação e não Regressão?</strong> A decisão de negócio
                é binária: <em>investir ou não nessa categoria?</em> Um número de crescimento esperado
                é menos acionável do que uma sinalização clara de risco/oportunidade.
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ════════════════════════════════════════════════════════════════════════════
# SEÇÃO 3 — EVIDÊNCIAS QUE SUSTENTAM OS MODELOS
# ════════════════════════════════════════════════════════════════════════════
st.markdown("### 📊 Evidências da EDA que Sustentam os Modelos")

tab1, tab2 = st.tabs(["📈 Regressão — Prazo de Entrega", "🚀 Classificação — Categorias"])

with tab1:
    col_g1, col_g2 = st.columns(2, gap="large")

    with col_g1:
        # Prazo por região
        regioes = ["Norte", "Nordeste", "Centro-Oeste", "Sul", "Sudeste"]
        prazos  = [23, 20, 15, 11, 9]
        cores   = ["#ff6b6b","#ff9966","#ffd93d","#00c882","#00c882"]
        fig_reg = go.Figure(go.Bar(
            y=regioes, x=prazos, orientation='h',
            marker_color=cores, text=[f"{p} dias" for p in prazos],
            textposition="outside", textfont=dict(color="#d9d9d9", size=12)
        ))
        fig_reg.update_layout(
            **PLOTLY_LAYOUT, height=300, showlegend=False,
            title="Prazo Mediano por Região (confirmado na EDA)",
            xaxis=dict(title="Dias", **PLOTLY_LAYOUT["xaxis"]),
            margin=dict(l=110, r=60, t=45, b=20)
        )
        st.plotly_chart(fig_reg, use_container_width=True)

    with col_g2:
        # Nota vs prazo
        prazos_nps = list(range(1, 31, 2))
        notas_nps  = [4.4, 4.3, 4.1, 3.9, 3.7, 3.5, 3.3, 3.1, 2.9, 2.8,
                      2.7, 2.6, 2.5, 2.4, 2.4]
        fig_nps = go.Figure()
        fig_nps.add_trace(go.Scatter(
            x=prazos_nps, y=notas_nps, mode='lines+markers',
            line=dict(color="#6c63ff", width=3),
            marker=dict(size=7, color="#a89bff"),
            fill='tozeroy', fillcolor='rgba(108,99,255,0.1)',
            name="Review Score médio"
        ))
        fig_nps.add_hline(y=3.67, line_dash="dash", line_color="#00c882",
                          annotation_text="Média geral: 3.67", annotation_position="right")
        fig_nps.update_layout(
            **PLOTLY_LAYOUT, height=300,
            title="Quanto mais dias, menor a nota",
            xaxis=dict(title="Dias de entrega", **PLOTLY_LAYOUT["xaxis"]),
            yaxis=dict(title="Review Score", range=[1, 5], **PLOTLY_LAYOUT["yaxis"]),
            margin=dict(l=20, r=80, t=45, b=20)
        )
        st.plotly_chart(fig_nps, use_container_width=True)

    insight_box("""
        <p style="font-family:'DM Sans',sans-serif;color:#d9d9d9;font-size:0.9rem;margin:0;">
        O Norte demora <strong>2,5× mais</strong> que o Sudeste para receber um pedido.
        Cada dia a mais no prazo reduz a nota — e a regressão linear vai capturar exatamente
        essa relação, gerando um coeficiente interpretável: <em>"cada dia adicional equivale a X pontos
        a menos no review score esperado"</em>.
        </p>
    """)

with tab2:
    col_c1, col_c2 = st.columns(2, gap="large")

    with col_c1:
        # Categorias exemplo BOOM vs declínio
        categorias_ex = ["Beleza & Saúde", "Esporte & Lazer", "Eletrônicos",
                         "Cama/Mesa/Banho", "Brinquedos", "Móveis", "Telefonia", "Informática"]
        crescimento_ex = [85, 72, 61, 38, 25, -12, -28, -41]
        boom_ex        = [1,1,1,1,0,0,0,0]
        cores_cat      = ["#00c882" if b else "#ff6b6b" for b in boom_ex]

        fig_cat = go.Figure(go.Bar(
            y=categorias_ex, x=crescimento_ex, orientation='h',
            marker_color=cores_cat,
            text=[f"{v:+.0f}%" for v in crescimento_ex],
            textposition="outside", textfont=dict(color="#d9d9d9", size=11)
        ))
        fig_cat.add_vline(x=0, line_color="#888", line_width=1)
        fig_cat.update_layout(
            **PLOTLY_LAYOUT, height=320, showlegend=False,
            title="Categorias: BOOM (verde) vs Declínio (vermelho)",
            xaxis=dict(title="Crescimento de Volume (%)", **PLOTLY_LAYOUT["xaxis"]),
            margin=dict(l=140, r=70, t=45, b=20)
        )
        st.plotly_chart(fig_cat, use_container_width=True)

    with col_c2:
        # Matriz de decisão do classificador
        fig_mat = go.Figure(data=go.Heatmap(
            z=[[45, 8], [5, 42]],
            x=["Previsto: Estável", "Previsto: BOOM"],
            y=["Real: Estável", "Real: BOOM"],
            colorscale=[[0,"rgba(13,12,104,0.3)"],[1,"#6c63ff"]],
            showscale=False,
            text=[["Acerto ✅<br>45", "Falso Alarme ⚠️<br>8"],
                  ["Oportunidade\nPerdida ❌<br>5", "Acerto ✅<br>42"]],
            texttemplate="%{text}", textfont=dict(size=13, color="#d9d9d9")
        ))
        fig_mat.update_layout(
            **PLOTLY_LAYOUT, height=320,
            title="Matriz de Confusão — Exemplo Esperado",
            margin=dict(l=100, r=20, t=45, b=20)
        )
        st.plotly_chart(fig_mat, use_container_width=True)

    insight_box("""
        <p style="font-family:'DM Sans',sans-serif;color:#d9d9d9;font-size:0.9rem;margin:0;">
        O classificador aprende a distinguir quais padrões de crescimento histórico indicam uma categoria
        em aceleração. Na matriz de confusão, o erro mais caro é o <strong>"Oportunidade Perdida"</strong>
        (categoria que vai explodir mas o modelo classificou como estável) — por isso a métrica
        F1-Score prioriza Recall.
        </p>
    """)

st.markdown("---")

# ════════════════════════════════════════════════════════════════════════════
# SEÇÃO 4 — COMO OS MODELOS APRENDEM
# ════════════════════════════════════════════════════════════════════════════
st.markdown("### ⚙️ Como Cada Modelo Aprende — Passo a Passo")

col_p1, col_p2 = st.columns(2, gap="large")

passos_reg = [
    ("1", "Coleta", "Histórico de 100k pedidos com prazo real, frete, origem, destino e data"),
    ("2", "Features", "Extrai variáveis: estado cliente/vendedor, frete, mês, dia da semana, rota interestadual"),
    ("3", "Treino", "Ajusta os coeficientes: quanto cada variável impacta o prazo, em dias"),
    ("4", "Validação", "Testa com 20% dos dados que o modelo nunca viu — mede o erro em dias (MAE)"),
    ("5", "Produção", "Recebe características de um pedido novo → retorna prazo previsto em segundos"),
]
passos_clf = [
    ("1", "Coleta", "Histórico de vendas por categoria e período (2016-2018)"),
    ("2", "Features", "Calcula volume total, crescimento entre anos e série histórica de volumes"),
    ("3", "Label", "Categorias no top 25% de crescimento recebem label BOOM = 1"),
    ("4", "Treino", "Random Forest aprende os padrões que distinguem BOOM de estável"),
    ("5", "Produção", "Recebe uma categoria com histórico → retorna probabilidade de BOOM (0-100%)"),
]

for col, passos, cor, titulo in [
    (col_p1, passos_reg, "#6c63ff", "Regressão Linear — Prazo"),
    (col_p2, passos_clf, "#00c882", "Classificação — Categorias"),
]:
    with col:
        st.markdown(f"""
        <div style="font-family:'Poppins',sans-serif;font-weight:700;color:{cor};
                    font-size:0.95rem;margin-bottom:1rem;">{titulo}</div>
        """, unsafe_allow_html=True)
        for num, nome, desc in passos:
            st.markdown(f"""
            <div style="display:flex;gap:0.9rem;margin-bottom:0.7rem;align-items:flex-start;">
                <div style="background:{cor};color:#fff;border-radius:50%;width:26px;height:26px;
                            display:flex;align-items:center;justify-content:center;
                            font-family:'Poppins',sans-serif;font-weight:700;font-size:0.8rem;
                            flex-shrink:0;margin-top:2px;">{num}</div>
                <div>
                    <div style="font-family:'Poppins',sans-serif;font-weight:600;
                                color:#d9d9d9;font-size:0.88rem;">{nome}</div>
                    <div style="font-family:'DM Sans',sans-serif;color:#999;
                                font-size:0.83rem;line-height:1.6;">{desc}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

st.markdown("---")

# ════════════════════════════════════════════════════════════════════════════
# SEÇÃO 5 — IMPACTO ESPERADO
# ════════════════════════════════════════════════════════════════════════════
st.markdown("### 💰 Impacto Esperado na Operação")

fig_impact = go.Figure()

acoes    = ["Prazo preciso\nexibido na compra", "Alerta proativo\nde atraso", 
            "Estoque antecipado\ncategorias BOOM", "Marketing direcionado\npor categoria"]
impactos = [88, 82, 74, 68]
cores_i  = ["#6c63ff","#a89bff","#00c882","#4ecdc4"]

fig_impact.add_trace(go.Bar(
    x=acoes, y=impactos, marker_color=cores_i,
    text=[f"{v}/100" for v in impactos],
    textposition="outside", textfont=dict(color="#d9d9d9", size=12)
))
fig_impact.update_layout(
    **PLOTLY_LAYOUT, height=340, showlegend=False,
    title="Score de Impacto Estimado por Ação (escala 0–100)",
    yaxis=dict(range=[0, 110], title="Score de Impacto", **PLOTLY_LAYOUT["yaxis"]),
    margin=dict(l=20, r=20, t=45, b=60)
)
st.plotly_chart(fig_impact, use_container_width=True)

proposta_box("""
    <p style="font-family:'DM Sans',sans-serif;color:#d9d9d9;font-size:0.9rem;margin:0;">
    O ponto de partida recomendado é a <strong>Regressão Linear de Prazo</strong> — maior impacto
    direto no NPS, dados já disponíveis no projeto e resultado interpretável para qualquer área.
    Em paralelo, a <strong>Classificação de Categorias</strong> endereça o crescimento estratégico.
    O notebook de pesquisa com o código completo está em
    <code>notebooks/Gustavo/ml_modelo_preditivo_classificacao.ipynb</code>.
    </p>
""")

st.markdown("---")

# ════════════════════════════════════════════════════════════════════════════
# SEÇÃO 6 — GLOSSÁRIO
# ════════════════════════════════════════════════════════════════════════════
with st.expander("📖 Glossário — Termos Técnicos em Linguagem Simples"):
    termos = [
        ("Regressão Linear",     "Modelo que encontra a melhor equação matemática para prever um número (ex: dias de entrega) com base em variáveis de entrada"),
        ("Classificação",        "Modelo que aprende a separar exemplos em categorias (ex: BOOM vs Estável) com base em padrões históricos"),
        ("Feature / Variável",   "Uma informação que o modelo usa como pista (ex: CEP, frete, dia da semana)"),
        ("Coeficiente",          "Número que diz o quanto uma variável impacta o resultado — ex: rota interestadual = +4 dias"),
        ("MAE",                  "Mean Absolute Error — erro médio em dias. Se MAE = 3, o modelo erra em média 3 dias"),
        ("F1-Score",             "Métrica que equilibra acertos e erros de classificação. Quanto mais perto de 1, melhor"),
        ("AUC-ROC",              "Mede o quanto o modelo consegue separar as classes. 0.5 = aleatório, 1.0 = perfeito"),
        ("Random Forest",        "Ensemble de muitas árvores de decisão — robusto, preciso e interpretável"),
        ("Overfitting",          "O modelo 'decorou' os dados de treino mas erra em dados novos — sinal de que é complexo demais"),
        ("Cross-Validation",     "Técnica de testar o modelo em várias divisões dos dados para garantir que o resultado é consistente"),
        ("LTV / CLV",            "Lifetime Value — o valor total que um cliente gera ao longo da relação com a empresa"),
    ]
    col_g1, col_g2 = st.columns(2)
    for i, (termo, def_) in enumerate(termos):
        col = col_g1 if i % 2 == 0 else col_g2
        with col:
            st.markdown(f"""
            <div style="margin-bottom:0.6rem;padding:0.6rem 0.9rem;
                        background:rgba(13,12,104,0.4);border-radius:8px;
                        border-left:3px solid #6c63ff;">
                <div style="font-family:'Poppins',sans-serif;font-weight:600;
                            color:#a89bff;font-size:0.85rem;">{termo}</div>
                <div style="font-family:'DM Sans',sans-serif;color:#bbb;
                            font-size:0.82rem;line-height:1.6;margin-top:0.2rem;">{def_}</div>
            </div>
            """, unsafe_allow_html=True)
