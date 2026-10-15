
SELECT
    anio,
    mes,
    provincia,
    cuenca,
    COUNT(*) AS cantidad
FROM {{ ref('fct_monthly_production') }}
GROUP BY
    anio,
    mes,
    provincia,
    cuenca
HAVING COUNT(*) > 1
