# PRD — B-Comm Analytics (Brazilian E-commerce Analytics)

## 1. Visão Geral
O **B-Comm Analytics** é uma plataforma de inteligência de dados de ponta a ponta, projetada para transformar o dataset relacional da Olist (2016-2018) em um ecossistema analítico interativo. A solução integra engenharia de dados em Python, persistência em PostgreSQL, uma API escalável em Node.js e um dashboard dinâmico em Vanilla Web (HTML/CSS/JS).

*   **Problema:** O dataset da Olist é fragmentado em múltiplos arquivos CSV, dificultando a extração imediata de insights sobre vendas, logística e satisfação no e-commerce brasileiro.
*   **Solução:** Uma arquitetura robusta que processa, limpa e centraliza os dados, disponibilizando-os através de uma API para consumo em uma interface visual premium e interativa.
*   **Valor:** Entrega uma visão clara do ciclo de vida do pedido, permitindo que gestores identifiquem gargalos logísticos e oportunidades de negócio com fundamentação técnica sólida.

---

## 2. Pipeline de Desenvolvimento (Roadmap)

### Etapa 1: Coleta e Ingestão de Dados (Python)
*   **O que será executado:** A equipe utilizará a biblioteca Pandas para carregar os arquivos `.csv` brutos (orders, order_items, customers, products, reviews, etc.). Cada arquivo será lido com `pd.read_csv()` e alocado em seu próprio DataFrame inicial.
*   **Por que será feito dessa forma:** O dataset é relacional e fragmentado. Antes de qualquer análise ou cruzamento, o Python precisa ter cada "peça do quebra-cabeça" carregada na memória de forma independente e estruturada.

### Etapa 2: Limpeza e Tratamento Isolado (Python)
*   **O que será executado:** Auditoria de cada DataFrame antes da junção. Serão identificados nulos (`isnull()`), colunas de tempo (ex: `order_purchase_timestamp`) serão convertidas para objetos de data reais (`pd.to_datetime()`) e strings textuais serão padronizadas (remoção de acentos e letras minúsculas).
*   **Por que será feito dessa forma:** Evita erros em análises de série temporal futuro. A limpeza prévia garante a integridade referencial e evita a propagação de "lixo" para a etapa de visualização.

### Etapa 3: Modelagem e Mesclagem (Python)
*   **O que será executado:** Uso intensivo de `pd.merge()`, elegendo a tabela de Pedidos (`orders`) como a espinha dorsal para acoplar Clientes, Itens, Pagamentos e Produtos.
*   **Por que será feito dessa forma:** A estatística descritiva precisa de contexto. Esta etapa cria um "Super DataFrame" consolidado, pronto para cálculos complexos como "ticket médio por região" ou "frete por categoria".

### Etapa 4: Análise Exploratória Descritiva (Python e Matplotlib)
*   **O que será executado:** Aplicação de agregações (`groupby`) e funções estatísticas do NumPy. Serão gerados gráficos estáticos em Matplotlib para validação interna.
*   **Processos:** Cálculo do funil de vendas e ciclo de vida do pedido (da aprovação à entrega).
*   **Insights:** Ticket Médio regional, categorias com atrasos logísticos e correlação entre tempo de entrega e avaliação do cliente.
*   **Por que será feito dessa forma:** É aqui que os números frios são transformados em inteligência de negócio e respostas claras sobre as dores do e-commerce.

### Etapa 5: Arquitetura de Banco de Dados e API (PostgreSQL e Node.js)
*   **O que será executado:** Os DataFrames processados serão exportados para um banco PostgreSQL estruturado. Em paralelo, um servidor Node.js criará uma API com rotas específicas (ex: `/api/vendas-mensais`) que consultarão o banco e devolverão métricas em JSON.
*   **Por que será feito dessa forma:** O PostgreSQL garante segurança e escalabilidade, enquanto a API em Node.js cria uma ponte leve e assíncrona entre o back-end e a interface gráfica.

### Etapa 6: Desenvolvimento do Dashboard Interativo (HTML, CSS e JavaScript)
*   **O que será executado:** Construção da camada visual. O front-end fará requisições assíncronas (`fetch`) para a API Node.js, capturará os JSONs e desenhará os gráficos interativos e cartões de métricas diretamente no navegador.
*   **Por que será feito dessa forma:** Cumpre a exigência de dashboard interativo com uma solução customizada, unindo engenharia de back-end com design e usabilidade de ponta.

