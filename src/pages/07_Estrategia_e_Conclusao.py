import streamlit as st

st.set_page_config(page_title="Conclusão - Olist", page_icon="💡", layout="wide")

st.title("💡 Estratégia e Recomendações")

st.markdown("""
### 🚀 Insights Acionáveis e Conclusões

Após uma análise técnica rigorosa (com tratamento de outliers via IQR e cruzamento de bases), consolidamos as seguintes recomendações:

#### 1. Estratégia de Pagamento e Ticket Médio
* **Descoberta**: O ticket médio aumenta linearmente com o número de parcelas. Compras em 10x têm ticket ~3x maior que compras à vista.
* **Ação**: Incentivar campanhas de 'Parcelamento Sem Juros' para categorias de alto valor (Relógios, Eletrônicos) para elevar o GMV total.

#### 2. Logística como Detrator de Marca
* **Descoberta**: A nota média (NPS) cai de **4.2 para 2.1** em pedidos com atraso. O custo do frete no Norte/Nordeste é o maior limitador de volume.
* **Ação**: Priorizar a descentralização logística (Hubs Regionais) para reduzir o frete e o prazo nessas regiões críticas.

#### 3. Otimização de Marketing (Prime-Time)
* **Descoberta**: As vendas concentram-se fortemente em dias úteis, entre 10h e 16h.
* **Ação**: Alocar orçamentos de Ads e disparos de Push Notifications especificamente neste horário para maximizar a conversão.

#### 4. Rigor nos Dados (IQR)
* **Descoberta**: Dados brutos continham outliers que distorciam a receita em até 15%.
* **Ação**: Todas as métricas de performance devem utilizar a base **Saneada** para evitar falsas percepções de crescimento baseadas em casos isolados de alto valor.

---
""")

st.info("💡 **Ação Prática:** O cruzamento de dados mostra que o atraso não é apenas um problema operacional, mas um drenador de receita futura. Clientes que avaliam com nota 1 ou 2 dificilmente retornam à plataforma.")

st.divider()

# --- Simulador de Impacto (Premium Feature) ---
st.subheader("🧮 Simulador de Impacto de Eficiência Logística")
st.markdown("Quanto o negócio ganharia se reduzissemos a taxa de atraso atual?")

from utils import get_analytical_df
df_sim = get_analytical_df()

# Métricas base
delay_rate_actual = df_sim['flag_atraso'].mean()
total_revenue_actual = df_sim['receita_liquida'].sum()

col_sim1, col_sim2 = st.columns([1, 2])

with col_sim1:
    st.write("**Parâmetros de Simulação**")
    meta_atraso = st.slider("Nova Meta de Taxa de Atraso (%)",
                           min_value=0.0, max_value=float(delay_rate_actual*100),
                           value=float(delay_rate_actual*50)) / 100

    churn_presumido = st.slider("Presunção de Churn por Atraso (%)",
                               min_value=5, max_value=80, value=30) / 100

with col_sim2:
    # Cálculo simplificado de ganho
    # Pedidos recuperados = (Taxa Atual - Nova Meta) * Total Pedidos
    # Receita Recuperada = Pedidos Recuperados * Ticket Médio * (1 - Churn Presumido)
    num_pedidos = df_sim['order_id'].nunique()
    ticket_medio = total_revenue_actual / num_pedidos

    pedidos_afetados_hoje = num_pedidos * delay_rate_actual
    pedidos_afetados_meta = num_pedidos * meta_atraso
    pedidos_salvos = pedidos_afetados_hoje - pedidos_afetados_meta

    receita_potencial_recuperada = pedidos_salvos * ticket_medio * churn_presumido

    st.metric("Receita Adicional Estimada (LTV)", f"R$ {receita_potencial_recuperada:,.2f}",
              delta=f"{(receita_potencial_recuperada/total_revenue_actual)*100:.2f}% do Faturamento Total",
              help="Cálculo baseado na recuperação de clientes que deixariam de comprar devido à frustração com o atraso.")

    st.caption(f"Taxa de atraso atual: {delay_rate_actual*100:.2f}%")

st.divider()

st.subheader("👥 Equipe Desafio Radar")
st.markdown("""
* **Davi**: Análise Estratégica e Sazonalidade
* **Edvan**: Regionalidade e Qualidade de Dados
* **Nikolas**: Performance Logística
* **Samuel**: Financeiro e Pagamentos
* **Gustavo**: Satisfação do Cliente
* **Romulo/Fabily**: Insights de Mercado
""")

st.divider()
st.markdown("*Agradecemos a visualização desta análise técnica! Esta ferramenta foi desenvolvida para transformar dados puros em decisões de alto impacto.*")

st.balloons()
