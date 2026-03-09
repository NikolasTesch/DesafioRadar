import streamlit as st
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from style_utils import inject_global_css, render_sidebar_logo, page_header, proposta_box
from utils import get_analytical_df

st.set_page_config(page_title="Olist - O peso do Atraso", page_icon=os.path.join(os.path.dirname(__file__), "..", "public", "Radar.svg"), layout="wide")
inject_global_css()
render_sidebar_logo()

page_header("🏆 Propostas de Valor Globais", "Síntese das soluções baseadas em evidências")

st.markdown("""
<p style="font-family:'DM Sans',sans-serif; color:#aaa; font-size:1rem; max-width:800px; line-height:1.8;">
Após uma análise técnica rigorosa — com tratamento de outliers via IQR, cruzamento de 7 datasets e
geração de métricas derivadas — consolidamos abaixo as <strong>4 propostas de valor prioritárias</strong>,
ordenadas pelo potencial de impacto no negócio.
</p>
""", unsafe_allow_html=True)

st.markdown("---")

proposals = [
    {
        "icon": "🏭",
        "title": "Descentralização Logística Regional",
        "priority": "Alta",
        "priority_color": "#ff5050",
        "finding": "Estados do Norte e Nordeste pagam até 4x mais de frete e esperam o dobro do prazo médio. A taxa de atraso nessas regiões é crítica.",
        "action": "Implantar Hubs de Distribuição em Recife (PE) e Manaus (AM), reduzindo raio de entrega e custo de last-mile em até 40% para essas regiões.",
        "impact": "Aumento de volume nas regiões sub-atendidas + redução de atraso + melhoria do NPS regional.",
    },
    {
        "icon": "💳",
        "title": "Incentivo Estratégico ao Parcelamento",
        "priority": "Alta",
        "priority_color": "#ff5050",
        "finding": "Compras parceladas em 10x têm ticket médio ~3x maior que compras à vista. O volume em 1x ainda domina.",
        "action": "Oferecer 'Parcelamento Sem Juros' subsidiado para categorias de alto valor (Eletrônicos, Relógios, Esportes). Parceria com adquirentes para redução da taxa.",
        "impact": "Elevação do GMV sem aquisição de novos clientes — aumento de 15–25% no ticket médio estimado.",
    },
    {
        "icon": "⏰",
        "title": "Otimização de Marketing por Prime-Time",
        "priority": "Média",
        "priority_color": "#ffd93d",
        "finding": "O volume de pedidos concentra-se entre 10h–16h em dias úteis. Campanhas fora desse horário têm ROAS inferior.",
        "action": "Alocar 70%+ do orçamento de Ads e disparos de Push Notifications no intervalo 9h–16h, de segunda a quinta. Automatizar com regras de dayparting.",
        "impact": "Redução de CPA e aumento de ROAS sem aumento de budget — potencial de +20% na conversão por clique.",
    },
    {
        "icon": "📋",
        "title": "Padronização de Métricas (Base Saneada)",
        "priority": "Média",
        "priority_color": "#ffd93d",
        "finding": "Dados brutos contêm outliers que distorcem revenue e ticket médio em até 15%, levando a decisões estratégicas baseadas em dados incorretos.",
        "action": "Adotar a metodologia IQR como padrão para todos os relatórios executivos e dashboards de BI. Criar data contract para métricas financeiras.",
        "impact": "Decisões de investimento e pricing mais precisas, evitando sub ou super-estimação do desempenho real.",
    },
]

for i, p in enumerate(proposals):
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
    ">
        <div style="font-size: 2.5rem; flex-shrink:0;">{p['icon']}</div>
        <div style="flex: 1;">
            <div style="display:flex; align-items:center; gap:0.8rem; margin-bottom:0.5rem;">
                <span style="font-family:'Poppins',sans-serif; font-weight:700; font-size:1.1rem; color:#d9d9d9;">{p['title']}</span>
                <span style="background:{p['priority_color']}22; border:1px solid {p['priority_color']}88; color:{p['priority_color']}; border-radius:20px; padding:0.15rem 0.7rem; font-size:0.72rem; font-family:'DM Sans',sans-serif; font-weight:700; letter-spacing:0.08em;">
                    {p['priority']} Prioridade
                </span>
            </div>
            <div style="font-family:'DM Sans',sans-serif; color:#aaa; font-size:0.88rem; margin-bottom:0.6rem;">
                🔍 <strong>Evidência:</strong> {p['finding']}
            </div>
            <div style="font-family:'DM Sans',sans-serif; color:#d9d9d9; font-size:0.9rem; margin-bottom:0.5rem;">
                🎯 <strong>Ação:</strong> {p['action']}
            </div>
            <div style="font-family:'DM Sans',sans-serif; color:#00c882; font-size:0.88rem;">
                📈 <strong>Impacto Esperado:</strong> {p['impact']}
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")
st.markdown("### 🧮 Simulador de Impacto de Eficiência Logística")
st.markdown("Quanto o negócio recuperaria reduzindo a taxa de atraso atual?")

