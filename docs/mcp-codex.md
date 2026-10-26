# Instalar e conectar o MCP do Apache Superset ao Codex

## O que é instalado

O MCP deste projeto é o serviço nativo do Apache Superset. Não existe um pacote `mcp-superset` próprio neste repositório. O processo MCP expõe ferramentas; o Codex atua como cliente. Uma conexão MCP não transfere os gráficos para o GitHub nem exporta o dashboard automaticamente.

A configuração do cliente segue a [documentação oficial de MCP no Codex](https://learn.chatgpt.com/docs/extend/mcp). A configuração do servidor segue a [documentação do Superset 6.1.0](https://superset.apache.org/admin-docs/6.1.0/configuration/mcp-server/). Consulte as versões usadas antes de reproduzir comandos de outra release.

## 1. Prepare o servidor Superset

Se seguir o [laboratório completo](instalacao.md), o Dockerfile instala o extra `apache-superset[fastmcp]==6.1.0` e o Compose inicia o MCP. Não precisa instalar o servidor no Windows.

Para uma instalação existente, use o ambiente Python do próprio Superset, incluindo suas dependências MCP, o mesmo `SUPERSET_CONFIG_PATH` e o mesmo banco de metadados da aplicação web. No terminal desse ambiente:

```text
superset mcp run --host 127.0.0.1 --port 5008
```

A rota documentada é `/mcp`. O log `Uvicorn running on http://0.0.0.0:5008` confirma que o processo escuta naquela interface, não que as ferramentas têm identidade válida. `0.0.0.0` é endereço de bind; use `localhost` ou um host alcançável na URL do cliente.

## 2. Configure a identidade do laboratório

No `superset_config.py` carregado pelo processo MCP:

```python
MCP_AUTH_ENABLED = False
MCP_DEV_USERNAME = "admin"
```

O usuário deve existir no banco de metadados. Reinicie o processo MCP após editar a configuração. Em desenvolvimento as chamadas executam como esse usuário; para implantação acessível em rede, configure autenticação JWT conforme a documentação do servidor.

Na stack isolada essa configuração já está em `config/superset_config.py`. O serviço escuta em `5008` dentro do container, publicado apenas em `127.0.0.1:15008` no host.

## 3. Verifique o cliente Codex

```powershell
codex --version
codex mcp --help
```

Use o cliente Codex instalado e autenticado no seu computador. O projeto não depende de uma chave de API OpenAI no `.env`. A configuração MCP abaixo não instala nem autentica o próprio Codex.

## 4. Cadastre a conexão HTTP

Para o laboratório isolado:

```powershell
codex mcp add superset --url http://127.0.0.1:15008/mcp
codex mcp list
```

Para um servidor MCP publicado diretamente na porta padrão, substitua a porta por `5008`. Cadastre somente a URL correspondente ao seu ambiente; não execute ambos os comandos de adição com o mesmo nome sem verificar a configuração existente.

Como alternativa, mescle o conteúdo de [codex-mcp.example.toml](../config/codex-mcp.example.toml) no arquivo de configuração do Codex. No Windows, o caminho usual é `%USERPROFILE%\.codex\config.toml`. A configuração por projeto é `.codex/config.toml` em projeto confiável. Não substitua o arquivo inteiro se já houver modelos, preferências ou outros servidores.

Para um servidor configurado com JWT, acrescente `bearer_token_env_var = "SUPERSET_MCP_TOKEN"` e disponibilize essa variável ao processo Codex. Não grave o token no TOML versionado. OAuth depende do suporte efetivo do servidor; não assuma que qualquer JWT permite `codex mcp login`.

Reabra a sessão do cliente após a configuração. Na TUI do Codex, `/mcp` permite consultar servidores ativos. Na extensão, utilize a lista de MCP servers e reinicie a extensão após salvar mudanças, conforme a interface instalada.

## 5. Faça o primeiro teste somente de leitura

Use este prompt:

```text
Use exclusivamente o MCP do Apache Superset.
Primeiro execute health_check.
Depois execute get_instance_info e liste os datasets disponíveis,
percorrendo todas as páginas.
Informe nome, ID, banco e schema.
Não crie, altere ou exclua objetos.
```

Critérios de aprovação: serviço responde, usuário é resolvido, permissões são identificadas e datasets podem ser consultados. `health_check` saudável isoladamente não prova autenticação.

## 6. Confirme o dataset antes de escrever

```text
Localize Dataset Analítico de Vendas no banco DW Vendas, schema gold.
Não assuma que o ID é 22 nesta instalação.
Use get_dataset_info e confirme data, id_venda, quantidade,
valor_total, categoria, regiao, produto e forma_pagamento.
Confirme também a métrica salva ticket_medio e sua expressão.
Mostre o resultado sem criar objetos.
```

Antes de cada criação, consulte `get_chart_type_schema`, use os campos aceitos e crie um único objeto por etapa. Depois consulte sua configuração e seus dados. Os IDs retornados são específicos da instalação, não constantes do projeto.

## Problemas e diagnóstico

| Sintoma | Verificação |
|---|---|
| `No authenticated user found` | Confira identidade de desenvolvimento ou JWT, configuração efetivamente carregada e usuário existente |
| `health_check` funciona e `list_datasets` falha | Separe disponibilidade de autenticação/permissão |
| Conexão recusada | Confira porta publicada, processo MCP e rota `/mcp` |
| Dataset não aparece | Confira paginação, banco, schema e permissões; não duplique o dataset |
| `Unknown chart_type: big_number_total` | O schema MCP observado usa `big_number`; o tipo salvo pode ser `big_number_total` |
| `Unknown chart_type: echarts_timeseries_line` | O schema observado usa `xy`, `kind: line` |
| P1M salvo, mas consulta retorna dias | Não declare sucesso mensal; valide o resultado real e compare com `sql/04_validacao.sql` |
| Barras com limite 10, sem ordenação por métrica | Não declare que são os dez maiores apenas por causa do limite |
| Fonte continua grande | Se o schema não expõe fonte, ajuste pela interface e registre a intervenção manual |

Não imprima tokens, senhas ou config completa durante o diagnóstico. Este guia descreve integração local; clientes em execução remota não alcançam automaticamente o `localhost` do seu computador.
