
{{ config(materialized='table') }}

SELECT
    anio,
    mes,
    provincia,
    cuenca,
    SUM(prod_pet) AS produccion_petroleo,
    SUM(prod_gas) AS produccion_gas,
    SUM(prod_agua) AS produccion_agua,
    COUNT(DISTINCT idpozo) AS cantidad_pozos
FROM {{ ref('stg_production') }}
GROUP BY
    anio,
    mes,
    provincia,
    cuenca
