"""Checagens de integridade: sintaxe, notebooks limpos e links locais."""
import ast
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    errors = []
    paths = [ROOT / "gerar_dados.py"]
    for directory in ("scripts", "tests", "config"):
        paths.extend((ROOT / directory).rglob("*.py"))
    for path in paths:
        try:
            ast.parse(path.read_text(encoding="utf-8-sig"), filename=str(path))
        except SyntaxError as exc:
            errors.append(f"{path.relative_to(ROOT)}: {exc.msg}")
    for path in ROOT.glob("*.ipynb"):
        notebook = json.loads(path.read_text(encoding="utf-8"))
        if notebook.get("nbformat") != 4:
            errors.append(f"{path.name}: versão inesperada")
        for index, cell in enumerate(notebook["cells"]):
            if cell["cell_type"] != "code":
                continue
            if cell.get("outputs") or cell.get("execution_count") is not None:
                errors.append(f"{path.name}, célula {index}: contém outputs")
            source = "".join(cell.get("source", []))
            source = "\n".join(line for line in source.splitlines() if not line.lstrip().startswith("%"))
            try:
                ast.parse(source)
            except SyntaxError:
                errors.append(f"{path.name}, célula {index}: sintaxe inválida")
    markdown_paths = [ROOT / "README.md", ROOT / "CONTRIBUTING.md"]
    markdown_paths.extend((ROOT / "docs").rglob("*.md"))
    for path in markdown_paths:
        for target in re.findall(r"\]\(([^)]+)\)", path.read_text(encoding="utf-8")):
            if re.match(r"https?://|mailto:|#", target):
                continue
            target = target.split("#")[0]
            if not (path.parent / target).exists():
                errors.append(f"{path.relative_to(ROOT)}: link local ausente: {target}")
    if errors:
        raise SystemExit("\n".join(errors))
    print("Sintaxe Python, notebooks sem outputs e links locais: aprovados")


if __name__ == "__main__":
    main()
