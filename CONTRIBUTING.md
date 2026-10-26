# Contribuição

Use Python 3.11 ou 3.12 para uma nova instalação do projeto. O Superset possui seu próprio ambiente Docker. Preserve os notebooks como trilha didática e mantenha a execução operacional em `scripts/` e `sql/`.

Antes de propor mudanças:

```text
python scripts/validate_data.py
python -m unittest discover -s tests -v
python scripts/check_project.py
```

Se alterar transformações ou schema, execute a carga duas vezes no laboratório isolado e verifique reconciliação. Não aponte testes para um banco compartilhado.

Ao salvar notebooks, remova outputs e contadores de execução antes do commit. Não inclua senhas, tokens, arquivos `.env` ou configurações pessoais do Codex. Os nomes e números do CSV são sintéticos.

Mudanças de visualização precisam informar a versão do Superset/MCP, configuração aceita e evidência dos dados retornados. Não trate o parâmetro salvo como prova de agregação, ordenação ou aparência. Os IDs da instância do autor não são universais.

Descreva em cada contribuição: problema resolvido, alteração de comportamento, validação executada e limitações restantes.
