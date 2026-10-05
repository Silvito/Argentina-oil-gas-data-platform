from pathlib import Path

from pyspark.sql import DataFrame, SparkSession
from pyspark.sql.functions import (
    countDistinct,
    sum,
)


PROJECT_ROOT = Path(__file__).resolve().parents[2]

SILVER_PATH = (
    PROJECT_ROOT
    / "data"
    / "silver"
    / "production_2026_spark.parquet"
)

GOLD_PATH = (
    PROJECT_ROOT
    / "data"
    / "gold"
    / "production_monthly"
)


def create_spark_session() -> SparkSession:
    return (
        SparkSession.builder
        .appName("ArgentinaOilGasGold")
        .master("local[*]")
        .getOrCreate()
    )


def transform_to_gold(df: DataFrame) -> DataFrame:
    """
    Creates a monthly production analytical dataset
    aggregated by year, month, province and basin.
    """

    df_gold = (
        df
        .groupBy(
            "anio",
            "mes",
            "provincia",
            "cuenca",
        )
        .agg(
            sum("prod_pet").alias("produccion_petroleo"),
            sum("prod_gas").alias("produccion_gas"),
            sum("prod_agua").alias("produccion_agua"),
            countDistinct("idpozo").alias("cantidad_pozos"),
        )
    )

    return df_gold


def save_gold(df: DataFrame) -> None:
    (
        df.write
        .mode("overwrite")
        .parquet(str(GOLD_PATH))
    )


def main():
    spark = create_spark_session()

    df_silver = spark.read.parquet(
        str(SILVER_PATH)
    )

    df_gold = transform_to_gold(df_silver)

    print("Silver rows:", df_silver.count())
    print("Gold rows:", df_gold.count())

    df_gold.printSchema()

    df_gold.orderBy(
        "anio",
        "mes",
        "provincia",
        "cuenca",
    ).show(20, truncate=False)

    save_gold(df_gold)
    spark.stop()


if __name__ == "__main__":
    main()