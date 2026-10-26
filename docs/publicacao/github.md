# Preparar e publicar no GitHub

## Nome e apresentação

Nome sugerido: **vendas-data-engineering-superset-mcp**.

Descrição sugerida: **Pipeline de vendas com PostgreSQL, Bronze/Silver/Gold, modelo dimensional e dashboard no Apache Superset integrado ao Codex via MCP.**

Tópicos sugeridos: `data-engineering`, `postgresql`, `apache-superset`, `business-intelligence`, `mcp`, `codex`, `python`, `portfolio`.

## 1. Validar a versão local

```powershell
.\.venv\Scripts\python.exe scripts/validate_data.py
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe scripts/check_project.py
```

Valide o Compose com `.env` preenchido e execute a integração em ambiente isolado conforme o guia de instalação. A CI inclui teste com PostgreSQL descartável, mas só será possível declarar o job aprovado após a execução no GitHub.

## 2. Revisar o conteúdo público

- Confirmar que `.env`, `.venv`, configs pessoais, logs e exports não entrarão no commit.
- Revisar as quatro células de conexão e manter outputs limpos.
- Capturar uma imagem real do dashboard após ajustes; não utilizar uma ilustração como evidência de funcionamento.
- Decidir a licença do código e confirmar autorização de materiais eventualmente adicionados. Nenhuma licença foi escolhida em nome do autor.
- Revisar as pendências de [diagnóstico](../analise/diagnostico.md).

O CSV é sintético e deve ser apresentado como tal. O projeto não contém exports importáveis do dashboard, nem um link público de demonstração.

## 3. Inicializar o Git

Na inspeção inicial a pasta não era um repositório Git. Depois da sua revisão:

```powershell
git init -b main
git status --short
git add README.md CONTRIBUTING.md .gitignore .gitattributes .env.example requirements.txt
git add gerar_dados.py dados scripts sql config docs tests .github llm-council/task-spec.json
git add docker-compose.yml docker-compose.demo.yml
git add 01_analise_exploratoria.ipynb 02_camada_bronze.ipynb 03_camada_silver.ipynb 04_camada_gold.ipynb
git diff --cached --stat
git diff --cached --check
```

Revise `git diff --cached` localmente antes do commit. Não copie possíveis segredos para uma conversa ou screenshot.

```powershell
git commit -m "Organiza pipeline de vendas, laboratório Superset MCP e documentação"
```

## 4. Criar e enviar o repositório

Crie um repositório vazio no GitHub com o nome escolhido. Não acrescente README remoto se já houver commit local. Copie a URL real apresentada pelo GitHub:

```powershell
git remote add origin <URL_REAL_DO_REPOSITORIO>
git push -u origin main
```

`<URL_REAL_DO_REPOSITORIO>` é um marcador a substituir, não um comando pronto para colar. Confira os jobs na aba Actions. Se algum falhar, corrija e rode novamente antes de mencionar CI aprovada.

## 5. Publicar o artigo

O repositório foi publicado em [igorlpc21/vendas-data-engineering-superset-mcp](https://github.com/igorlpc21/vendas-data-engineering-superset-mcp). Revise [o artigo](artigo-linkedin.md) e anexe a captura validada antes de publicar o artigo e o [post](post-linkedin.md). Nada foi publicado no LinkedIn.
