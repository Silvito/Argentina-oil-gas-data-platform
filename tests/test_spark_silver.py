from pathlib import Path

import pandas as pd
from pyspark.sql import SparkSession
from pyspark.sql.functions import col


PROJECT_ROOT = Path(__file__).resolve().parents[1]

PANDAS_SILVER_PATH = (
    PROJECT_ROOT
    / "data"
    / "silver"
    / "production_2026.parquet"
)

SPARK_SILVER_PATH = (
    PROJECT_ROOT
    / "data"
    / "silver"
    / "production_2026_spark.parquet"
)

KEY_COLUMNS = [
    "idempresa",
    "anio",
    "mes",
    "idpozo",
]


def create_spark_session() -> SparkSession:
    return (
        SparkSession.builder
        .appName("TestSparkSilver")
        .master("local[*]")
        .getOrCreate()
    )


def test_spark_silver_matches_pandas_silver():

    pandas_df = pd.read_parquet(
        PANDAS_SILVER_PATH
    )

    spark = create_spark_session()

    # Convertimos el Silver de Pandas a Spark
    # sin utilizar toPandas() sobre el dataset de Spark.
    pandas_spark_df = spark.createDataFrame(
        pandas_df
    )

    spark_df = spark.read.parquet(
        str(SPARK_SILVER_PATH)
    )

    # --------------------------------------------------
    # 1. Validación estructural
    # --------------------------------------------------

    assert spark_df.count() == pandas_spark_df.count()

    assert spark_df.columns == pandas_spark_df.columns

    # --------------------------------------------------
    # 2. Validación de claves
    # --------------------------------------------------

    assert (
        spark_df
        .groupBy(KEY_COLUMNS)
        .count()
        .filter(col("count") > 1)
        .count()
        == 0
    )

    assert (
        pandas_spark_df
        .groupBy(KEY_COLUMNS)
        .count()
        .filter(col("count") > 1)
        .count()
        == 0
    )

    # --------------------------------------------------
    # 3. Comparación de claves
    # --------------------------------------------------

    spark_keys = spark_df.select(
        KEY_COLUMNS
    ).dropDuplicates()

    pandas_keys = pandas_spark_df.select(
        KEY_COLUMNS
    ).dropDuplicates()

    missing_in_spark = pandas_keys.subtract(
        spark_keys
    )

    missing_in_pandas = spark_keys.subtract(
        pandas_keys
    )

    assert missing_in_spark.count() == 0
    assert missing_in_pandas.count() == 0

    # --------------------------------------------------
    # 4. Comparación de valores
    # --------------------------------------------------

    value_columns = [
        column
        for column in spark_df.columns
        if column not in KEY_COLUMNS
    ]

    pandas_renamed = pandas_spark_df.select(
        *[
            col(column).alias(
                f"pandas_{column}"
            )
            for column in pandas_spark_df.columns
        ]
    )

    spark_renamed = spark_df.select(
        *[
            col(column).alias(
                f"spark_{column}"
            )
            for column in spark_df.columns
        ]
    )

    joined = pandas_renamed.join(
        spark_renamed,
        (
            (col("pandas_idempresa") == col("spark_idempresa"))
            & (col("pandas_anio") == col("spark_anio"))
            & (col("pandas_mes") == col("spark_mes"))
            & (col("pandas_idpozo") == col("spark_idpozo"))
        ),
        "inner",
    )

    # --------------------------------------------------
    # 5. Detectar diferencias
    # --------------------------------------------------

    differences = []

    for column in value_columns:

        pandas_column = col(
            f"pandas_{column}"
        )

        spark_column = col(
            f"spark_{column}"
        )

        difference = (
            pandas_column.isNull()
            != spark_column.isNull()
        ) | (
            pandas_column.isNotNull()
            & spark_column.isNotNull()
            & (pandas_column != spark_column)
        )

        differences.append(
            difference
        )

    any_difference = differences[0]

    for difference in differences[1:]:
        any_difference = (
            any_difference | difference
        )

    different_rows = joined.filter(
        any_difference
    )

    assert different_rows.count() == 0

    spark.stop()