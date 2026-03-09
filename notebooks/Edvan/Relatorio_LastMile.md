# Relatório Operacional: Supply Chain e Transporte Brasileiro (O Abismo da Última Milha)

**Data:** Março de 2026
**Público-Alvo:** Equipe de Supply Chain, Transportadoras Terceirizadas e Lojistas.

## 1. Contextualização: São Paulo não é o único vilão
Na Matriz de "Origem vs Destino" provamos que mais de 60% do nosso fluxo logístico é uma "Mão Única" do polo Sudeste para o resto do país.
Contudo, se a logística comercial brasileira fosse resolvida simplesmente alugando aviões-cargo entre Guarulhos e Manaus, o valor do frete não seria um problema.
**O terrorismo logístico mora na Última Milha ("Last-Mile").** A etapa onde o produto sai da Capital Hub (Ex: Salvdor, Manaus, Belém) e rasteja de caminhonete 300km asfalto afora até chegar ao município ribeirinho ou sertanejo final.

## 2. A Descoberta: O Degrau Intraestadual
Classificamos todas as cidades do Brasil entre **"Capitais/Hubs"** vs **"Interiores"**. Gerando Gráficos de Violino (Violin Plot) no nosso estudo técnico (`05_analise_last_mile.ipynb`), o diagnóstico geográfico se formou:

* **O Sul e Sudeste são Abençoados.** O Frete Mediano e o Tempo de Espera em São Paulo (Capital) vs São José do Rio Preto (Interior SP) são rigorosamente os mesmos (R$ 13/R$ 15). A densidade da malha rodoviária do Sudeste não pune quem mora distante no interior, por força da qualidade das estradas Anhanguera/Bandeirantes/etc e volume de frota local rodando.
* **O Degrau do Nordeste (+68% de Punição).** O fluxo Olist-Nordeste cai severamente aqui. Entregar mercadoria em Salvador/Fortaleza/Recife tem frete mediano suportável de **R$ 21,90** e leva 14 dias para quem desce de SP. **O problema acontece ao entrar no Sertão.** Sair de Salvador para uma cidade do interior baiano cobra um imposto cruel da transportadora: os valores de Frete deparam pra **R$ 36,90** de Mediana (aumentando bruscamente para 18 a 21 dias).
* **O Caos do Centro-Oeste.** Engana-se quem pensa que só o Norte é distante. Brasília e Goiânia são capitais interligadas ao Sudeste por malha pavimentada eficiente. O Frete é R$ 16,90. Mas ao comprar para o interior do Mato Grosso/Mato Grosso do Sul? Subimos a montanha russa para impressionantes **R$ 29,90** de Custo Mediano (Quase 100% de ágio).

## 3. Plano de Ação (Transportadoras)

A Olist está escoando dinheiro no gargalo regional porque continua dependendo da tabela fixa unificada dos Correios ou Grandes Transportadoras Nacionais na milha final. 
Como uma "TNT/Fedex/Correios" possui frota pesada, enfiar um caminhão grande no interior do Maranhão custa fortunas em pedágio, combustível e risco de furto.

* **Recomendação de Board:** Para o Norte e Nordeste, devemos abolir o fretamento unificado. 
A equipe de Supply Chain deve negociar com a Transportadora pesada **apenas a perna "Hub-to-Hub"** (Jogar o lote de SKUs do armazém de São Paulo no CD de Fortaleza através das BRs). 
Dali em diante, o *hand-off* (repassamento da carga) deve ser feito para as **Micro-Transportadoras Locais (Frotistas de Vãs ou Moto-Frete de Bairro e Cooperativas do Estado)**. Por conhecerem as vias não asfaltadas do município, atalhos de balsa e custarem barato em manutenção, essas cooperativas locais esmagarão os +68% de Punição do frete na Última Milha.