### Etapa 7: Visão de Futuro e Propostas de ML (Apresentação Estratégica)
*   **Proposta 1 (Predição de Logística):** Utilizar algoritmos clássicos de Machine Learning (como Random Forest ou XGBoost via Scikit-learn) para prever o risco de atraso de uma entrega no momento da compra, permitindo a gestão proativa de expectativas do cliente.
*   **Proposta 2 (Segmentação de Clientes - RFM):** Implementar modelos de Clustering (K-Means) para agrupar clientes por Recência, Frequência e Valor Monetário (RFM). Isso permite identificar "clientes campeões", "em risco de churn" ou "potenciais novos" para estratégias de marketing personalizadas.
*   **Proposta 3 (Previsão de Demanda/Time Series):** Utilizar modelos de séries temporais (Prophet ou ARIMA) para prever o volume de vendas dos próximos meses por categoria de produto, otimizando o planejamento de estoque dos vendedores.
*   **Proposta 4 (Sistemas de Recomendação):** Desenvolver um motor de recomendação baseado em Filtragem Colaborativa ou análise de "Cesta de Compras" (Regras de Associação) para sugerir produtos complementares no checkout, aumentando o Ticket Médio.
*   **Proposta 5 (Automação Inteligente e Agentes de IA):** Integrar agentes de IA (via plataformas como n8n ou LangChain) que analisam sentimentos em avaliações  de nota 1 ou 2. Se um atraso for detectado, o agente aciona automaticamente uma automação para disparar um e-mail de desculpas com um cupom de desconto personalizado.

*   **Por que será feito dessa forma:** Demonstra que a análise do passado (descritiva) é apenas a fundação. O real valor do dado surge ao automatizar e prever o futuro (preditiva e prescritiva), transformando o dashboard de uma ferramenta de "olhar para trás" em um motor de decisão estratégica.

---

## 3. Requisitos Técnicos

### 3.1. [ETL] Processamento e Engenharia de Dados (Python)
- [ ] **Modelagem de Dados (Joins)**: UNIR `olist_orders_dataset` (fato) com Itens, Clientes, Pagamentos, Avaliações e Produtos.
- [ ] **Limpeza e Padronização**:
    - Tradução de categorias (`product_category_name`) para inglês/padronizado.
    - Conversão de tipos: Timestamps para objetos `datetime`.
    - Higienização de strings: Remoção de acentos e capitalização.
- [ ] **Engenharia de Recursos (Feature Engineering)**:
    - **Tempo de Entrega (Dias)**: Diferença entre `order_delivered_customer_date` e `order_purchase_timestamp`.
    - **Atraso na Entrega**: Booleano identificando se a data real ultrapassou a estimada.
    - **Receita Líquida**: Soma do `price` + `freight_value`.

### 3.2. [BACK] API e Persistência (PostgreSQL & Node.js)
- [ ] **Schema do Banco**: Criação de tabelas otimizadas para consulta analítica no PostgreSQL.
- [ ] **Endpoints da API**:
    - `GET /api/kpis`: Retorno de GMV, total de pedidos e ticket médio.
    - `GET /api/vendas/evolucao`: Dados para gráfico de linha temporal.
    - `GET /api/logistica/desempenho`: Médias de entrega por estado.
    - `GET /api/produtos/ranking`: Top 10 categorias mais rentáveis.

### 3.3. [DASH] Frontend e Visualização (HTML/CSS/JS)
- [ ] **Layout Premium**:
    - Interface baseada em **Glassmorphism** e **Dark Mode**.
    - Tipografia moderna (Inter ou Outfit).
- [ ] **Componentes de Visualização (Charts)**:
    - **Gráfico de Evolução**: Linha (Receita vs Tempo).
    - **Ranking de Categorias**: Barras horizontais.
    - **Performance Regional**: Gráfico de barras verticais (Dias de Entrega por Estado).
    - **Mix de Pagamento**: Gráfico de Donut.
    - **Heatmap de Sazonalidade**: Cruzamento de Dia da Semana vs Hora do Dia.
- [ ] **Interatividade Dinâmica**:
    - Filtros na sidebar (Data, Estado, Categoria) que atualizam os componentes via `fetch`.
    - Botão de exportação para CSV dos dados filtrados.

