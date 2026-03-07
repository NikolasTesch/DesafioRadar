# Resumo didático — `05_analise_last_mile.ipynb`

## O que este notebook quis responder

Este notebook investiga o gargalo da **última milha** na logística brasileira.  
A pergunta central é: **o problema do frete termina quando a mercadoria chega à capital da região, ou continua forte até o interior?**

A hipótese do estudo é que parte importante do custo e do atraso não vem apenas da longa distância entre estados, mas da etapa final de distribuição dentro da própria região.

## Bases de dados utilizadas

O notebook trabalha com uma base integrada que cruza:

- pedidos
- clientes
- localização do destino
- frete
- tempo de espera
- classificação geográfica da cidade

A ideia é comparar cidades classificadas como:

- **capital/hub**
- **interior**

## Preparação e tratamento dos dados

Uma etapa central do notebook é a criação de um dicionário manual com capitais brasileiras para classificar cada cidade do destino em:

- capital
- interior

Depois, o estudo combina isso com:

- região
- frete
- tempo de espera

Também há filtragem de fretes extremos para melhorar a visualização das distribuições.

## Principais análises realizadas

### 1. Comparação entre capital e interior
O notebook usa gráficos do tipo violin plot para comparar, dentro de cada região:

- custo de frete
- tempo de espera

entre capitais e interiores.

A lógica é muito boa do ponto de vista de negócio, porque ela separa dois problemas diferentes:

- chegar até o grande centro regional
- completar a entrega até o destino final

### 2. Tabela de medianas por região e tipo de cidade
Além do gráfico, o notebook calcula uma tabela analítica com medianas de frete e prazo.

Isso permite sair da percepção visual e trazer números mais concretos para a leitura operacional.

### 3. Identificação do “degrau” da última milha
A conclusão do notebook é que o interior de algumas regiões sofre um salto importante de custo e prazo em relação às capitais.

O relatório complementar destaca especialmente:

- **Nordeste**: capital com frete mediano em torno de **R$ 21,90**, interior em torno de **R$ 36,90**
- **Centro-Oeste**: forte salto de custo quando sai da capital e vai para o interior
- **Sudeste**: diferença bem menor entre capital e interior

Em linguagem simples: em algumas regiões, chegar à capital é só metade da viagem; a parte mais cara e mais difícil ainda vem depois.

## Principais insights do notebook

1. **A última milha é um problema real e desigual no Brasil.**  
   O custo adicional do trecho final não pesa da mesma forma em todas as regiões.

2. **Capitais e interiores não devem ser tratados como a mesma operação logística.**  
   Em regiões mais desafiadoras, o interior exige outra lógica de custo e prazo.

3. **O Nordeste e partes do Centro-Oeste mostram um degrau logístico relevante.**  
   O salto de custo entre capital e interior é muito mais visível.

4. **No Sudeste, a malha é mais capilarizada e eficiente.**  
   A diferença entre capital e interior tende a ser menor, o que reduz a penalização logística do destino final.

## O que esse notebook agrega para o “grande resumo”

Este notebook é importante porque aprofunda o diagnóstico da regionalidade.  
Enquanto o notebook 02 mostra o problema macro da origem e do destino, este aqui mostra que **mesmo depois de a mercadoria chegar à região certa, ainda pode existir um gargalo severo para completar a entrega**.

Ele é o estudo que melhor traduz o conceito de “última milha” em termos práticos.

## Ações sugeridas pelo material

Com base no notebook e no relatório complementar, algumas ações coerentes seriam:

- negociar estratégias diferentes para trecho hub-to-hub e trecho final
- usar parceiros logísticos regionais ou microtransportadoras
- revisar malha e contratos para interior de regiões mais críticas
- adaptar SLA e expectativa do cliente conforme perfil do destino

## Conclusão em linguagem simples

Se fosse para explicar este notebook para alguém de fora da área, eu diria:

> O estudo mostra que o frete não termina quando o produto chega perto do cliente.  
> Em várias regiões, especialmente quando a entrega vai para o interior, o trecho final fica muito mais caro e lento.  
> Ou seja: a última etapa da entrega é um dos principais gargalos da operação.
