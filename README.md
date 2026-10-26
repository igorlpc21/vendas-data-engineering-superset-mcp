# Engenharia de dados de vendas com PostgreSQL e Apache Superset

Pipeline de vendas com dados sintéticos, camadas Bronze/Silver/Gold, modelo dimensional e dashboard no Apache Superset. Inclui integração opcional com o Codex por meio do MCP nativo do Superset.

## Arquitetura

```text
CSV → Bronze → Silver → Gold → Dataset analítico → Dashboard Superset
                                           ↑
                                   Codex via MCP
```

As camadas são schemas do PostgreSQL. Os notebooks apresentam a trilha didática; os scripts permitem executar e validar a carga de forma automatizada.

## Dados de referência

| Indicador | Valor |
|---|---:|
| Vendas distintas | 1.000 |
| Faturamento após desconto | R$ 2.318.923,25 |
| Ticket médio | R$ 2.318,92 |
| Itens vendidos | 3.074 |
| Período | Jan/2025 a Set/2026 |

Os dados são sintéticos. Cada linha representa uma venda de um produto, com sua quantidade.

## Instalação

Pré-requisitos: Python 3.11 ou 3.12 e Docker com Compose. O Superset utiliza ambiente separado nos containers.

No PowerShell, a partir da raiz do projeto:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
Copy-Item .env.example .env
```

Preencha no `.env`: `POSTGRES_PASSWORD`, `SUPERSET_SECRET_KEY` e `SUPERSET_ADMIN_PASSWORD`.

```powershell
docker compose -p vendas-demo -f docker-compose.demo.yml up -d --build
.\.venv\Scripts\python.exe scripts/run_pipeline.py --port 15434 --full-refresh
```

O Superset fica disponível em `http://localhost:18888` e o MCP em `http://127.0.0.1:15008/mcp`.

`--full-refresh` substitui os dados de Bronze, Silver e fato Gold no banco configurado. Utilize somente no ambiente de laboratório.

Consulte o [passo a passo completo de instalação](docs/instalacao.md) para configurar a conexão, o dataset analítico e a métrica de ticket médio. Os objetos do Superset são configurados separadamente; não há export importável do dashboard neste repositório.

## Validação

```powershell
.\.venv\Scripts\python.exe scripts/validate_data.py
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe scripts/check_project.py
```

O GitHub Actions verifica o contrato de dados, os notebooks e os arquivos Compose, além de executar a carga duas vezes em PostgreSQL 17 descartável. O build completo da aplicação Superset/MCP ainda precisa ser validado.

## Estrutura

```text
01_analise_exploratoria.ipynb  Análise da fonte
02_camada_bronze.ipynb        Ingestão
03_camada_silver.ipynb        Transformação
04_camada_gold.ipynb          Modelo dimensional
gerar_dados.py               Geração da base sintética
dados/                       CSV de referência
scripts/                     Carga e validação
sql/                         Estruturas, transformações e consultas
config/                      Superset e exemplo MCP
docs/                        Documentação técnica
tests/                       Testes do contrato de dados
.github/workflows/           Integração contínua
```

`docker-compose.yml` mantém a opção de PostgreSQL isolado da trilha dos notebooks, na porta 5434. `docker-compose.demo.yml` fornece o laboratório completo em portas separadas.

## Documentação

- [Instalação](docs/instalacao.md)
- [Arquitetura e contrato de dados](docs/arquitetura.md)
- [Dashboard e métricas](docs/dashboard.md)
- [MCP do Superset no Codex](docs/mcp-codex.md)
- [Contribuição](CONTRIBUTING.md)

A carga é full refresh de laboratório. Não implementa carga incremental, histórico SCD ou implantação de produção.
