# Diagnóstico técnico e plano de evolução

## Escopo da análise

Análise local dos arquivos do projeto e das evidências retornadas pelo MCP na conversa de 26/10/2026. Público: recrutadores e profissionais avaliando um portfólio de engenharia de dados.

**Esta análise não é resultado do LLM Council.** A execução do orquestrador foi tentada, mas terminou antes de iniciar os planejadores por ausência da configuração de agentes. Não há votação, avaliação independente ou `final-plan.md` produzido. O [briefing](../../llm-council/task-spec.json) está disponível para executar o conselho após configurar os agentes.

## Avaliação

O projeto possui uma narrativa técnica consistente: começa com dados rastreáveis, aplica transformações, constrói modelo dimensional e entrega indicadores de vendas. O diferencial de portfólio está em mostrar como a integração com IA é validada, inclusive quando a ferramenta não oferece o recurso desejado.

| Achado inicial | Implicação | Tratamento nesta organização |
|---|---|---|
| Quatro notebooks sem README | Difícil reproduzir sem acompanhar a aula | README, trilha manual e instalação completa |
| Credencial fixa no Compose | Arquivo inadequado para publicação | Variável obrigatória e `.env.example` vazio |
| Dependências não declaradas | Ambiente implícito | requirements separado do ambiente Superset |
| Outputs salvos nos notebooks | Ruído de revisão e possíveis detalhes locais | Outputs e contadores removidos |
| Cargas dependentes da ordem de células | Reexecução pode falhar por FKs | Pipeline SQL transacional com dimensões preservadas |
| Ausência de contrato automatizado | Erros podem chegar ao dashboard | Validação Decimal, testes de falhas e CI |
| Objetos disponíveis apenas na instância | Clone não reproduz dashboard sozinho | Inventário, SQL e roteiro; export continua pendente |
| Configuração MCP aceita sem resultado mensal validado | Possível falsa confirmação | Critérios explícitos de aceite por visual |
| Sem configuração LLM Council | Conselho não executa | Tentativa registrada e instruções de setup |

## Evidência local

O CSV fornecido possui 1.000 IDs únicos, 3.074 itens, receita de 2.318.923,25 e 21 meses entre 01/01/2025 e 30/09/2026. O ticket sem arredondamento é 2.318,92325. A fonte tem dez produtos, quatro categorias, cinco regiões e cinco formas de pagamento.

A validação do CSV confirma a fórmula de desconto por linha. A conferência de joins e a reconciliação entre camadas estão no pipeline e no job de integração, mas a execução completa do banco precisa ser distinguida dos testes offline.

## O que ainda exige evidência

1. Build e primeiro boot do Compose completo em Docker com acesso ao daemon.
2. Execução do pipeline duas vezes contra um PostgreSQL isolado.
3. Instalação nova do Superset com conexão, dataset e métrica cadastrados.
4. Agrupamento mensal do gráfico com 21 pontos efetivos e ordenação temporal.
5. Ranking dos produtos e ordenação dos gráficos de barras.
6. KPIs compactos e sem rolagem no layout de quatro colunas.
7. Captura real e export nativo revisado, sem dados de autenticação.
8. Execução efetiva do conselho após configurar agentes.

## Prioridades para revisão

**Antes de publicar:** revisar mudanças locais, executar os checks, registrar limites de validação, selecionar licença e inserir o link real do repositório no material de divulgação. A credencial anteriormente presente deve ser trocada caso tenha sido compartilhada ou reutilizada; esta preparação remove sua ocorrência do Compose, mas não altera usuários do banco.

**Para demonstrar o dashboard:** validar os 21 meses, concluir ordenação e fontes pela interface, capturar os resultados e declarar os ajustes manuais. Evitar a promessa de “dashboard 100% automatizado” enquanto essas etapas estiverem pendentes.

**Evolução de engenharia:** acrescentar agendamento, logs estruturados, cargas incrementais, segregação de permissões, migrações de schema e testes de contrato contra fontes com pedidos de múltiplos itens. Só acrescentar essas tecnologias quando houver um requisito demonstrável.

## Decisões de organização

- Preservar os notebooks na raiz, sem quebrar a trilha original.
- Manter o gerador e o CSV de referência para comparação determinística.
- Separar configuração do Codex de configurações locais reais.
- Oferecer stack isolada, sem executar mudanças na instância conectada.
- Utilizar consultas SQL explícitas para comparar a semântica esperada com o retorno do MCP.
- Registrar limitações como parte da análise técnica do projeto.

## Validação desta entrega

Consulte [validacao.md](validacao.md) para os checks efetivamente executados. A existência de um workflow no repositório não significa que ele já passou no GitHub.
