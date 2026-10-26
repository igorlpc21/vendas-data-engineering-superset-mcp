-- Estruturas extra?das dos notebooks did?ticos.

CREATE SCHEMA IF NOT EXISTS bronze;

CREATE SCHEMA IF NOT EXISTS silver;

CREATE SCHEMA IF NOT EXISTS gold;

CREATE TABLE IF NOT EXISTS bronze.vendas (
id_venda INTEGER,
data_venda DATE,
cliente TEXT,
produto TEXT,
categoria TEXT,
regiao TEXT,
quantidade INTEGER,
valor_unitario NUMERIC(12,2),
desconto_percentual INTEGER,
valor_total NUMERIC(12,2),
forma_pagamento TEXT
);

CREATE TABLE IF NOT EXISTS silver.vendas (
id_venda INTEGER,
data_venda DATE,
cliente TEXT,
produto TEXT,
categoria TEXT,
regiao TEXT,
quantidade INTEGER,
valor_unitario NUMERIC(12,2),
desconto_percentual INTEGER,
valor_total NUMERIC(12,2),
forma_pagamento TEXT,
ano INTEGER,
mes INTEGER,
dia INTEGER
);

CREATE TABLE IF NOT EXISTS gold.dim_data (
id_data SERIAL PRIMARY KEY,
data DATE NOT NULL UNIQUE,
dia INTEGER NOT NULL,
mes INTEGER NOT NULL,
nome_mes TEXT NOT NULL,
ano INTEGER NOT NULL,
trimestre INTEGER NOT NULL,
dia_semana TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS gold.dim_produto (
id_produto SERIAL PRIMARY KEY,
produto TEXT NOT NULL,
categoria TEXT NOT NULL,
UNIQUE (produto, categoria)
);

CREATE TABLE IF NOT EXISTS gold.dim_cliente (
id_cliente SERIAL PRIMARY KEY,
cliente TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS gold.dim_regiao (
id_regiao SERIAL PRIMARY KEY,
regiao TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS gold.fato_vendas (
id_venda INTEGER PRIMARY KEY,
id_data INTEGER NOT NULL,
id_produto INTEGER NOT NULL,
id_cliente INTEGER NOT NULL,
id_regiao INTEGER NOT NULL,
quantidade INTEGER NOT NULL,
valor_unitario NUMERIC(12,2) NOT NULL,
desconto_percentual INTEGER NOT NULL,
valor_total NUMERIC(12,2) NOT NULL,
forma_pagamento TEXT NOT NULL,
CONSTRAINT fk_data
FOREIGN KEY (id_data)
REFERENCES gold.dim_data(id_data),
CONSTRAINT fk_produto
FOREIGN KEY (id_produto)
REFERENCES gold.dim_produto(id_produto),
CONSTRAINT fk_cliente
FOREIGN KEY (id_cliente)
REFERENCES gold.dim_cliente(id_cliente),
CONSTRAINT fk_regiao
FOREIGN KEY (id_regiao)
REFERENCES gold.dim_regiao(id_regiao)
);
