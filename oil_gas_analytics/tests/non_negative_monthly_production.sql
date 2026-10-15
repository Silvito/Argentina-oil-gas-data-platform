
SELECT *
FROM {{ ref('fct_monthly_production') }}
WHERE produccion_petroleo < 0
   OR produccion_gas < 0
   OR produccion_agua < 0
   OR cantidad_pozos < 0