df_sim = get_analytical_df()
if not df_sim.empty:
    delay_rate_actual = df_sim['flag_atraso'].mean()
    total_revenue_actual = df_sim['receita_liquida'].sum()
    num_pedidos = df_sim['order_id'].nunique()
    ticket_medio = total_revenue_actual / num_pedidos

    col_sim1, col_sim2 = st.columns([1, 2])
    with col_sim1:
        meta_atraso = st.slider(
            "Nova Meta de Taxa de Atraso (%)",
            min_value=0.0, max_value=float(delay_rate_actual * 100),
            value=float(delay_rate_actual * 50)
        ) / 100
        churn_presumido = st.slider("Churn Estimado por Atraso (%)", min_value=5, max_value=80, value=30) / 100

    with col_sim2:
        pedidos_afetados_hoje = num_pedidos * delay_rate_actual
        pedidos_afetados_meta = num_pedidos * meta_atraso
        pedidos_salvos = pedidos_afetados_hoje - pedidos_afetados_meta
        receita_recuperada = pedidos_salvos * ticket_medio * churn_presumido

        st.metric(
            "💰 Receita Adicional Estimada (LTV)",
            f"R$ {receita_recuperada:,.2f}",
            delta=f"+{(receita_recuperada/total_revenue_actual)*100:.2f}% do GMV Total",
            help="Estimativa de receita recuperada por clientes que voltariam a comprar após melhorias logísticas."
        )
        st.caption(f"Taxa de atraso atual: {delay_rate_actual*100:.2f}% | Pedidos salvos: {pedidos_salvos:,.0f}")

    st.markdown("---")
    st.markdown("### ⚖️ Concentração de Mercado: Princípio de Pareto")
    
    col_par1, col_par2 = st.columns([1, 2])
    
    df_seller = get_analytical_df()
    if not df_seller.empty:
        receita_vendedores = df_seller.groupby('seller_id')['receita_liquida'].sum().sort_values(ascending=False)
        top_20_count = max(1, int(len(receita_vendedores) * 0.2))
        receita_top_20 = receita_vendedores.head(top_20_count).sum()
        receita_total = receita_vendedores.sum()
        percent_receita = (receita_top_20 / receita_total) * 100
        
        with col_par1:
            st.metric("Dominância Top 20%", f"{percent_receita:.1f}%", help="Percentual da receita total gerada pelos 20% maiores vendedores.")
            st.caption(f"Dos {len(receita_vendedores)} vendedores, apenas {top_20_count} sustentam o marketplace.")
            
        with col_par2:
            st.markdown(f"""
            <div style="background: rgba(0,200,130,0.1); border: 1px solid rgba(0,200,130,0.3); border-radius: 12px; padding: 1rem;">
                <strong>Insight de Risco:</strong> A operação é altamente dependente de uma elite de vendedores. 
                Uma falha sistêmica ou saída desses parceiros impactaria <strong>{percent_receita:.1f}%</strong> do faturamento imediato.
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 🏆 Performance dos Top 50 Vendedores")
    st.markdown("Volume de vendas vs. Satisfação do Cliente (Nota Média)")
    
    if not df_seller.empty:
        seller_stats = df_seller.groupby('seller_id').agg(
            volume=('order_id', 'nunique'),
            score=('review_score', 'mean'),
            receita=('receita_liquida', 'sum')
        ).reset_index()
        
        top_50 = seller_stats.sort_values('volume', ascending=False).head(50)
        
        from style_utils import PLOTLY_LAYOUT
        import plotly.express as px
        fig_sell = px.scatter(
            top_50, x="volume", y="score", size="receita",
            hover_name="seller_id",
            labels={'volume': 'Volume de Vendas', 'score': 'Nota Média'},
            color_discrete_sequence=['#a89bff']
        )
        fig_sell.update_layout(**PLOTLY_LAYOUT)
        fig_sell.add_hline(y=4.0, line_dash="dash", line_color="#ff5050", annotation_text="Meta de Qualidade")
        st.plotly_chart(fig_sell, use_container_width=True)

st.markdown("---")
st.markdown("### 👥 Equipe do Projeto")
members = [
    ("Davi", "Análise Estratégica e Sazonalidade", "📅"),
    ("Edvan", "Regionalidade e Qualidade de Dados", "🌎"),
    ("Nikolas", "Performance Logística", "🚚"),
    ("Samuel", "Financeiro e Pagamentos", "💰"),
    ("Gustavo", "Satisfação do Cliente", "⭐"),
    ("Romulo / Fabily", "Insights de Mercado", "💡"),
]
cols = st.columns(3)
for i, (name, role, icon) in enumerate(members):
    with cols[i % 3]:
        st.markdown(f"""
        <div style="background:rgba(108,99,255,0.08); border:1px solid rgba(108,99,255,0.2); border-radius:10px; padding:0.8rem; margin-bottom:0.7rem; text-align:center;">
            <div style="font-size:1.5rem;">{icon}</div>
            <div style="font-family:'Poppins',sans-serif; font-weight:700; color:#d9d9d9; font-size:0.9rem;">{name}</div>
            <div style="font-family:'DM Sans',sans-serif; color:#888; font-size:0.8rem; margin-top:0.2rem;">{role}</div>
        </div>
        """, unsafe_allow_html=True)
