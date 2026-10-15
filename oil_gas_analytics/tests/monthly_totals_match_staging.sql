
WITH source_totals AS (
    SELECT
        SUM(prod_pet) AS petroleo,
        SUM(prod_gas) AS gas,
        SUM(prod_agua) AS agua
    FROM {{ ref('stg_production') }}
),
mart_totals AS (
    SELECT
        SUM(produccion_petroleo) AS petroleo,
        SUM(produccion_gas) AS gas,
        SUM(produccion_agua) AS agua
    FROM {{ ref('fct_monthly_production') }}
)
SELECT *
FROM source_totals
CROSS JOIN mart_totals
WHERE ABS(source_totals.petroleo - mart_totals.petroleo) > 0.01
   OR ABS(source_totals.gas - mart_totals.gas) > 0.01
   OR ABS(source_totals.agua - mart_totals.agua) > 0.01
