# Do CSV ao dashboard: engenharia de dados de vendas com PostgreSQL, Superset e Codex via MCP

Um dashboard pode exibir números corretos e ainda contar uma história errada.

Durante a construção de um projeto de vendas, encontrei um exemplo concreto: o gráfico tinha a granularidade mensal salva na configuração, mas a consulta de validação retornava 502 datas individuais. O resultado esperado era uma série com 21 meses.

Esse episódio mudou o foco do projeto. Além de construir o pipeline e os gráficos, passei a tratar a validação de cada etapa como parte central da entrega.

## O projeto

Construí um laboratório de engenharia de dados com uma base sintética de mil vendas. A proposta foi acompanhar todo o caminho: geração da fonte, análise exploratória, persistência no PostgreSQL, transformação em camadas, modelagem dimensional e visualização no Apache Superset.

A integração com o Codex foi realizada pelo MCP nativo do Superset. Assim, o assistente pôde consultar datasets, inspecionar schemas e criar gráficos por meio de ferramentas disponibilizadas pelo servidor.

Os dados são simulados. Os indicadores não representam receita de uma empresa real; servem para testar consistência, modelagem e visualização.

## 1. Primeiro, uma fonte que pode ser conferida

O gerador utiliza uma semente fixa e produz vendas entre janeiro de 2025 e setembro de 2026. Cada linha representa uma venda com um único produto e sua quantidade.

Essa definição de grão é importante. Se o cenário passasse a representar pedidos com vários itens, seria necessário rever as chaves e separar a identificação do pedido da identificação de cada linha.

Na base de referência, os resultados são:

- 1.000 vendas distintas;
- R$ 2.318.923,25 de faturamento após desconto;
- R$ 2.318,92 de ticket médio;
- 3.074 itens vendidos;
- 21 meses com dados.

A fórmula do valor de cada venda é quantidade multiplicada pelo preço unitário, com aplicação do desconto. Uma validação decimal confere essa igualdade em centavos, além de verificar campos obrigatórios, IDs duplicados e domínios numéricos.

Não há modelagem de devoluções, impostos, frete, cancelamentos ou margem. Declarar esses limites evita atribuir ao indicador um significado que a fonte não sustenta.

## 2. Bronze, Silver e Gold com responsabilidades claras

No laboratório, as camadas são schemas do PostgreSQL.

A Bronze recebe os dados tipados da fonte. A Silver padroniza textos, verifica condições de domínio e acrescenta atributos temporais. A Gold organiza uma fato de vendas associada às dimensões de data, produto, cliente e região.

O dataset analítico do Superset reúne esses atributos por JOINs. Essa consulta também precisa ser validada: relacionamentos incorretos podem multiplicar vendas e inflar o faturamento sem produzir um erro de execução.

Para tornar o projeto reproduzível, preservei os notebooks como material didático e acrescentei uma trilha de execução por scripts e SQL. A carga completa usa uma transação e verifica a reconciliação entre a fonte e as camadas. Se houver divergência, a carga deve falhar em vez de aceitar um resultado parcial.

É uma implementação de laboratório com full refresh. Não a apresento como uma plataforma incremental pronta para produção.

## 3. Métricas antes da estética

O dashboard reúne quatro KPIs e análises de evolução temporal, categoria, região, produto e pagamento.

Uma decisão foi manter explícita a fórmula do ticket médio:

```sql
SUM(valor_total) / COUNT(DISTINCT id_venda)
```

Embora uma média simples possa coincidir com esse resultado no grão atual, registrar o numerador e o denominador evita depender dessa coincidência. A semântica da métrica precisa acompanhar a evolução do modelo.

Também separei quantidade de vendas de quantidade de itens. A primeira utiliza vendas distintas; a segunda utiliza a soma da quantidade comercializada.

## 4. Como o MCP entrou no fluxo

O MCP fornece uma interface de ferramentas entre o cliente e o Superset. A documentação do [serviço nativo](https://superset.apache.org/admin-docs/6.1.0/configuration/mcp-server/) apresenta sua execução como processo separado e a rota HTTP de conexão.

No cliente, segui a [documentação oficial do Codex para MCP](https://learn.chatgpt.com/docs/extend/mcp). O repositório inclui um exemplo de configuração e um roteiro para testar a conexão antes de criar objetos.

O fluxo adotado foi simples: descobrir, inspecionar, criar um objeto e validar o retorno. Em uma nova instalação, os IDs precisam ser descobertos novamente; os identificadores da minha sessão não são constantes reutilizáveis.

Outro aprendizado foi separar disponibilidade de autenticação. O servidor pode responder ao health check e ainda não conseguir listar datasets porque nenhuma identidade válida foi resolvida.

## 5. O limite de uma ferramenta também faz parte do resultado

Na versão consultada, o schema de Big Number não expôs opções para reduzir o tamanho do número ou do subtítulo. Não adiantava pedir “Small” repetidamente: aquele parâmetro não estava disponível pela interface MCP utilizada.

Nos gráficos de barras, havia suporte a orientação e limite de resultados, mas não à ordenação pela métrica no schema observado. Aplicar limite dez, por si só, não comprova um Top 10 por faturamento. É preciso ordenar antes de limitar.

Na série temporal, o parâmetro mensal salvo não foi suficiente para comprovar o agrupamento real. A consulta retornou datas diárias, então registrei a divergência e deixei a validação mensal pendente.

Esses casos reforçaram uma prática que pretendo manter em projetos com agentes: distinguir configuração aceita, cálculo conferido e visualização validada. Um retorno de sucesso da ferramenta não substitui os três.

## 6. O que foi preparado para reprodução

O projeto passou a incluir configuração por variáveis de ambiente, requisitos do ambiente Python, SQL separado, validação do CSV, testes de contrato, workflow de CI e um laboratório Docker isolado para PostgreSQL, Superset e MCP.

A execução completa desse laboratório e dos jobs no ambiente de destino ainda precisa ser confirmada. Também permanecem ajustes visuais pela interface do Superset e a inclusão de uma captura real do dashboard. Prefiro registrar essas pendências a apresentar automação total sem evidência.

A revisão por LLM Council foi preparada, mas não executou porque os agentes locais ainda precisam ser configurados. Portanto, a análise publicada aqui não é apresentada como consenso de múltiplos modelos.

## O aprendizado que levo

Integrar um assistente ao BI amplia o que consigo explorar e automatizar. A responsabilidade técnica continua incluindo a definição do grão, a reconciliação, a semântica das métricas e a verificação do resultado.

O valor desse projeto, para mim, está em tornar esse processo visível: da fonte ao indicador, com decisões, testes e limitações documentados.

**Repositório:** [vendas-data-engineering-superset-mcp](https://github.com/igorlpc21/vendas-data-engineering-superset-mcp).

Qual validação você considera indispensável antes de confiar em um dashboard criado com apoio de agentes?

---

Nota editorial: antes de postar, revisar a voz do autor e anexar uma captura real após os ajustes visuais. Este arquivo é um rascunho publicável; nada foi enviado ao LinkedIn.
