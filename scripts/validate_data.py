"""Valida o CSV sem banco, Pandas ou bibliotecas externas. Saída JSON."""
import argparse
import csv
import json
from datetime import date
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COLUMNS = [
    "id_venda", "data_venda", "cliente", "produto", "categoria", "regiao",
    "quantidade", "valor_unitario", "desconto_percentual", "valor_total",
    "forma_pagamento",
]


def validate(path: Path) -> dict:
    with path.open(encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream)
        if reader.fieldnames != COLUMNS:
            raise ValueError("Colunas do CSV diferentes do contrato esperado")
        rows = list(reader)
    if not rows:
        raise ValueError("CSV sem vendas")
    ids, dates, revenue, items = set(), [], Decimal("0"), 0
    for line, row in enumerate(rows, start=2):
        if None in row or any(v is None or not v.strip() for v in row.values()):
            raise ValueError(f"Linha {line}: campos ausentes ou extras")
        try:
            sale_id = int(row["id_venda"])
            day = date.fromisoformat(row["data_venda"])
            quantity = int(row["quantidade"])
            price = Decimal(row["valor_unitario"])
            discount = Decimal(row["desconto_percentual"])
            total = Decimal(row["valor_total"])
            if not all(v.is_finite() for v in (price, discount, total)):
                raise ValueError("Valor monetário não finito")
        except (ValueError, InvalidOperation) as exc:
            raise ValueError(f"Linha {line}: tipos inválidos") from exc
        if sale_id in ids:
            raise ValueError(f"Linha {line}: id_venda duplicado")
        if sale_id <= 0 or quantity <= 0 or price < 0 or total < 0 or not 0 <= discount <= 100:
            raise ValueError(f"Linha {line}: valor fora do domínio")
        expected = (quantity * price * (1 - discount / 100)).quantize(
            Decimal("0.01"), rounding=ROUND_HALF_UP
        )
        if total != expected:
            raise ValueError(f"Linha {line}: valor_total diverge da fórmula")
        ids.add(sale_id)
        dates.append(day)
        revenue += total
        items += quantity
    return {
        "status": "aprovado", "vendas": len(ids), "linhas": len(rows),
        "faturamento": str(revenue), "ticket_medio": str(revenue / len(ids)),
        "itens": items, "primeira_data": str(min(dates)), "ultima_data": str(max(dates)),
        "meses": len({(d.year, d.month) for d in dates}),
        "categorias": len({r["categoria"] for r in rows}),
        "regioes": len({r["regiao"] for r in rows}),
        "produtos": len({r["produto"] for r in rows}),
        "formas_pagamento": len({r["forma_pagamento"] for r in rows}),
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--csv", type=Path, default=ROOT / "dados/vendas.csv")
    args = parser.parse_args()
    try:
        print(json.dumps(validate(args.csv), ensure_ascii=False, indent=2))
    except (OSError, ValueError) as exc:
        parser.exit(1, f"Validação reprovada: {exc}\n")
