## 📋 Tabela de Referência

| Emoji | Tipo | Descrição | Exemplo |
| :--- | :--- | :--- | :--- |
| ✨ | `feat` | Nova funcionalidade ou componente | `✨ feat(viz): adiciona heatmap de calor por UF` |
| 🐛 | `fix` | Correção de bug ou erro nos dados | `🐛 fix(etl): corrige parse de data ISO 8601` |
| 🧹 | `chore` | Limpeza, refatoração ou manutenção | `🧹 chore(lint): aplica regras do ruff nos scripts` |
| 📝 | `docs` | Documentação (README, PRD, Markdown) | `📝 docs(prd): atualiza métricas de ticket médio` |
| 📦 | `data` | Atualização de datasets ou CSVs | `📦 data(raw): adiciona olist_sellers_dataset` |
| ⚙️ | `refactor` | Mudança no código que não altera comportamento | `⚙️ refactor(etl): otimiza joins de tabelas grandes` |
| 🧪 | `test` | Adição ou modificação de testes | `🧪 test(etl): adiciona teste unitário para nulos` |
| 🛠️ | `infra` | Configurações, dependências e ambiente | `🛠️ infra(env): adiciona pandas às dependências` |

---

## 📂 Escopos Comuns (`scope`)

- `etl`: Scripts de processamento, junção e limpeza de dados.
- `viz`: Dashboard Streamlit, gráficos e componentes de UI.
- `data`: Arquivos dentro da pasta `data/` (raw, interim, processed).
- `notebook`: Arquivos `.ipynb` de análise ou experimentação.
- `docs`: Documentação técnica e README.

## 🚀 Exemplo de Fluxo Eficiente

```bash
git commit -m "✨ feat(etl): implementa feature engineering de tempo de entrega"
git commit -m "📊 viz(dash): adiciona indicador de nota média de avaliação"
git commit -m "📝 docs(readme): atualiza instruções de instalação"
```
