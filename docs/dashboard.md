# Dashboard Executivo de Vendas

## Métricas e gráficos

| Gráfico | Tipo | Métrica | Dimensão |
|---|---|---|---|
| KPI - Faturamento Total | Big Number | `SUM(valor_total)` | — |
| KPI - Total de Vendas | Big Number | `COUNT(DISTINCT id_venda)` | — |
| KPI - Ticket Médio | Big Number | métrica salva `ticket_medio` | — |
| KPI - Itens Vendidos | Big Number | `SUM(quantidade)` | — |
| Evolução Mensal do Faturamento | Linha temporal | `SUM(valor_total)` | `data`, mês |
| Faturamento por Categoria | Barras | `SUM(valor_total)` | `categoria` |
| Faturamento por Região | Barras | `SUM(valor_total)` | `regiao` |
| Top 10 Produtos por Faturamento | Barras | `SUM(valor_total)` | `produto` |
| Vendas por Forma de Pagamento | Donut | `COUNT(DISTINCT id_venda)` | `forma_pagamento` |

A métrica salva `ticket_medio` utiliza `SUM(valor_total) / COUNT(DISTINCT id_venda)`. Configure-a na aba Metrics do dataset antes de criar o KPI correspondente.

## Criar os gráficos via MCP

1. Liste os datasets e confirme o dataset analítico no banco DW Vendas, schema gold.
2. Use `get_dataset_info` para confirmar colunas e métricas.
3. Consulte `get_chart_type_schema` para o tipo desejado.
4. Crie cada gráfico com `generate_chart`, usando `save_chart: true` e o ID real do dataset.
5. Verifique o resultado com `get_chart_info` e `get_chart_data`.
6. Localize os nove gráficos com `list_charts` e crie o dashboard com `generate_dashboard`.

Não reutilize IDs de outra instalação nem duplique objetos existentes.

Na interface MCP utilizada, os tipos de configuração são `big_number`, `xy` para linhas/barras e `pie` para pizza/Donut. Confirme os parâmetros na versão instalada.

Exemplo de configuração de faturamento:

```json
{
  "chart_type": "big_number",
  "metric": {"name": "valor_total", "aggregate": "SUM"},
  "subheader": "Faturamento Total",
  "y_axis_format": ",.2f"
}
```

Para Ticket Médio, use `{"name": "ticket_medio", "saved_metric": true}`. Para vendas, use `COUNT_DISTINCT` sobre `id_venda`. Para itens, use `SUM` sobre `quantidade`.

## Layout sugerido

| Linha | Conteúdo | Distribuição |
|---|---|---|
| 1 | Faturamento, vendas, ticket médio e itens | Quatro cards iguais |
| 2 | Evolução mensal | Largura total |
| 3 | Categoria e Região | Duas colunas |
| 4 | Top 10 e Pagamento | Duas colunas |

Ajuste o layout e as fontes pela interface quando esses controles não estiverem disponíveis no schema MCP. Confira a legibilidade e a ausência de rolagem dentro dos cards.

## Validação

- Faturamento: R$ 2.318.923,25.
- Vendas distintas: 1.000.
- Ticket médio: R$ 2.318,92.
- Itens vendidos: 3.074.
- Série mensal: 21 pontos, de janeiro/2025 a setembro/2026, em ordem crescente.
- Categoria: 4 categorias, com receita conciliada ao KPI.
- Região: 5 regiões, com receita conciliada ao KPI.
- Produtos: ordenar pela soma do faturamento antes de limitar a dez.
- Pagamento: 5 formas e 1.000 vendas, com participações somando 100%.

Use as consultas em [04_validacao.sql](../sql/04_validacao.sql) como referência independente para os resultados.

## Limitações da interface MCP

A presença de `P1M` na configuração não comprova a agregação mensal: confira os pontos retornados. Um limite de dez linhas não comprova um Top 10 sem ordenação pela métrica.

O schema consultado não expõe tamanho de fonte de Big Number, tamanho de subtítulo ou configuração específica de BRL. Para barras, orientação e limite estão disponíveis, mas ordenação e rótulos podem depender da interface visual e da versão instalada.

## Capturas do dashboard

As imagens fornecidas pelo autor estão preservadas sem alterações:

- [Indicadores de vendas](imagens/dashboard-kpis.png).
- [Evolução e categorias](imagens/dashboard-evolucao-categorias.png).
- [Regiões, produtos e pagamentos](imagens/dashboard-regioes-produtos-pagamentos.png).

As capturas documentam a aparência dos visuais e não substituem a validação dos dados retornados, da granularidade temporal ou da ordenação dos produtos.

Não há export nativo importável do dashboard neste repositório. A configuração dos objetos no Superset faz parte da instalação.
