# 🏗️ Arquitetura do Sistema: B-Comm Analytics

Este documento define a organização técnica do projeto, focada na transformação do dataset relacional da Olist em um dashboard estratégico.

## 📂 Estrutura de Pastas

```text
projeto_database/
├── .agent/            # Inteligência e Automações (Agentes/Skills/Workflows)
├── data/              # Camada de Dados
│   ├── raw/           # Arquivos originais da Olist (Imutáveis)
│   ├── interim/       # Tabelas intermediárias (pós-join)
│   └── processed/     # Dataset final unificado (Master Table)
├── documentation/     # PRD, Padrões e Referências
├── notebooks/         # Laboratório de EDA e Experimentos de ML
└── src/               # Código Produtivo
    ├── etl/           # Scripts de Limpeza, Join e Feature Engineering
    └── app/           # Dashboard Streamlit e Visualizações
```

---

## ⚡ Fluxo de Dados (Pipeline)

A arquitetura segue o fluxo **Bronze → Silver → Gold**:

1.  **Raw (Bronze):** Os múltiplos CSVs originais (pedidos, clientes, etc) residem aqui. São tratados como leitura protegida.
2.  **Interim (Silver):** Scripts em `src/etl/` realizam as junções (joins) e a engenharia de recursos (ex: cálculo de tempo de entrega).
3.  **Processed (Gold):** Uma tabela final, limpa e desnormalizada, é gerada para garantir a performance do Dashboard.

---

## 🛠️ Tecnologias e Camadas

### 1. `src/` (Produção)
*   **ETL:** Lógica pura em Python para o processamento de dados.
*   **App:** Componentes visuais e filtros do Streamlit.

### 2. `notebooks/` (Experimentação)
*   Dedique esta pasta para a análise exploratória (EDA) e prototipagem de modelos de machine learning propostos no PRD.

### 3. `.agent/` (Automação)
*   Centraliza os **Workflows** (`/analyze-data`, `/model-baseline`) que aceleram as tarefas repetitivas de análise e treino.

---

##  Regras de Ouro
1.  **Imutabilidade:** Nunca altere um arquivo em `data/raw`. Se o dado está errado, corrija-o via script de ETL.
2.  **Performance:** O dashboard deve ler sempre da pasta `processed` para evitar processamento pesado em tempo de execução.
3.  **Higiene:** Notebooks são para rascunhos; código reutilizável deve ser movido para `src/`.