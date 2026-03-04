# Pipeline de Limpeza de Dados (ETL) — Explicação Detalhada

A limpeza e o processamento dos dados salvos no diretório `data/processed` (que resultou no arquivo consolidado `olist_super_dataset.csv`) foram orquestrados através do script `src/etl/data_cleaning.py`.

Este processo utilizou uma combinação de práticas guiadas pelas **Skills** do sistema (como `data-analysis-eda`, `clean-code` e `python-patterns`), aplicadas pelo Agente Analista de Dados. O objetivo foi transformar um dataset fragmentado em vários arquivos CSV da Olist em uma base relacional única, higienizada e pronta para produção e visualização em Dashboard.

---

## 1. Orientação pelas Skills de Análise e Engenharia
O script foi construído seguindo diretrizes consistentes que priorizam um código limpo, tratamento de erros e um fluxo claro de *Exploratory Data Analysis* (EDA):

- **Isolamento de Estágios**: A extração (Extract), a transformação (Transform) e o salvamento (Load) foram divididos em etapas lineares explícitas e rastreáveis.
- **Eficiência de Memória e Carga**: Foram aplicadas funções vetorizadas com `pandas` para transformar colunas em sua totalidade de forma performática.
- **Tratamento Específico de Tipos**: Colunas que representam datas ou textos sujos foram higienizadas logo no início do processo.

---

## 2. Estrutura do Script `data_cleaning.py`

O script contém **1 função principal** e **1 bloco de entrada CLI**, organizados da seguinte forma:

```
data_cleaning.py
│
├── clean_and_merge_data(raw_data_dir, output_path)   ← Função principal (ETL completa)
│   ├── Etapa 1 — Ingestão (7 CSVs → 7 DataFrames)
│   ├── Etapa 2 — Limpeza e Tratamento
│   │   ├── 2.1  Filtro de status de pedidos (apenas 'delivered')
│   │   ├── 2.2  Conversão de colunas de data
│   │   ├── 2.3  Limpeza de texto (cidades)
│   │   └── 2.4  Tratamento de nulos (NaT)
34: │   ├── Etapa 3 — Feature Engineering
35: │   │   ├── tempo_entrega_dias  (cálculo e filtro 1 a 100 dias)
36: │   │   └── atraso_entrega      (flag booleano)
37: │   ├── Etapa 4 — JOINs (construção do super dataset)
38: │   │   ├── products ← translators   (tradução de categorias)
39: │   │   ├── orders   ← customers     (LEFT JOIN)
40: │   │   ├── merged   ← items         (LEFT JOIN)
41: │   │   ├── merged   ← products      (LEFT JOIN)
42: │   │   ├── merged   ← payments_agg  (LEFT JOIN)
43: │   │   └── merged   ← reviews_agg   (LEFT JOIN)
44: │   ├── receita_liquida = price + freight_value
45: │   ├── 4.3 Filtro de Outliers Financeiros (Price, Freight, Payment)
46: │   └── Etapa 5 — Exportação (CSV final)
│
└── __main__ (entrada CLI via argparse)
```

---

## 3. Passo a Passo Técnico da Limpeza

A limpeza seguiu estritamente as regras de negócio mapeadas para garantir a qualidade técnica e de negócio da tabela final.

### Etapa A: Ingestão e Auditoria Inicial

O script utiliza o `pandas` para carregar **7 arquivos `.csv` brutos**, transformando-os em DataFrames individuais.

### Etapa B: Aplicação de Regras de Negócio e Filtros

Para garantir que o dataset espelhe apenas transações finalizadas e seguras:

```python
valid_status = ['delivered']
orders = orders[orders['order_status'].isin(valid_status)].copy()
```

> **Resultado:** De **99.441** pedidos brutos, agora focamos apenas em **96.478** pedidos entregues (`delivered`).

### Etapa C: Tratamento de Tipos, Datas e Higienização Textual

Cinco colunas relacionadas a datas foram convertidas para `datetime`. A cidade do cliente foi normalizada removendo acentos e espaços extras.

### Etapa D: Engenharia de Recursos (Feature Engineering)

#### D.1 — `tempo_entrega_dias`
Representa o número inteiro de dias corridos entre a compra e a entrega. Foram filtrados apenas os registros onde:
- **`tempo_entrega_dias > 0`**
- **`tempo_entrega_dias <= 100`**

### Etapa E: Resolução de Duplicatas e Mesclagem (JOINs)

As tabelas de pagamentos e reviews foram agregadas antes do JOIN para evitar a explosão de linhas.
As 5 colunas de dimensões de produtos (`weight`, `length`, `height`, `width`, `name_lenght`) foram removidas para simplificar o dataset.

---

### Etapa F: Tratamento de Outliers Financeiros

Foram aplicados limites máximos para evitar distorções estatísticas:
- **Preço de Produto (`price`)**: Máximo de **R$ 2.000,00**.
- **Valor do Frete (`freight_value`)**: Máximo de **R$ 200,00**.
- **Valor total do Pagamento (`payment_value`)**: Máximo de **R$ 8.000,00**.

---

### Etapa G: Exportação do Super Dataset

**Resultado final: `olist_super_dataset.csv`**
- **~109.929 linhas**
- **27 colunas** (reduzido após limpeza de dimensões)