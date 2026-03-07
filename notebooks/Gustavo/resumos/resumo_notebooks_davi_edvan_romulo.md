# Resumo consolidado de notebooks — Davi, Edvan e Rômulo

## Como usar este arquivo
Este resumo foi pensado para servir como camada de contexto curta para agentes e para leitura humana rápida. Cada item abaixo aponta o caminho do notebook-fonte e registra apenas o que vale reaproveitar no notebook integrador do projeto. Quando for necessário aprofundar, a consulta deve ser feita diretamente no notebook original.

---

## 1) Davi — Análise Estratégica de E-commerce
**Referência:** `notebooks/Davi/Analise_Estrategica_Ecommerce.ipynb`

**Foco do notebook:**
Integrar dados de pedidos, itens, clientes, produtos, pagamentos e avaliações para analisar como logística, frete e características do produto se relacionam com a experiência do cliente.

**Anotações úteis:**
- Monta uma base analítica unificada a partir das tabelas centrais da Olist, com variáveis úteis para análises posteriores, como `tempo_real_entrega_dias`, `dias_atraso`, `flag_atraso`, `review_score`, `freight_value`, `price`, `product_weight_g` e agregações por período.
- A linha principal do notebook é a relação entre operação logística e satisfação: atrasos e maior tempo de entrega aparecem associados a piores avaliações, enquanto peso e dimensões do pedido ajudam a explicar o aumento do frete.
- Também traz uma visão executiva do negócio com evolução de receita/volume ao longo do tempo e visualizações para explorar segmentações operacionais e comerciais.
- Há uma etapa final de modelagem para previsão de atraso com regressão logística, usando principalmente frete, preço, peso e quantidade de fotos do produto. Essa parte é útil como direção analítica, mas deve ser revalidada no ambiente final antes de entrar como conclusão do projeto.

**O que vale aproveitar no notebook final:**
- A estrutura da base analítica e as features de atraso.
- A narrativa “logística impacta satisfação”.
- As variáveis que conectam frete, prazo e avaliação em uma mesma análise.

---

## 2) Davi — Análise de Sazonalidade
**Referência:** `notebooks/Davi/Analise_Sazonalidade.ipynb`

**Foco do notebook:**
Entender o comportamento temporal das vendas, identificar picos sazonais e separar tendência de crescimento de padrões recorrentes de demanda.

**Anotações úteis:**
- Consolida pedidos com informação temporal e valor financeiro para montar uma série histórica de vendas, usando principalmente `order_purchase_timestamp` e `total_order_value`.
- Extrai atributos de tempo como mês, ano, dia da semana e período mensal, o que permite estudar ritmo semanal, evolução mensal e decomposição da série temporal.
- A decomposição estatística destaca crescimento do negócio ao longo do período e reforça a presença de sazonalidade, com picos concentrados no fim do ano e em períodos promocionais como Black Friday.
- O notebook também usa K-Means para classificar meses em faixas de demanda e compara formas de pagamento com valor do pedido, sugerindo que cartão de crédito concentra compras de maior ticket.

**O que vale aproveitar no notebook final:**
- A leitura de sazonalidade para campanhas e planejamento de estoque.
- A ideia de segmentar meses em baixa, média e alta demanda.
- A relação entre calendário comercial, ticket e forma de pagamento.

---

## 3) Edvan — Regionalidade
**Referência:** `notebooks/Edvan/02_analise_regionalidade.ipynb`

**Foco do notebook:**
Mostrar como a geografia afeta volume de vendas, frete, tempo de entrega e fluxo entre origem do vendedor e destino do cliente.

**Anotações úteis:**
- Constrói uma base com pedidos, clientes, itens, pagamentos e depois adiciona vendedores para conectar destino do cliente com origem do produto.
- Mostra forte concentração de mercado no Sudeste, enquanto Norte e Nordeste aparecem com fretes e tempos de espera mais altos.
- A distribuição dos vendedores ajuda a explicar parte do problema: a oferta está concentrada em São Paulo/Sudeste, o que força rotas longas para várias regiões do país.
- A parte mais útil do notebook é a matriz origem-destino e a comparação entre compras “dentro da mesma região” e compras “entre regiões”, porque isso ajuda a separar o efeito da distância logística do efeito da demanda.

**O que vale aproveitar no notebook final:**
- A tese de concentração geográfica da oferta.
- A leitura de desigualdade logística entre regiões.
- A matriz origem-destino como peça central para explicar frete alto e prazo maior fora do eixo principal.

---

## 4) Edvan — Satisfação do cliente
**Referência:** `notebooks/Edvan/03_analise_satisfacao.ipynb`

**Foco do notebook:**
Relacionar avaliação da compra com desempenho logístico, especialmente tempo de espera e atraso percebido pelo cliente.

**Anotações úteis:**
- Junta `review_score` à base logística para medir como a nota varia quando o prazo aumenta.
- A evidência principal do notebook é uma associação forte entre demora na entrega e pior avaliação: pedidos com notas baixas tendem a ter maior tempo médio de espera.
- O recorte regional reforça o diagnóstico operacional: Norte e Nordeste concentram proporção maior de clientes detratores do que o Sudeste, o que sugere que a experiência pior não está distribuída de forma homogênea pelo país.
- Esse notebook funciona como ponte entre operação e marca, porque mostra que a logística não afeta apenas custo: ela afeta reputação e percepção de qualidade.

**O que vale aproveitar no notebook final:**
- A ligação entre tempo de entrega e `review_score`.
- A comparação regional de detratores.
- O argumento de que melhoria logística também é melhoria de experiência do cliente.

---

