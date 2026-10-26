-- Consulta do dataset virtual. Não cria outro dataset automaticamente.
SELECT
    f.id_venda,
    d.data, d.dia, d.mes, d.nome_mes, d.ano, d.trimestre, d.dia_semana,
    p.produto, p.categoria,
    c.cliente,
    r.regiao,
    f.quantidade, f.valor_unitario, f.desconto_percentual, f.valor_total,
    f.forma_pagamento
FROM gold.fato_vendas AS f
INNER JOIN gold.dim_data AS d ON f.id_data = d.id_data
INNER JOIN gold.dim_produto AS p ON f.id_produto = p.id_produto
INNER JOIN gold.dim_cliente AS c ON f.id_cliente = c.id_cliente
INNER JOIN gold.dim_regiao AS r ON f.id_regiao = r.id_regiao;
