# Instalação e reprodução

## 1. Escolha o ambiente

Há duas opções que não devem ser confundidas:

| Opção | Compose | PostgreSQL no host | Superset | MCP |
|---|---|---:|---:|---:|
| Aula original | `docker-compose.yml` | 5434 | instalação existente | instalação existente |
| Laboratório completo isolado | `docker-compose.demo.yml`, projeto `vendas-demo` | 15434 | 18888 | 15008 |

O laboratório isolado não reutiliza o dataset 22 ou o dashboard 10 da sessão original. Os IDs surgirão na nova instalação. Não copie IDs sem redescobrir os objetos.

## 2. Instale dependências do projeto

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
Copy-Item .env.example .env
```

Preencha `POSTGRES_PASSWORD`, `SUPERSET_SECRET_KEY` e `SUPERSET_ADMIN_PASSWORD`. Não deixe senhas em notebooks nem no Git. O script lê pares simples `CHAVE=valor`, com aspas externas opcionais; não use interpolação `${VAR}` no `.env`.

Se o Compose original já usa um volume existente, a variável `POSTGRES_PASSWORD` deve corresponder à senha atual desse banco. Alterar o `.env` não troca a senha de um usuário já criado. Não remova volumes para resolver autenticação.

No macOS/Linux, os mesmos comandos Python usam `.venv/bin/python` em vez de `.venv\Scripts\python.exe`.

## 3. Valide a fonte

O CSV já acompanha o projeto. Sua regeneração é opcional:

```powershell
.\.venv\Scripts\python.exe gerar_dados.py
.\.venv\Scripts\python.exe scripts/validate_data.py
```

A validação usa `Decimal` e exige IDs únicos, campos preenchidos, datas válidas, quantidades positivas e igualdade exata da fórmula de desconto em centavos. O contrato de referência também está nos testes.

## 4. Suba o laboratório completo

```powershell
docker compose -p vendas-demo -f docker-compose.demo.yml config --quiet
docker compose -p vendas-demo -f docker-compose.demo.yml up -d --build
docker compose -p vendas-demo -f docker-compose.demo.yml ps -a
docker compose -p vendas-demo -f docker-compose.demo.yml logs --tail 80 superset-init
```

O serviço `superset-init` aplica as migrações, cria o administrador e sincroniza as permissões. A aplicação web e o processo MCP compartilham a mesma configuração e o mesmo banco de metadados `superset`, separado do banco analítico `db_vendas` no PostgreSQL.

Mantenha `POSTGRES_DB=db_vendas` no laboratório: o inicializador cria `superset` separadamente para os metadados. Não use `superset` como nome do banco analítico.

A imagem deriva de `apache/superset:6.1.0` e instala o extra oficial `fastmcp` e o driver PostgreSQL. O uso de extras da própria versão evita adivinhar dependências MCP. Base: [pyproject da release 6.1.0](https://github.com/apache/superset/blob/6.1.0/pyproject.toml) e [Dockerfile da release](https://github.com/apache/superset/blob/6.1.0/Dockerfile).

Se a criação do administrador indicar usuário já existente, não remova o volume: execute `docker compose -p vendas-demo -f docker-compose.demo.yml run --rm --no-deps superset-init superset init` e inicie apenas `superset` e `superset-mcp` com `up -d --no-deps`. O inicializador foi projetado para o primeiro boot; não ignora falhas automaticamente.

Portas publicadas são restritas a `127.0.0.1`. O modo MCP sem JWT é apenas para laboratório local. Não exponha essa stack na internet.

## 5. Execute a carga

```powershell
.\.venv\Scripts\python.exe scripts/run_pipeline.py --port 15434 --full-refresh
```

São criados os schemas e as tabelas do laboratório; depois a carga substitui Bronze, Silver e fato Gold dentro de uma única transação. As dimensões são preservadas por chaves naturais, com `ON CONFLICT DO NOTHING`. Falha de reconciliação provoca rollback.

A carga compara linhas, vendas distintas, receita e quantidade entre CSV, Bronze, Silver e fato; também verifica se os JOINs da consulta analítica preservam linhas e faturamento. Em uma segunda execução, os resultados devem permanecer iguais. Não é um sistema incremental e não mantém histórico de alterações dimensionais.

## 6. Conecte o DW ao Superset

Abra `http://localhost:18888` e entre com o usuário e a senha definidos no `.env`. Em **Settings → Database Connections**, adicione uma conexão PostgreSQL chamada **DW Vendas**:

```text
host: postgres
port: 5432
database: db_vendas
username: valor de POSTGRES_USER
password: valor de POSTGRES_PASSWORD
```

Dentro da rede Docker, `postgres:5432` aponta para o DW. No Python executado no Windows, o endereço é `127.0.0.1:15434`. A URL do banco, se usada, exige senha codificada para URL; prefira os campos do formulário.

No SQL Lab, execute [03_dataset_analitico.sql](../sql/03_dataset_analitico.sql), confira as colunas e salve uma única vez como **Dataset Analítico de Vendas** no schema `gold`. Se o dataset já existir, reutilize-o. Cadastre `ticket_medio` na aba Metrics com expressão `SUM(valor_total) / COUNT(DISTINCT id_venda)`, nome de exibição **Ticket Médio** e descrição **Valor médio faturado por venda**.

Essa etapa é manual porque o MCP observado não ofereceu ferramenta explícita para adicionar métricas a datasets. A instalação isolada não recebe automaticamente os objetos da sessão original.

## 7. Conecte o Codex

Continue em [MCP no Codex](mcp-codex.md), depois execute o [roteiro do dashboard](dashboard.md).

## 8. Alternativa: trilha dos notebooks

Para o PostgreSQL original: `docker compose up -d postgres`. Inicie Jupyter na raiz com `.\.venv\Scripts\python.exe -m jupyterlab`. Execute os notebooks 01 a 04 em ordem. As células de conexão usam porta 5434 e pedem a senha com `getpass`; ajuste os campos se usar o laboratório isolado.

Os notebooks foram preservados como material de aula. Algumas células limpam dimensões e não devem ser repetidas fora de ordem quando já existem fatos com chaves estrangeiras. Para carga repetível, prefira `run_pipeline.py`, que carrega a fato e preserva as dimensões na mesma transação.

## 9. Parar sem apagar dados

```powershell
docker compose -p vendas-demo -f docker-compose.demo.yml stop
```

O projeto não orienta remoção automática de volumes. O Compose foi validado estruturalmente, mas o build e o boot completo devem ser verificados no seu Docker antes de declarar reprodução ponta a ponta aprovada.