## 5) Edvan — Categorias e mix de mercado
**Referência:** `notebooks/Edvan/04_analise_categorias.ipynb`

**Foco do notebook:**
Comparar categorias mais vendidas por região e entender se a diferença regional está no gosto do consumidor ou no ticket viável diante do frete.

**Anotações úteis:**
- Calcula a participação das categorias dentro de cada região em vez de olhar apenas volume bruto, o que reduz o efeito da dominância do Sudeste.
- O notebook sugere que o mix principal de categorias é relativamente parecido entre regiões; a diferença mais forte não parece estar no “gosto”, mas no tipo de compra que continua financeiramente viável depois do frete.
- Norte e Nordeste aparecem com ticket mediano mais alto, o que indica sensibilidade maior ao custo logístico: itens baratos perdem atratividade quando o frete pesa demais na compra.
- A leitura é valiosa para marketing e comercial, porque mostra que a limitação regional pode estar mais ligada à estrutura de custo do que à preferência de catálogo.

**O que vale aproveitar no notebook final:**
- A distinção entre “gosto regional” e “ticket viável”.
- A ideia de sensibilidade ao frete para produtos baratos.
- O uso do recorte por categoria como apoio para decisões de mídia, mix e bundles.

---

## 6) Edvan — Last mile
**Referência:** `notebooks/Edvan/05_analise_last_mile.ipynb`

**Foco do notebook:**
Investigar o gargalo da última milha, comparando capitais e interiores para medir onde o frete e o prazo pioram mesmo depois que a carga chega à região de destino.

**Anotações úteis:**
- Classifica cidades entre capital e interior para criar um recorte operacional que o dataset não entrega pronto.
- Compara frete e tempo de espera por região nesse recorte, mostrando que o problema não é apenas “distância entre estados”, mas também a distribuição final dentro da própria região.
- O efeito aparece com mais força em regiões como Nordeste e Centro-Oeste, enquanto Sul e Sudeste tendem a mostrar menor diferença entre capital e interior.
- Esse notebook complementa o de regionalidade porque aprofunda a origem do custo logístico: parte relevante da punição está na etapa final da entrega, não só no envio interestadual.

**O que vale aproveitar no notebook final:**
- A separação entre custo interestadual e custo de última milha.
- O recorte capital vs interior como explicação operacional concreta.
- A hipótese de hubs regionais e parceiros locais como resposta logística.

---

## 7) Rômulo — Categorias de produto (visão executiva)
**Referência:** `notebooks/romulo/romulo.ipynb`

**Foco do notebook:**
Cruzar receita por categoria com ofensores logísticos e sinais de insatisfação para priorizar, em linguagem executiva, onde a operação e o comercial devem atuar primeiro.

**Anotações úteis:**
- Trabalha diretamente sobre o dataset consolidado do projeto e monta métricas por categoria como receita total, nota média, percentual de avaliações críticas (notas 1 e 2), percentual do frete sobre o ticket, taxa de atraso e recortes de horário/mês.
- A leitura principal é de priorização: nem sempre a categoria mais importante é a que mais vende, mas sim a que combina receita relevante com frete pesado, atrasos e pior experiência do cliente.
- O notebook destaca categorias de maior atrito operacional, com ênfase em itens mais pesados e estruturais — especialmente **Móveis de Escritório** — e também sinaliza risco em **Informática Acessórios** quando a taxa de insatisfação severa sobe acima do patamar médio.
- Também adiciona duas camadas acionáveis para negócio: janelas de maior conversão ao longo do dia (com concentração principalmente entre **13h–16h** e **19h–21h**) e leitura sazonal por categoria, útil para estoque e mídia.

**O que vale aproveitar no notebook final:**
- A matriz executiva **receita x frete x atraso x satisfação** para priorização de categorias.
- O recorte de categorias com frete muito invasivo em relação ao valor do produto.
- As janelas horárias de maior conversão e o apoio da sazonalidade por categoria para decisões comerciais.

---

## Síntese para o notebook integrador do dataset
Os sete notebooks convergem para uma leitura única do negócio:

1. **A geografia da oferta importa.** A operação é fortemente puxada pelo eixo Sudeste, e isso ajuda a explicar por que várias regiões compram com frete maior e prazo pior.
2. **Frete e prazo afetam mais do que custo.** Eles também afetam satisfação, reputação e chance de recompra, então logística deve ser tratada como variável de experiência do cliente.
3. **A sazonalidade precisa entrar no desenho final.** O comportamento das vendas não é estático: há crescimento no período observado e picos relevantes no fim do ano e em datas promocionais.
4. **O problema regional não parece ser preferência de consumo.** O mix de categorias é relativamente parecido entre regiões; o que muda com mais força é o ticket que continua compensando diante do frete.
5. **A última milha é parte central do gargalo.** Em algumas regiões, especialmente fora das capitais, a etapa final da entrega amplia custo e prazo de forma relevante.
6. **Nem toda categoria deve ser tratada igual.** A priorização executiva fica melhor quando receita é lida junto com peso do frete, taxa de atraso e avaliações críticas.

## Sugestão de uso pelo agente
Se o objetivo for construir um notebook final único sobre o dataset inteiro, este resumo já aponta os eixos principais a combinar:
- sazonalidade e calendário comercial;
- concentração geográfica de vendedores e clientes;
- frete e prazo como determinantes de satisfação;
- ticket/categoria por região;
- capital vs interior como aprofundamento logístico;
- priorização de categorias por receita, frete, atraso e insatisfação.

Esses eixos podem ser transformados em uma narrativa única: **estrutura logística -> custo e prazo -> comportamento de compra -> satisfação do cliente**.
