# Post de divulgação

Construí um projeto de engenharia de dados que conecta uma base sintética de vendas a um dashboard no Apache Superset, com apoio do Codex via MCP.

O caminho completo:

• CSV determinístico e análise exploratória;
• PostgreSQL com camadas Bronze, Silver e Gold;
• modelo dimensional com fato e quatro dimensões;
• KPIs de faturamento, vendas, ticket médio e itens;
• ferramentas MCP para descobrir datasets e criar visualizações;
• scripts de validação, testes e documentação de reprodução.

O aprendizado mais útil apareceu na validação: ter `P1M` salvo no gráfico não comprovou que o retorno estava agregado por mês. E limitar uma consulta a dez produtos não comprovou um Top 10 sem ordenação pela métrica.

Documentei esses limites porque considero essa distinção parte do trabalho de engenharia: configuração aceita e resultado validado precisam ser conferidos separadamente.

A base contém 1.000 vendas simuladas; não são dados de uma operação real. O repositório também registra os ajustes manuais e as verificações de ambiente que ainda precisam ser concluídos.

Código e passo a passo: https://github.com/igorlpc21/vendas-data-engineering-superset-mcp
Artigo completo: inserir o link após publicar o artigo.

#EngenhariaDeDados #PostgreSQL #ApacheSuperset #BusinessIntelligence #MCP #Python

---

Antes de postar: substituir o marcador do artigo, anexar imagem real e revisar o status das pendências. Nenhuma publicação foi realizada no LinkedIn.
