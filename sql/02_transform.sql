-- Carga completa da fato; dimens?es preservadas por chaves naturais.

INSERT INTO silver.vendas (
id_venda,
data_venda,
cliente,
produto,
categoria,
regiao,
quantidade,
valor_unitario,
desconto_percentual,
valor_total,
forma_pagamento,
ano,
mes,
dia
)
SELECT DISTINCT
id_venda,
data_venda,
TRIM(cliente),
TRIM(produto),
INITCAP(TRIM(categoria)),
INITCAP(TRIM(regiao)),
quantidade,
valor_unitario,
desconto_percentual,
valor_total,
INITCAP(TRIM(forma_pagamento)),
EXTRACT(YEAR FROM data_venda)::INTEGER,
EXTRACT(MONTH FROM data_venda)::INTEGER,
EXTRACT(DAY FROM data_venda)::INTEGER
FROM bronze.vendas
WHERE
id_venda IS NOT NULL
AND data_venda IS NOT NULL
AND quantidade > 0
AND valor_unitario >= 0
AND valor_total >= 0
AND desconto_percentual BETWEEN 0 AND 100;

INSERT INTO gold.dim_data (
data,
dia,
mes,
nome_mes,
ano,
trimestre,
dia_semana
)
SELECT DISTINCT
data_venda,
EXTRACT(DAY FROM data_venda)::INTEGER,
EXTRACT(MONTH FROM data_venda)::INTEGER,
CASE EXTRACT(MONTH FROM data_venda)
WHEN 1 THEN 'Janeiro'
WHEN 2 THEN 'Fevereiro'
WHEN 3 THEN 'Março'
WHEN 4 THEN 'Abril'
WHEN 5 THEN 'Maio'
WHEN 6 THEN 'Junho'
WHEN 7 THEN 'Julho'
WHEN 8 THEN 'Agosto'
WHEN 9 THEN 'Setembro'
WHEN 10 THEN 'Outubro'
WHEN 11 THEN 'Novembro'
WHEN 12 THEN 'Dezembro'
END,
EXTRACT(YEAR FROM data_venda)::INTEGER,
EXTRACT(QUARTER FROM data_venda)::INTEGER,
CASE EXTRACT(DOW FROM data_venda)
WHEN 0 THEN 'Domingo'
WHEN 1 THEN 'Segunda-feira'
WHEN 2 THEN 'Terça-feira'
WHEN 3 THEN 'Quarta-feira'
WHEN 4 THEN 'Quinta-feira'
WHEN 5 THEN 'Sexta-feira'
WHEN 6 THEN 'Sábado'
END
FROM silver.vendas
WHERE data_venda IS NOT NULL
ORDER BY data_venda
ON CONFLICT DO NOTHING;

INSERT INTO gold.dim_produto (
produto,
categoria
)
SELECT DISTINCT
produto,
categoria
FROM silver.vendas
WHERE
produto IS NOT NULL
AND categoria IS NOT NULL
ORDER BY
produto,
categoria
ON CONFLICT DO NOTHING;

INSERT INTO gold.dim_cliente (
cliente
)
SELECT DISTINCT
cliente
FROM silver.vendas
WHERE cliente IS NOT NULL
ON CONFLICT (cliente) DO NOTHING;

INSERT INTO gold.dim_regiao (
regiao
)
SELECT DISTINCT
regiao
FROM silver.vendas
WHERE regiao IS NOT NULL
ON CONFLICT (regiao) DO NOTHING;

INSERT INTO gold.fato_vendas (
id_venda,
id_data,
id_produto,
id_cliente,
id_regiao,
quantidade,
valor_unitario,
desconto_percentual,
valor_total,
forma_pagamento
)
SELECT
s.id_venda,
d.id_data,
p.id_produto,
c.id_cliente,
r.id_regiao,
s.quantidade,
s.valor_unitario,
s.desconto_percentual,
s.valor_total,
s.forma_pagamento
FROM silver.vendas AS s
INNER JOIN gold.dim_data AS d
ON s.data_venda = d.data
INNER JOIN gold.dim_produto AS p
ON s.produto = p.produto
AND s.categoria = p.categoria
INNER JOIN gold.dim_cliente AS c
ON s.cliente = c.cliente
INNER JOIN gold.dim_regiao AS r
ON s.regiao = r.regiao;
