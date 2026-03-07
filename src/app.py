import streamlit as st
from utils import get_analytical_df

# Configuração da página
st.set_page_config(
    page_title="Análise Estratégica Olist",
    page_icon="📊",
    layout="wide"
)

def main():
    st.title("📊 Análise Estratégica de E-commerce: Olist")
    
    st.markdown("""
    ## 1. Visão Geral do Projeto
    
    Este projeto consolida a análise exploratória e estratégica do ecossistema de e-commerce da Olist. 
    Nosso objetivo é identificar os **gargalos logísticos**, entender o impacto da **regionalidade** no frete 
    e mapear os principais drivers de **satisfação do cliente**.
    
    ### 🎯 Objetivos Principais:
    1. **Logística**: Como o tempo de entrega afeta o NPS?
    2. **Financeiro**: Qual o impacto do frete na conversão e ticket médio?
    3. **Regional**: Quais estados apresentam maior fricção?
    4. **Sazonalidade**: Como eventos (Black Friday) estressam a operação?
    """)

    st.sidebar.success("Selecione uma análise acima.")

    st.info("💡 Navegue pelas páginas no menu lateral para ver os detalhes técnicos e insights.")

    # Carregamento inicial para cache
    with st.spinner("Carregando base analítica consolidada..."):
        df = get_analytical_df()
        if not df.empty:
            st.success(f"Base carregada com sucesso! {len(df):,} registros processados.")
            
            # KPIs Rápidos na Home
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Receita Total (GMV)", f"R$ {df['payment_value'].sum()/1e6:.2f}M")
            with col2:
                st.metric("Frete Médio", f"R$ {df['freight_value'].mean():.2f}")
            with col3:
                st.metric("Taxa de Atraso", f"{(df['flag_atraso'].mean()*100):.1f}%")

if __name__ == "__main__":
    main()
