"""Carga completa do laboratório. Não cria objetos no Apache Superset."""
import argparse
import csv
import json
import os
from pathlib import Path

from validate_data import ROOT, validate


def load_env(path: Path) -> None:
    """Subconjunto simples KEY=VALUE; variáveis do processo têm precedência."""
    if not path.exists():
        return
    for line in path.read_text(encoding="utf-8-sig").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        key, separator, value = line.partition("=")
        if not separator or not key.strip():
            raise ValueError("Linha inválida no arquivo de ambiente")
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
            value = value[1:-1]
        os.environ.setdefault(key.strip(), value)


def run(csv_path: Path, port: int) -> dict:
    import psycopg2
    from psycopg2.extras import execute_values

    source = validate(csv_path)
    password = os.environ.get("POSTGRES_PASSWORD")
    if not password:
        raise ValueError("Defina POSTGRES_PASSWORD no ambiente ou .env")
    with csv_path.open(encoding="utf-8-sig", newline="") as stream:
        rows = list(csv.reader(stream))[1:]
    connection = psycopg2.connect(
        host=os.environ.get("DB_HOST", "127.0.0.1"), port=port,
        dbname=os.environ.get("POSTGRES_DB", "db_vendas"),
        user=os.environ.get("POSTGRES_USER", "postgres"), password=password,
        connect_timeout=10,
    )
    try:
        # DDL, substituição dos dados e validações na mesma transação.
        # Qualquer divergência desfaz a carga inteira.
        with connection:
            with connection.cursor() as cursor:
                cursor.execute((ROOT / "sql/01_schema.sql").read_text(encoding="utf-8"))
                cursor.execute("TRUNCATE TABLE gold.fato_vendas, silver.vendas, bronze.vendas")
                execute_values(cursor, "INSERT INTO bronze.vendas VALUES %s", rows)
                cursor.execute((ROOT / "sql/02_transform.sql").read_text(encoding="utf-8"))
                for table in ("bronze.vendas", "silver.vendas", "gold.fato_vendas"):
                    # Identificadores vêm exclusivamente desta lista fixa.
                    cursor.execute(
                        f"SELECT COUNT(*), COUNT(DISTINCT id_venda), "
                        f"SUM(valor_total), SUM(quantidade) FROM {table}"
                    )
                    count, distinct, revenue, items = cursor.fetchone()
                    if (count, distinct, str(revenue), items) != (
                        source["linhas"], source["vendas"], source["faturamento"], source["itens"]
                    ):
                        raise ValueError(f"Reconciliação reprovada na tabela {table}")
                # Verifica se os JOINs preservam o grão e o faturamento da fato.
                dataset_sql = (ROOT / "sql/03_dataset_analitico.sql").read_text(encoding="utf-8").strip().rstrip(";")
                cursor.execute(f"SELECT COUNT(*), SUM(valor_total) FROM ({dataset_sql}) AS dataset")
                count, revenue = cursor.fetchone()
                if count != source["vendas"] or str(revenue) != source["faturamento"]:
                    raise ValueError("JOINs do dataset analítico alteraram quantidade ou faturamento")
        return {"status": "carga validada", "fonte": source, "meses_esperados": source["meses"]}
    finally:
        connection.close()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--env-file", type=Path, default=ROOT / ".env")
    parser.add_argument("--csv", type=Path, default=ROOT / "dados/vendas.csv")
    parser.add_argument("--port", type=int, default=None)
    parser.add_argument("--full-refresh", action="store_true", required=True,
                        help="Substitui as linhas Bronze, Silver e fato Gold do banco configurado")
    args = parser.parse_args()
    try:
        load_env(args.env_file)
        port = args.port or int(os.environ.get("POSTGRES_PORT", "5434"))
        print(json.dumps(run(args.csv, port), ensure_ascii=False, indent=2))
    except Exception as exc:
        # Não imprime mensagens do driver com detalhes de conexão.
        parser.exit(1, f"Carga não concluída ({type(exc).__name__}). Confira configuração, schema e CSV.\n")


if __name__ == "__main__":
    main()
