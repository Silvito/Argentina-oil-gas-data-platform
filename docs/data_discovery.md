# Data Discovery — Producción de petróleo y gas por pozo

## 1. Objetivo

El objetivo de esta etapa es comprender la estructura, granularidad, calidad y características de los datos de producción de petróleo y gas por pozo antes de diseñar el pipeline de Data Engineering.

La fuente utilizada es el dataset oficial de producción de petróleo y gas por pozo publicado mediante el portal de datos abiertos de Argentina.

La exploración se realizó sobre los recursos correspondientes al año 2026.

---

## 2. Recursos analizados

Se identificaron dos recursos correspondientes a 2026:

1. Producción de Pozos de Gas y Petróleo – 2026
2. Producción de Pozos de Gas y Petróleo – 2026 (DDJJ abiertas y cerradas)

Ambos recursos presentan 38 columnas y una estructura prácticamente idéntica.

---

## 3. Volumen de datos

### Producción 2026

* Registros: 650.281
* Columnas: 38

### DDJJ 2026

* Registros: 651.844
* Columnas: 38

Diferencia:

* Registros adicionales en DDJJ: 1.563
* Registros presentes únicamente en Producción: 0

El análisis de claves mostró que todos los registros identificados en Producción también están presentes en DDJJ, mientras que DDJJ contiene 1.563 combinaciones adicionales.

El motivo de estas diferencias queda pendiente de investigación.

---

## 4. Granularidad

Se evaluó la combinación:

`idempresa + anio + mes + idpozo`

No se encontraron registros duplicados utilizando esta combinación como clave.

Resultado:

* Duplicados en Producción 2026: 0
* Duplicados en DDJJ 2026: 0

Por lo tanto, se establece provisionalmente como hipótesis de granularidad:

> Una fila representa un registro de producción de un pozo perteneciente a una empresa durante un determinado mes.

Esta hipótesis deberá validarse posteriormente mediante el análisis de `fecha_data`, `fechaingreso`, estados y demás atributos del registro.

La combinación `idempresa + anio + mes + idpozo` queda definida como candidata a clave natural del registro.

---

## 5. Estructura identificada

Las principales columnas observadas incluyen:

### Identificación

* `idempresa`
* `idpozo`
* `anio`
* `mes`

### Producción

* `prod_pet`
* `prod_gas`
* `prod_agua`

### Inyección

* `iny_agua`
* `iny_gas`
* `iny_co2`
* `iny_otro`

### Características del pozo

* `tef`
* `vida_util`
* `tipoextraccion`
* `tipoestado`
* `tipopozo`
* `profundidad`
* `formacion`
* `formprod`

### Información administrativa

* `observaciones`
* `fechaingreso`
* `rectificado`
* `habilitado`
* `idusuario`

### Información empresarial y geográfica

* `empresa`
* `sigla`
* `idareapermisoconcesion`
* `areapermisoconcesion`
* `idareayacimiento`
* `areayacimiento`
* `cuenca`
* `provincia`

### Clasificación

* `tipo_de_recurso`
* `proyecto`
* `clasificacion`
* `subclasificacion`
* `sub_tipo_recurso`

### Fecha

* `fecha_data`

---

## 6. Valores faltantes

Se detectaron diferentes niveles de valores faltantes.

Entre los campos con mayor ausencia se encuentran:

* `vida_util`
* `observaciones`
* `formprod`
* `formacion`
* `clasificacion`
* `subclasificacion`
* `sub_tipo_recurso`

Los valores faltantes no deben considerarse automáticamente errores.

Antes de definir reglas de calidad será necesario determinar si la ausencia es esperada según el tipo, estado o clasificación del pozo.

---

## 7. Variables de producción e inyección

Sobre el recurso Producción 2026 se obtuvo:

