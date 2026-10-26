-- Consultas somente de leitura. Execute contra o banco analítico.
SELECT COUNT(*) AS linhas, COUNT(DISTINCT id_venda) AS vendas,
       SUM(valor_total) AS faturamento,
       SUM(valor_total) / NULLIF(COUNT(DISTINCT id_venda), 0) AS ticket_medio,
       SUM(quantidade) AS itens
FROM gold.fato_vendas;

SELECT DATE_TRUNC('month', d.data)::date AS mes,
       SUM(f.valor_total) AS faturamento
FROM gold.fato_vendas AS f
INNER JOIN gold.dim_data AS d ON d.id_data = f.id_data
GROUP BY DATE_TRUNC('month', d.data)::date
ORDER BY mes ASC;

SELECT p.produto, SUM(f.valor_total) AS faturamento
FROM gold.fato_vendas AS f
INNER JOIN gold.dim_produto AS p ON p.id_produto = f.id_produto
GROUP BY p.produto
ORDER BY faturamento DESC, p.produto ASC
LIMIT 10;
