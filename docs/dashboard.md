# Dashboard Executivo de Vendas

## Inventário da sessão original

Dashboard **10**, dataset **22**, banco **DW Vendas**, schema **gold**. IDs válidos apenas na instalação usada na conversa; redescubra em uma nova instalação. O inventário não é um export nativo importável.

| Gráfico | ID | Medida / dimensão |
|---|---:|---|
| KPI - Faturamento Total | 104 | `SUM(valor_total)` |
| KPI - Total de Vendas | 105 | `COUNT(DISTINCT id_venda)` |
| KPI - Ticket Médio | 106 | métrica salva `ticket_medio` |
| KPI - Itens Vendidos | 107 | `SUM(quantidade)` |
| Evolução Mensal do Faturamento | 108 | data mensal; `SUM(valor_total)` |
| Faturamento por Categoria | 110 | categoria; `SUM(valor_total)` |
| Faturamento por Região | 111 | regiao; `SUM(valor_total)` |
| Top 10 Produtos por Faturamento | 112 | produto; `SUM(valor_total)` |
| Vendas por Forma de Pagamento | 113 | forma_pagamento; `COUNT(DISTINCT id_venda)` |

`ticket_medio = SUM(valor_total) / COUNT(DISTINCT id_venda)`. Não substituir por `AVG(valor_total)`: a fórmula especifica explicitamente o denominador de vendas distintas.

## Fluxo de criação em uma instalação nova

1. Liste datasets e percorra páginas. Confirme o analítico, colunas e métricas.
2. Consulte o schema do tipo. Na versão observada: `big_number`, `xy` para barras/linhas e `pie` para pizza/Donut.
3. Use `generate_chart` com `save_chart: true`, um gráfico por vez.
4. Registre o ID retornado e use `get_chart_info` e `get_chart_data`.
5. Não recrie gráficos já existentes. Localize-os com `list_charts`.
6. Use `generate_dashboard` com os nove IDs confirmados e título **Dashboard Executivo de Vendas**.
7. Confira o dashboard com `get_dashboard_info`.

Exemplo conceitual de configuração para KPI (use o schema retornado na sua versão):

```json
{
  "chart_type": "big_number",
  "metric": {"name": "valor_total", "aggregate": "SUM"},
  "subheader": "Faturamento Total",
  "y_axis_format": ",.2f"
}
```

Para o Ticket Médio, utilize `{"name": "ticket_medio", "saved_metric": true}`. Para vendas distintas use `aggregate: "COUNT_DISTINCT"`; para itens use `aggregate: "SUM"` sobre `quantidade`.

## Layout editorial desejado

| Linha | Conteúdo | Distribuição sugerida |
|---|---|---|
| 1 | Os quatro KPIs, na ordem do inventário | Quatro cards de mesma largura |
| 2 | Evolução mensal | Largura total |
| 3 | Categoria e Região | Duas colunas |
| 4 | Top 10 e Formas de pagamento | Duas colunas |

O layout e a compactação dos KPIs não foram confirmados pelo MCP na sessão. Pela interface, escolha os menores tamanhos de número e subtítulo disponíveis na versão instalada; confira a ausência de rolagem no tamanho real dos cards. Não registre enums de fonte como se fossem aceitos pelo MCP quando não aparecem no schema.

## Critérios de aceite

| Visual | Verificação necessária |
|---|---|
| Faturamento | R$ 2.318.923,25; formato compacto opcional com unidade explícita |
| Total de vendas | 1.000 vendas distintas |
| Ticket médio | R$ 2.318,92, com fórmula salva correta |
| Itens | 3.074, soma de quantidade |
| Evolução mensal | 21 pontos de jan/2025 a set/2026, ordenados por data crescente |
| Categoria | 4 categorias, soma conciliada com o KPI, ordem decrescente se configurável |
| Região | 5 regiões, soma conciliada, horizontal se suportado |
| Top 10 | ORDER BY soma de faturamento DESC antes do LIMIT; empate com critério estável |
| Pagamento | 5 formas; 1.000 vendas no total; participação soma 100% |

Como existem dez produtos no CSV de referência, o gráfico com limite dez pode conter todos. Isso não prova que a configuração realiza um Top N correto para uma fonte com mais produtos. A validação de ranking deve verificar a ordenação antes do corte.

## Limitações observadas

O schema MCP consultado não expôs parâmetros de fonte, tamanho de subtitle, ocultação de Metric Name ou moeda BRL específica para Big Number. Expôs `subheader` e `y_axis_format`. Para barras, aceitou `orientation` e `row_limit`, mas não expôs ordenação da métrica ou rótulos nas barras.

A configuração mensal `P1M` foi salva no gráfico 108, porém a consulta MCP retornou 502 datas individuais na verificação realizada. Uma edição posterior foi observada no inventário, sem revalidação correspondente. Não declare o gráfico mensal aprovado com base apenas no parâmetro salvo.

O Donut 113 aceitou legenda e `label_type: key_value_percent`. Boleto retornou 212 de 1.000 vendas, equivalentes a 21,2%.

## Evidência para o portfólio

Capture o dashboard inteiro e detalhes dos KPIs após os ajustes manuais. Remova nomes de usuários, informações de conexão e segredos. Exporte o dashboard pelo Superset somente após revisão: o arquivo pode conter metadados de conexões. Não publique a URL `localhost` como demonstração pública.

Inclua no README a imagem real e um link de repositório somente depois de existir. Nenhuma captura ou export foi fabricado nesta preparação.
