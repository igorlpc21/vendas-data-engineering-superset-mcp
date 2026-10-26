# Validação executada nesta preparação

Data: 26/10/2026. Validação local; sem alterações na instância Superset conectada.

| Verificação | Resultado |
|---|---|
| CSV com contrato, fórmulas e tipos | Aprovado: 1.000 vendas, 3.074 itens, 2.318.923,25, 21 meses |
| Teste do conjunto de referência | Aprovado |
| Rejeição de ID duplicado | Aprovado |
| Rejeição de faturamento incoerente | Aprovado |
| Estrutura dos quatro notebooks com nbformat | Aprovada; IDs de células normalizados |
| Outputs e contadores dos notebooks | Removidos para publicação |
| Sintaxe Python e links locais | Verificados por `scripts/check_project.py` |
| Varredura de atribuições literais sensíveis em Python/notebooks | Nenhuma atribuição não vazia encontrada para senha/token/secret; não substitui revisão manual |
| Compose original: `config --quiet` | Aprovado, exit code 0 |
| Compose completo: `config --quiet` | Aprovado, exit code 0 |
| Build e inicialização da imagem Superset/MCP | Não executados |
| Pipeline e reexecução em PostgreSQL | Aprovados em PostgreSQL 17 descartável no GitHub Actions; não executados no Docker local |
| Workflow GitHub Actions | Jobs `local-contract` e `warehouse-integration` aprovados na primeira publicação |
| Conexão de instalação nova com Codex | Documentada, não executada nesta preparação |
| Execução LLM Council | Falhou no início: configuração de agentes ausente |

O Docker CLI conseguiu validar os arquivos Compose sem precisar de containers. A leitura de `docker version` e `docker ps` encontrou restrição de acesso ao daemon e à configuração pessoal do Docker. Isso não é evidência de falha dos containers: eles não foram iniciados para teste.

As consultas anteriores da conversa forneceram os IDs e valores do Superset. Esta preparação não revalidou renderização, dimensões dos cards ou o gráfico temporal após edições manuais. Não houve export nativo, captura de tela ou publicação no LinkedIn. Posteriormente, o repositório público foi criado e os dois jobs de CI passaram: [execução de validação](https://github.com/igorlpc21/vendas-data-engineering-superset-mcp/actions/runs/40411258044).

As dependências Python de notebooks usam intervalos compatíveis, não um lockfile completo. A imagem Superset é fixada em 6.1.0, mas as dependências transitivas do extra MCP ainda são resolvidas no build. Um build validado e travado por digest/lock é uma evolução para reprodução mais estrita.
