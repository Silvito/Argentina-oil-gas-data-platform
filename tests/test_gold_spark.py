from pathlib import Path

from pyspark.sql import SparkSession
from pyspark.sql.functions import col


PROJECT_ROOT = Path(__file__).resolve().parents[1]

GOLD_PATH = (
    PROJECT_ROOT
    / "data"
    / "gold"
    / "production_monthly"
)


KEY_COLUMNS = [
    "anio",
    "mes",
    "provincia",
    "cuenca",
]

FLOAT_TOLERANCE = 1e-4


def create_spark_session() -> SparkSession:
    return (
        SparkSession.builder
        .appName("TestGoldSpark")
        .master("local[*]")
        .getOrCreate()
    )


def test_gold_is_not_empty():

    spark = create_spark_session()

    df_gold = spark.read.parquet(
        str(GOLD_PATH)
    )

    assert df_gold.count() > 0

    spark.stop()


def test_gold_has_unique_keys():

    spark = create_spark_session()

    df_gold = spark.read.parquet(
        str(GOLD_PATH)
    )

    duplicate_keys = (
        df_gold
        .groupBy(KEY_COLUMNS)
        .count()
        .filter(col("count") > 1)
    )

    assert duplicate_keys.count() == 0

    spark.stop()


def test_gold_month_is_valid():

    spark = create_spark_session()

    df_gold = spark.read.parquet(
        str(GOLD_PATH)
    )

    invalid_months = (
        df_gold
        .filter(
            (col("mes") < 1)
            | (col("mes") > 12)
        )
    )

    assert invalid_months.count() == 0

    spark.stop()


def test_gold_metrics_are_not_negative():

    spark = create_spark_session()

    df_gold = spark.read.parquet(
        str(GOLD_PATH)
    )

    numeric_columns = [
        "produccion_petroleo",
        "produccion_gas",
        "produccion_agua",
        "cantidad_pozos",
    ]

    for column in numeric_columns:

        negative_values = (
            df_gold
            .filter(col(column) < 0)
        )

        assert negative_values.count() == 0

    spark.stop()


def test_gold_preserves_production_totals():

    spark = create_spark_session()

    silver_path = (
        PROJECT_ROOT
        / "data"
        / "silver"
        / "production_2026_spark.parquet"
    )

    df_silver = spark.read.parquet(
        str(silver_path)
    )

    df_gold = spark.read.parquet(
        str(GOLD_PATH)
    )

    silver_totals = (
        df_silver
        .agg(
            {"prod_pet": "sum",
             "prod_gas": "sum",
             "prod_agua": "sum"}
        )
        .collect()[0]
    )

    gold_totals = (
        df_gold
        .agg(
            {"produccion_petroleo": "sum",
             "produccion_gas": "sum",
             "produccion_agua": "sum"}
        )
        .collect()[0]
    )

    assert abs(
        silver_totals["sum(prod_pet)"]
        - gold_totals["sum(produccion_petroleo)"]
    ) < FLOAT_TOLERANCE

    assert abs(
        silver_totals["sum(prod_gas)"]
        - gold_totals["sum(produccion_gas)"]
    ) < FLOAT_TOLERANCE

    assert abs(
        silver_totals["sum(prod_agua)"]
        - gold_totals["sum(produccion_agua)"]
    ) < FLOAT_TOLERANCE

    spark.stop()