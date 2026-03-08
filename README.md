# 📊 Desafio Radar: Dashboard Estratégico Olist

Este projeto é uma aplicação **Streamlit** desenvolvida para fornecer uma visualização 360º e análise profunda dos dados do ecossistema de e-commerce da **Olist**. O objetivo é transformar dados brutos em insights estratégicos sobre os principais pilares da operação.

---

## 📋 Visão Geral
O Dashboard consolida análises fundamentais para a gestão do e-commerce:
*   **Logística**: Identificação de gargalos e impacto do tempo de entrega no NPS.
*   **Financeiro**: Visualização de GMV, impacto do frete e ticket médio por região.
*   **Regionalidade**: Mapeamento de fricções e performance por estado.
*   **Sazonalidade**: Comportamento da operação em eventos críticos como a Black Friday.

---

## 🚀 Como Executar

Este projeto foi desenvolvido utilizando **Python 3.13**. Siga os passos abaixo para preparar o ambiente em qualquer dispositivo.

### 1. Clonar o Repositório
```bash
git clone https://github.com/NikolasTesch/DesafioRadar.git
cd DesafioRadar
```

### 2. Instalação de Dependências

#### Opção A: Usando Poetry (Recomendado)
Se você tem o [Poetry](https://python-poetry.org/) instalado:
```bash
poetry install
```

#### Opção B: Usando Pip (Ambiente Virtual)
Se preferir o modo tradicional:
```bash
# Criar ambiente virtual
python -m venv .venv

# Ativar o ambiente (Windows)
.venv\Scripts\activate

# Ativar o ambiente (Linux/Mac)
source .venv/bin/activate

# Instalar dependências
pip install streamlit pandas numpy matplotlib seaborn plotly scikit-learn statsmodels unidecode setuptools
```

### 3. Executar o Dashboard
Com as dependências instaladas, execute:
```bash
streamlit run src/app.py
```

---

## 📁 Estrutura do Projeto
*   `data/`: Contém os datasets brutos (`raw/`) e processados.
*   `src/app.py`: Ponto de entrada da aplicação Streamlit.
*   `src/pages/`: Páginas detalhadas de análise (Logística, Regionalidade, etc).
*   `src/utils.py`: Funções de processamento, ETL e cache de dados.
*   `notebooks/`: Documentação da análise exploratória e experimentos de ML.

---

## 🛠️ Tecnologias Utilizadas
*   **Framework**: [Streamlit](https://streamlit.io/)
*   **Análise de Dados**: [Pandas](https://pandas.pydata.org/), [NumPy](https://numpy.org/)
*   **Visualização**: [Plotly](https://plotly.com/), [Matplotlib](https://matplotlib.org/), [Seaborn](https://seaborn.pydata.org/)
*   **Modelagem**: [Scikit-Learn](https://scikit-learn.org/), [Statsmodels](https://www.statsmodels.org/)
*   **Gestão de Pacotes**: [Poetry](https://python-poetry.org/)

---

## 📊 Detalhes Técnicos (Como funciona?)

### Carregamento Otimizado
Utilizamos o decorator `@st.cache_data` para garantir que o processamento pesado de junção das 7 tabelas (~100k registros) ocorra apenas uma vez, garantindo uma navegação fluida.

### Interface Wide
A configuração `layout="wide"` no Streamlit é utilizada para maximizar a área de visualização dos gráficos complexos e indicadores (KPIs).
