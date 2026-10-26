import csv
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from validate_data import COLUMNS, validate


class DataContractTests(unittest.TestCase):
    def test_reference_dataset(self):
        result = validate(ROOT / "dados/vendas.csv")
        self.assertEqual(result["vendas"], 1000)
        self.assertEqual(result["faturamento"], "2318923.25")
        self.assertEqual(result["itens"], 3074)
        self.assertEqual(result["meses"], 21)

    def test_rejects_duplicate_identifier(self):
        with (ROOT / "dados/vendas.csv").open(encoding="utf-8-sig") as stream:
            row = next(csv.DictReader(stream))
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "duplicate.csv"
            with path.open("w", encoding="utf-8", newline="") as stream:
                writer = csv.DictWriter(stream, fieldnames=COLUMNS)
                writer.writeheader()
                writer.writerows([row, row])
            with self.assertRaisesRegex(ValueError, "duplicado"):
                validate(path)

    def test_rejects_incorrect_revenue(self):
        with (ROOT / "dados/vendas.csv").open(encoding="utf-8-sig") as stream:
            row = next(csv.DictReader(stream))
        row["valor_total"] = "0.01"
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "invalid.csv"
            with path.open("w", encoding="utf-8", newline="") as stream:
                writer = csv.DictWriter(stream, fieldnames=COLUMNS)
                writer.writeheader()
                writer.writerow(row)
            with self.assertRaisesRegex(ValueError, "fórmula"):
                validate(path)


if __name__ == "__main__":
    unittest.main()
