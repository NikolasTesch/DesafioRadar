import streamlit as st
import plotly.graph_objects as go
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from style_utils import inject_global_css, render_sidebar_logo, page_header, PLOTLY_LAYOUT
from utils import get_analytical_df

st.set_page_config(page_title="Olist - Propostas Globais", page_icon=os.path.join(os.path.dirname(__file__), "..", "public", "Radar.svg"), layout="wide")
inject_global_css()
render_sidebar_logo()

page_header("🏆 Propostas de Valor Globais", "Impacto estimado e plano de ação resumido")

# ── FUNÇÃO PARA PEQUENOS GRÁFICOS (SPARKLINES) ──────────────────────────────
def create_sparkline(values, color="#00c882"):
    fig = go.Figure(go.Scatter(
        y=values,
        mode='lines',
        fill='tozeroy',
        line=dict(color=color, width=3),
        fillcolor=f"rgba{tuple(list(int(color.lstrip('#')[i:i+2], 16) for i in (0, 2, 4)) + [0.2])}"
    ))
    layout = PLOTLY_LAYOUT.copy()
    layout.update(dict(
        height=70,
        width=180,
        margin=dict(l=0, r=0, t=0, b=0),
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        showlegend=False
    ))
    fig.update_layout(layout)
    return fig

proposals = [
    {
        "icon": "🏭",
        "title": "Descentralização Logística",
        "priority": "Alta",
        "priority_color": "#ff5050",
        "evidencia": "Clientes no Norte/Nordeste pagam fretes até 400% superiores e enfrentam prazos 2x maiores que o Sudeste, gerando abandono de carrinho e baixo NPS regional.",
        "acao": "Implementação estratégica de Centros de Distribuição (Fulfillment) em Recife (PE) e Manaus (AM) para estoque de produtos 'A-Class' (alto giro).",
        "impacto": "Redução drástica de até 40% no Lead Time de entrega e nos custos de frete last-mile, aumentando a competitividade nessas regiões.",
        "chart_label": "REDUÇÃO DE PRAZO (DIAS)",
        "chart_desc": "Estimativa de queda após novos Hubs",
        "chart_data": [10, 8, 9, 6, 5, 4]
    },
    {
        "icon": "💳",
        "title": "Parcelamento Estratégico",
        "priority": "Alta",
        "priority_color": "#ff5050",
        "evidencia": "Embora o pagamento em 1x represente o maior volume, compras parceladas em 10x apresentam um Ticket Médio 3x superior (R$ 450 vs R$ 150).",
        "acao": "Subsídio planejado de taxas de juros para parcelamentos longos em categorias de alto valor agregado, como Eletrônicos e Relógios.",
        "impacto": "Elevação estimada de 20-25% no Ticket Médio Global através do incentivo ao consumo de produtos Premium via crédito facilitado.",
        "chart_label": "CRESCIMENTO TICKET MÉDIO",
        "chart_desc": "Projeção de ticket por faixa parcelada",
        "chart_data": [100, 110, 105, 120, 135, 150]
    },
    {
        "icon": "⏰",
        "title": "Marketing em Prime-Time",
        "priority": "Média",
        "priority_color": "#ffd93d",
        "evidencia": "Dados de tráfego confirmam pico de conversão e volume de pedidos em dias úteis entre 10h e 16h, com queda acentuada de eficiência no período noturno.",
        "acao": "Automação de Dayparting: alocar 75% do budget de publicidade (Ads/Push) nas janelas de alta conversão, reduzindo desperdício fora do horário comercial.",
        "impacto": "Otimização do ROAS (Retorno sobre Investimento em Ads) em até 25%, reduzindo o custo de aquisição de cliente (CAC) sem aumentar o budget total.",
        "chart_label": "EFICIÊNCIA DE CONVERSÃO",
        "chart_desc": "Ganho de ROAS em janelas otimizadas",
        "chart_data": [2.1, 2.3, 2.2, 2.8, 3.2, 3.5]
    },
]

for i, p in enumerate(proposals):
    container = st.container()
    with container:
        st.markdown(f"""
        <style>
        .card-{p['title'].replace(' ', '')} {{
            background: rgba(13,12,104,0.45);
            border: 1px solid rgba(108,99,255,0.25);
            border-radius: 16px;
            padding: 1.2rem 1.8rem;
            margin-bottom: 0.8rem;
        }}
        </style>
        """, unsafe_allow_html=True)
        
        col_txt, col_graph = st.columns([3.5, 1], vertical_alignment="center")
        
        with col_txt:
            st.markdown(f"""
            <div style="flex: 1;">
                <div style="display:flex; align-items:center; gap:0.6rem; margin-bottom:0.4rem;">
                    <span style="font-family:'Poppins',sans-serif; font-weight:700; font-size:1.15rem; color:#d9d9d9;">{p['title']}</span>
                <span style="background:{p['priority_color']}22; color:{p['priority_color']}; border:1px solid {p['priority_color']}88; border-radius:12px; padding:0rem 0.6rem; font-size:0.68rem; font-weight:700;">{p['priority']}</span>
            </div>
            <div style="font-family:'DM Sans',sans-serif; font-size:0.9rem; color:#aaa; line-height:1.6; margin-bottom:0.6rem;">
                🔍 <strong>Fato de Negócio:</strong> {p['evidencia']}<br>
                🎯 <strong>Ação Recomendada:</strong> {p['acao']}
            </div>
            <div style="font-family:'DM Sans',sans-serif; font-size:1rem; color:#00c882; font-weight:600;">
                🚀 Impacto Estimado: {p['impacto']}
            </div>
            """, unsafe_allow_html=True)
            
        with col_graph:
            st.plotly_chart(create_sparkline(p['chart_data']), config={'displayModeBar': False}, use_container_width=True)
            st.markdown(f"""
                <div style='text-align:center; margin-top:-15px;'>
                    <div style='font-size:0.65rem; color:#777; font-family:"Poppins",sans-serif; font-weight:600; letter-spacing:0.05em; text-transform:uppercase;'>{p['chart_label']}</div>
                    <div style='font-size:0.6rem; color:#555; font-family:"DM Sans",sans-serif; font-style:italic;'>{p['chart_desc']}</div>
                </div>
            """, unsafe_allow_html=True)
    
    if i < len(proposals) - 1:
        st.markdown("<div style='margin-bottom: 1.5rem; border-bottom: 1px solid rgba(108,99,255,0.15);'></div>", unsafe_allow_html=True)