| Variable    | Registros con valor 0 | Registros con valor distinto de 0 |
| ----------- | --------------------: | --------------------------------: |
| `prod_pet`  |               469.242 |                           181.039 |
| `prod_gas`  |               510.089 |                           140.192 |
| `prod_agua` |               469.715 |                           180.566 |
| `iny_agua`  |               608.917 |                            41.364 |
| `iny_gas`   |               650.094 |                               187 |
| `iny_co2`   |               650.281 |                                 0 |
| `iny_otro`  |               650.239 |                                42 |

Un hallazgo relevante es que `iny_co2` presenta valor 0 en el 100% de los registros del recurso 2026.

`iny_gas` y `iny_otro` presentan una cantidad muy reducida de registros distintos de cero.

No se eliminarán estas columnas en esta etapa. Primero se debe determinar si forman parte de un esquema general de producción/inyección y si su ausencia de actividad en 2026 es esperada.

---

## 8. Posibles anomalías detectadas

Durante el profiling se identificaron algunos valores que requieren investigación.

### `prod_pet`

El mínimo observado fue aproximadamente:

`-5e-16`

Este valor es prácticamente cero y puede estar relacionado con precisión numérica o representación de punto flotante.

No se considera todavía una producción negativa real.

### `prod_agua`

Se observó un mínimo de aproximadamente:

`-0,99`

Este valor requiere investigación antes de definir una regla de calidad que prohíba valores negativos.

### Valores extremos

También se observaron valores elevados en algunas variables de producción/inyección.

Estos valores no serán eliminados automáticamente. Primero se deberá determinar si corresponden a datos legítimos, unidades específicas o anomalías de origen.

---

## 9. Hallazgos principales

Al finalizar la primera etapa de Data Discovery se identificaron los siguientes puntos:

1. Los dos recursos 2026 tienen 38 columnas.
2. Producción contiene 650.281 registros.
3. DDJJ contiene 651.844 registros.
4. DDJJ contiene 1.563 registros adicionales.
5. Todos los registros de Producción están presentes en DDJJ según la clave analizada.
6. `idempresa + anio + mes + idpozo` no presenta duplicados en ninguno de los dos recursos.
7. Esta combinación queda como candidata a clave natural.
8. Existen campos con una proporción significativa de valores faltantes.
9. `iny_co2` tiene valor cero en todos los registros de 2026.
10. `iny_gas` e `iny_otro` presentan muy pocos registros distintos de cero.
11. Existen valores que requieren investigación antes de establecer reglas definitivas de calidad.
12. Todavía debe determinarse la diferencia semántica entre el recurso estándar y el recurso DDJJ.

---

## 10. Preguntas pendientes

Antes de comenzar la transformación de datos se deben resolver:

* ¿Qué representan exactamente las 1.563 filas adicionales de DDJJ?
* ¿Cuál es la diferencia funcional entre ambos recursos?
* ¿Cuál será la fuente principal de la primera versión del pipeline?
* ¿Qué significa cada columna desde el punto de vista del negocio?
* ¿Qué unidades utilizan las variables de producción e inyección?
* ¿Qué representa exactamente `tef`?
* ¿Qué representan `fecha_data`, `fechaingreso`, `rectificado` y `habilitado`?
* ¿Cuándo es válido que determinados campos sean `NULL`?
* ¿Qué reglas de calidad deben implementarse?
* ¿Qué columnas deben formar parte del modelo Silver?
* ¿Qué atributos serán dimensiones y cuáles medidas del modelo analítico?

---

## 11. Próxima etapa

La siguiente etapa será profundizar el Data Discovery antes de comenzar la transformación.

El flujo previsto es:

CKAN API
→ Data Discovery
→ Data Contract
→ Ingestion
→ Bronze
→ Data Quality
→ Silver
→ Data Warehouse / Gold
→ dbt
→ Orchestration
→ Cloud
→ Analytics

El siguiente objetivo inmediato será comprender la diferencia entre los dos recursos 2026 y completar el significado de las principales columnas antes de diseñar el esquema del pipeline.
