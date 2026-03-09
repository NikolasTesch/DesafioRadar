# Relatório de Inteligência: Marketing e Mix de Produtos (Categorias vs Logística)

**Data:** Março de 2026
**Público-Alvo:** Equipe Comercial, Tráfego Pago (Ads) e Inteligência de Mercado.

## 1. O Paradoxo do Consumo Regional
Será que um brasileiro do Norte consome produtos diferentes de um brasileiro do Sul? Ou será que ele consome a *mesma coisa*, mas o funil de compras é castrado pela Matemática do Frete?
Para responder a isso, atrelamos mais de 90.000 itens vendidos às suas respectivas Classes (`olist_products_dataset.csv`), traduzimos para o inglês para padronização gráfica corporativa (`product_category_name_translation.csv`) e cruzamos com a base demográfica e de preços (Vide Notebook `04_analise_categorias.ipynb`).

## 2. O Mix de Produtos: O Brasileiro é Um Só
Ao isolarmos as vendas absolutas por Região e checarmos o *Market Share* de cada categoria de forma percentual e parametrizada, a conclusão é clara: **Não existe diferença drástica de gosto entre as regiões.**
* **Saúde & Beleza (Health/Beauty)**, **Cama/Mesa/Banho** e **Esportes/Lazer** compõem os 3 grandes pilares do e-commerce Olist de ponta a ponta do país.

Se o gosto catalográfico é o mesmo, onde mora o grande diferencial geográfico nas vendas?

---

## 3. O Abismo do Ticket Médio (Sensibilidade ao Frete)
O diferencial mora no *Preço do Item* que o cliente resolve botar no carrinho.

Pela Lei da Utilidade Econômica da Logística: **O frete não pode superar ou empatar com o preço do produto bruto**, sob pena de altíssimas taxas de abandono de carrinho.
Criamos um Boxplot (Gráfico de Caixa) filtrando itens de consumo em massa (< R$ 1000) e ranqueando-os por região. Eis o achado irrefutável:

* **Sudeste (Frete Médio R$ 15):** O consumidor do Sudeste compra qualquer coisa na internet, pois o frete viabiliza isso. O Ticket Mediano do item que ele compra é de **R$ 65,00**. 
* **Norte / Nordeste (Frete > R$ 38):** Ninguém paga 40 reais de frete para comprar um relógio ou capinha de 20 reais. Quando o cliente do Nordeste entra no funil Olist, ele eleva violentamente o padrão da cesta de compras para compensar o Custo de Logística, saltando para um Ticket Mediano de **R$ 89,00 a R$ 90,00**.

O Nordestino não é que compre menos quantitativamente apenas por poder aquisitivo; ele compra menos porque todo o catálogo "barato" do e-commerce fica financeiramente inútil para ele devido à Origem do Estoque em São Paulo (Rota 1).

---

## 4. Plano de Ação (Propostas Práticas)

### Otimização de ROI no Tráfego Pago (Geo-Targeting)
O tempo da nossa agência de Marketing (Meta Ads / Google Ads) subir "Campanhas Nacionais" genéricas acabou!
- Anunciar para as praças de MS, MT, Norte e Nordeste produtos do Catálogo que custem *menos de R$ 60 reais* é queimar o dinheiro dos investidores. O clique no Anúncio (CPC) via rede social acontecerá, mas quando o usuário calcular o frete no carrinho, a taxa de rejeição será imediata.
- **Solução Imediata:** A partir de hoje, as campanhas digitais geolocalizadas para fora da Bacia Sul-Sudeste devem conter apenas carrosséis/produtos com o **Ticket superior a R$ 90 (Eletrônicos, Informática, Móveis, Eletro, Combos/Kits Atacado)**.

### Combos e Bundles de Venda Cruzada
Para o Norte/Nordeste, se o departamento comercial quiser continuar vendendo "Health e Beauty" baratos, ele precisa obrigatoriamente forçar um UX de "Kits" no Front-End. O cliente não pode comprar "1 Creme Hidratante" pra entregar no Amapá, o sistema de recomendação deve exibir exclusivamente o "Kit Leve 4 Pague 3", elevando o preço da cesta para R$ 100+ de forma a encolher a dor psicológica do Frete alto.
