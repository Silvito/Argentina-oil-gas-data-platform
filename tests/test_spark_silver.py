from pathlib import Path

import pandas as pd
from pyspark.sql import SparkSession


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

    spark_df = spark.read.parquet(
        str(SPARK_SILVER_PATH)
    )

    assert spark_df.count() == len(pandas_df)

    assert len(spark_df.columns) == len(
        pandas_df.columns
    )

    assert spark_df.columns == list(
        pandas_df.columns
    )

    spark.stop()