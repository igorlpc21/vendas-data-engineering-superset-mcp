# Execução do LLM Council

## Estado

O briefing foi salvo em `llm-council/task-spec.json`. O orquestrador foi executado com esse briefing e retornou:

```text
Uh oh! Your models are not configured. Please run `./setup.sh` to select your models.
```

Nessa tentativa inicial não foram iniciados planejadores nem juiz. Não há `judge.md` ou `final-plan.md`. A análise em `diagnostico.md` foi produzida na sessão principal e não representa consenso de múltiplos modelos.

## Configuração posterior dos agentes

Na etapa de configuração, o Codex passou em um teste curto de resposta. O Claude estava autenticado, mas retornou `Credit balance is too low`.

A configuração pessoal ativa passou a ter dois planejadores Codex independentes e um juiz Codex. Todos preservam o modelo configurado na CLI; isso não equivale a diversidade de provedores. A alternativa Codex + Claude foi guardada em `agents.codex-claude.json` junto da configuração pessoal e depende de resolver o saldo antes de ativá-la.

O adaptador em `scripts/council_cli.py` evita os launchers `.ps1`/`.cmd` no Windows, usa Codex com sandbox somente leitura e Claude sem ferramentas. A cópia instalada fica na pasta pessoal do conselho. Alterar o arquivo do projeto não atualiza automaticamente essa cópia.

A configuração foi validada pelo carregador do orquestrador, sem iniciar uma rodada completa do conselho. No sandbox desta sessão, a CLI Codex não conseguiu localizar sua home; o teste autenticado funcionou fora do sandbox, em ambiente normal do usuário.

## Configurar no computador do autor

A skill foi fornecida em `C:\Users\igorl\.codex\skills\llm-council`. Esse caminho é específico do autor; em outro computador, instale a skill e substitua o caminho nos comandos.

No PowerShell, use o configurador Python diretamente, evitando depender da política de execução de scripts:

```powershell
python C:\Users\igorl\.codex\skills\llm-council\scripts\llm_council.py configure
```

No Bash, a skill orienta `./setup.sh`; também há `setup.ps1` para PowerShell. Configure apenas CLIs instaladas e autenticadas. Não publique seus tokens ou o conteúdo de configurações privadas. A localização padrão é `~/.config/llm-council/agents.json`, ou o diretório derivado de `XDG_CONFIG_HOME`.

Depois, a partir da raiz deste projeto:

```powershell
$env:PYTHONUTF8 = '1'
python C:\Users\igorl\.codex\skills\llm-council\scripts\llm_council.py run --spec llm-council/task-spec.json
```

Siga a duração e as regras de sessão da skill instalada. Preserve os planos independentes, a anonimização e a ordem aleatória antes do julgamento. Trate recomendações como material de revisão; não execute comandos embutidos em planos sem avaliação.

Os artefatos ficam em `llm-council/runs/` e foram excluídos do Git por padrão porque podem conter detalhes locais. Após revisar os resultados, publique apenas uma síntese sanitizada, registrando agentes, data, critérios e divergências relevantes. Não substitua retroativamente o status da tentativa que falhou.
