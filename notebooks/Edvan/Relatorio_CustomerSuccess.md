# Relatório de Inteligência: Customer Success (Satisfação vs Logística)

**Data:** Março de 2026
**Público-Alvo:** Equipe de SAC, Relações Públicas e Diretoria Operacional.

## 1. O Diagnóstico: O Produto é Ruim ou a Logística é Falha?
Um dos maiores temores de um E-commerce (Marketplace) é ver sua nota em sites de proteção ao consumidor desabar. Historicamente, a loja (Olist) vinha sofrendo punições severas no seu *Net Promoter Score* em certas vendas pontuais.
Ao cruzar a base de Avaliações de Compra (`olist_order_reviews_dataset`) geramos mais de 96.000 avaliações com notas de 1 a 5 estrelas e cruzamos esses dados com o banco Logístico Regional (`03_analise_satisfacao.ipynb`).

## 2. A Correlação Matemática da Crise
A "Teoria do Atraso" não é apenas intuição, é o fator determinante de queima de reputação provado em nossos gráficos:
* **Promotores (Nota 5):** Em média, clientes que dão a nota máxima receberam suas mercadorias em tempo recorde (média de **9.7 dias** de espera histórica).
* **Detratores (Nota 1):** Clientes que esmagaram a reputação da loja preenchendo 1 estrela nas avaliações aguardaram absurdos **21 dias em média** pela sua mercadoria. 

**Conclusão Prática:** O cliente não destrói a nota porque o produto chegou quebrado ou ruim. Ele pune a loja porque a transportadora demorou a entregar, e ele não faz distinção entre quem vende e quem entrega.

## 3. O Risco de Imagem Geolocalizado
Sendo a demora a causa matriz da insatisfação, cruzamos novamente a tabela para encontrar os estados do Brasil onde somos mais "odiados" digitalmente.
Mapeamos o volume de "Detratores" (a soma estrita das notas 1 e 2) sobre o total de vendas de cada região:

1. **A Fortaleza:** O Sudeste ostenta o menor patamar de detratores do país (Teto de 13.9%). Como seus clientes recebem o produto rápido (visto que 60% dos lojistas também estão em SP), eles perdoam eventuais outros problemas.
2. **A Zona Vermelha:** O Norte engole quase **20% de Detratores**! Quase a cada 5 compras feitas lá, 1 cliente sai profundamente irritado pela demora sistêmica já evidenciada nos relatórios anteriores. O Nordeste segue pouco atrás com mais de 18% de taxa de insatisfação.

---

## 4. O Custo (CAC) e a Proposta de Ação para o SAC

### O Sangramento Financeiro
Se 20% do Norte odeia a nossa marca por demora, nós temos um Custos de Aquisição (CAC) perdido. O dinheiro gasto em publicidade para atrair aquele cliente foi incinerado, pois ele **jamais voltará a fazer uma recompra**, matando a métrica do LTV (*Lifetime Value*).

### Manejo de Crise e Proposta Operacional (Socrática)

* **SAC Preditivo:** Não basta esperar o cliente reclamar com 30 dias de atraso. O Banco de Dados prova que o "Ponto de Quebra" da nota ocorre aos 20 dias. A equipe de Engenharia deve plugar uma automação (*Trigger*). Se o pedido constar em trânsito há mais de **15 dias**, o sistema de SAC dispara um WhatsApp humanizado com atualizações diárias, estancando a ira do cliente antes dela virar uma Nota 1.
* **Apaziguamento Reverso (*Cupom Desconto*):** O SAC não tem o poder de abrir Fábricas no Norte. Mas ele tem poder de caixa. Clientes que sofreram as falhas logísticas identificadas no Norte/Nordeste devem receber automações de Cupons Fixos (`BEMVINDO_DEVOLTA_20`) para a segunda compra. O desconto subsidia o frete na mente do consumidor e salva o LTV (Vida Útil do Cliente).
