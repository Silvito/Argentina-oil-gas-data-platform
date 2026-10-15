from pathlib import Path
import sys

import duckdb

ROOT = Path(__file__).resolve().parents[2]
DB_PATH = ROOT / "oil_gas_analytics" / "dev.duckdb"
GOLD_PATH = ROOT / "data" / "gold" / "production_monthly"

KEYS = ["anio", "mes", "provincia", "cuenca"]
METRICS = [
    "produccion_petroleo",
    "produccion_gas",
    "produccion_agua",
]
TOLERANCE = 0.01


def fail(message):
    print(f"ERROR: {message}")
    sys.exit(1)


def main():
    if not DB_PATH.exists():
        fail(f"No se encontró la base DuckDB: {DB_PATH}")

    if not list(GOLD_PATH.glob("part-*.parquet")):
        fail(f"No se encontraron archivos Parquet en: {GOLD_PATH}")

    parquet_glob = (GOLD_PATH / "part-*.parquet").as_posix()
    columns = """
        anio, mes, provincia, cuenca,
        produccion_petroleo, produccion_gas,
        produccion_agua, cantidad_pozos
    """

    with duckdb.connect(str(DB_PATH), read_only=True) as con:
        dbt_df = con.execute(
            f"SELECT {columns} FROM main.fct_monthly_production"
        ).fetchdf()

        spark_df = con.execute(
            f"SELECT {columns} FROM read_parquet('{parquet_glob}')"
        ).fetchdf()

    print("=== RECONCILIACIÓN dbt vs PySpark Gold ===")
    print(f"Filas dbt:     {len(dbt_df)}")
    print(f"Filas PySpark: {len(spark_df)}")

    for name, df in [("dbt", dbt_df), ("PySpark", spark_df)]:
        if df.duplicated(KEYS).any():
            fail(f"{name} contiene claves duplicadas.")

    # El merge de Pandas permite emparejar las claves con cuenca nula.
    merged = dbt_df.merge(
        spark_df,
        on=KEYS,
        how="outer",
        suffixes=("_dbt", "_spark"),
        indicator=True,
    )

    only_dbt = merged[merged["_merge"] == "left_only"]
    only_spark = merged[merged["_merge"] == "right_only"]
    matched = merged[merged["_merge"] == "both"]

    print(f"Claves solo en dbt:     {len(only_dbt)}")
    print(f"Claves solo en PySpark: {len(only_spark)}")
    print(f"Claves coincidentes:    {len(matched)}")

    if not only_dbt.empty:
        print("\nClaves que solo aparecen en dbt:")
        print(only_dbt[KEYS].head(10).to_string(index=False))

    if not only_spark.empty:
        print("\nClaves que solo aparecen en PySpark:")
        print(only_spark[KEYS].head(10).to_string(index=False))

    count_diff = (
        matched["cantidad_pozos_dbt"] != matched["cantidad_pozos_spark"]
    )
    print(f"Filas con cantidad_pozos distinta: {int(count_diff.sum())}")

    metric_diffs = {}
    for metric in METRICS:
        delta = (
            matched[f"{metric}_dbt"].astype(float)
            - matched[f"{metric}_spark"].astype(float)
        ).abs()

        metric_diffs[metric] = delta > TOLERANCE
        max_delta = float(delta.max()) if not delta.empty else 0.0

        print(
            f"{metric}: diferencias > {TOLERANCE} = "
            f"{int(metric_diffs[metric].sum())}; "
            f"diferencia máxima = {max_delta}"
        )

    passed = (
        only_dbt.empty
        and only_spark.empty
        and len(matched) == len(dbt_df) == len(spark_df)
        and not count_diff.any()
        and all(not diff.any() for diff in metric_diffs.values())
    )

    if passed:
        print("\nRESULTADO: PASS — dbt y PySpark Gold coinciden.")
    else:
        print("\nRESULTADO: FAIL — revisar las diferencias anteriores.")
        sys.exit(1)


if __name__ == "__main__":
    main()