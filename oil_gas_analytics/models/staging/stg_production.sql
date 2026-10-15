{{ config(materialized='view') }}

SELECT *
FROM read_parquet('../data/silver/production_2026.parquet')
