from pathlib import Path

from pyspark.sql import DataFrame, SparkSession
from pyspark.sql.functions import col, to_timestamp, when


PROJECT_ROOT = Path(__file__).resolve().parents[2]

BRONZE_PATH = (
    PROJECT_ROOT
    / "data"
    / "bronze"
    / "production_2026.parquet"
)

SILVER_PATH = (
    PROJECT_ROOT
    / "data"
    / "silver"
    / "production_2026_spark.parquet"
)


def create_spark_session() -> SparkSession:

    return (
        SparkSession.builder
        .appName("ArgentinaOilGasSilver")
        .master("local[*]")
        .config(
            "spark.hadoop.fs.permissions.umask-mode",
            "022"
        )
        .getOrCreate()
    )


def transform_to_silver_spark(
    df: DataFrame,
) -> DataFrame:

    df_silver = (
        df
        .withColumn(
            "fechaingreso",
            to_timestamp(col("fechaingreso"))
        )
        .withColumn(
            "fecha_data",
            to_timestamp(col("fecha_data"))
        )
        .withColumn(
            "rectificado",
            when(col("rectificado") == "t", True)
            .when(col("rectificado") == "f", False)
        )
        .withColumn(
            "habilitado",
            when(col("habilitado") == "t", True)
            .when(col("habilitado") == "f", False)
        )
    )

    return df_silver


def save_silver_spark(
    df: DataFrame,
) -> None:

    (
        df.write
        .mode("overwrite")
        .parquet(str(SILVER_PATH))
    )


def main():

    spark = create_spark_session()

    df_bronze = spark.read.parquet(
        str(BRONZE_PATH)
    )

    df_silver = transform_to_silver_spark(
        df_bronze
    )

    print("Bronze rows:", df_bronze.count())
    print("Silver rows:", df_silver.count())

    df_silver.printSchema()

    save_silver_spark(df_silver)

    spark.stop()


if __name__ == "__main__":
    main()