---

## 4. Regras de Negócio (Business Rules)

### 4.1. Definição de Venda e Receita (GMV)
*   **Status Válidos**: Para cálculos de performance de vendas e GMV, serão considerados apenas pedidos com status `delivered`, `shipped` e `invoiced`. Pedidos `canceled` ou `unavailable` são excluídos das métricas de receita.
*   **Cálculo do GMV**: Definido como a soma de `price` (valor do produto) + `freight_value` (valor do frete) de todos os itens de pedidos válidos.
*   **Ticket Médio**: Calculado dividindo o GMV total pelo número de `order_id` únicos.

### 4.2. Logística e Performance de Entrega
*   **Tempo de Entrega Real**: Calculado em dias corridos entre `order_purchase_timestamp` e `order_delivered_customer_date`.
*   **Prazo Estimado**: Comparação entre `order_delivered_customer_date` e `order_estimated_delivery_date`.
*   **Tratamento de Dados Incompletos**: Pedidos sem data de entrega real (mesmo que marcados como entregues) devem ser desconsiderados no cálculo de média de tempo, para evitar distorções estatísticas.

### 4.3. Análise Geográfica e Temporal
*   **Granularidade Regional**: Os dados serão agregados por Estado (UF) do cliente. Diferenças de fuso horário não serão tratadas, utilizando o horário padrão do timestamp do servidor Olist.
*   **Padronização de Categorias**: Categorias com menos de 1% de representatividade no volume total podem ser agrupadas em "Outros" para melhorar a legibilidade dos rankings.

### 4.4. Avaliação e Satisfação
*   **NPS Simulado**: A nota de `review_score` (1-5) será a base para o índice de satisfação.
    *   **Promotores**: Notas 5.
    *   **Neutros**: Notas 4.
    *   **Detratores**: Notas 1 a 3.

---

## 5. Fluxo de Usuário (User Flow) Detalhado

### 5.1. Jornada de Descoberta (Acesso Inicial)
1.  **Splash & Loading**: Ao acessar a URL, o usuário visualiza uma animação de *skeleton loading* enquanto o frontend faz o *handshake* com a API Node.js e o PostgreSQL processa as agregações iniciais.
2.  **Visão Holística**: O dashboard renderiza primeiro os **4 Cards de KPI** no topo. O usuário identifica imediatamente a saúde financeira e operacional do período total.

### 5.2. Investigação e Drill-down (Filtros)
3.  **Filtragem Temporal**: O usuário ajusta o slider de data para analisar a Black Friday de 2017.
4.  **Ação Reativa**: Todos os gráficos realizam uma transição suave (*CSS Transitions*) para refletir os novos números. O gráfico de barras de categorias mostra o pico de "Beleza e Saúde".
5.  **Filtro por Estado**: O usuário clica em "SP" no ranking ou seleciona no dropdown. O dashboard foca apenas nos dados de São Paulo, revelando se os atrasos são locais ou nacionais.

### 5.3. Análise de Causa Raiz
6.  **Insights Cruzados**: O usuário observa o gráfico de "Satisfação vs Atraso". Ao filtrar por pedidos atrasados, ele nota a queda drástica na nota média, validando a hipótese de que a logística é o principal detrator do negócio.

### 5.4. Extração de Valor
7.  **Exportação**: Após segmentar os dados de uma categoria crítica, o usuário clica no botão "Exportar Relatório". O sistema gera um arquivo CSV contendo os dados desnormalizados e tratados apenas daquela seleção para uso em ferramentas externas.

---

## 6. Fora do Escopo (Out of Scope)

*   **Geolocalização via Coordenadas:** Análises espaciais limitadas a agregações estaduais (UF).
*   **Análise de Vendedores (Sellers):** Foco exclusivo no comportamento do consumidor e logística de pedidos.
*   **Processamento de Linguagem Natural (NLP):** Uso apenas da nota numérica (`review_score`) para análise de satisfação.
*   **Predição em Tempo Real:** Modelos preditivos (Etapa 7) são conceituais/estratégicos e não rodarão em tempo real no dashboard.
*   **Sincronização de Dados Vitalícia:** Projeto baseado no dataset estático da Olist (2016-2018).
*   **Sistema de Login:** Acesso público e irrestrito.
