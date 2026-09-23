# Data Discovery — Producción de petróleo y gas por pozo

## 1. Objetivo

El objetivo de esta etapa es comprender la estructura, granularidad, calidad y características de los datos de producción de petróleo y gas por pozo antes de diseñar el pipeline de Data Engineering.

La fuente utilizada es el dataset oficial de producción de petróleo y gas por pozo publicado mediante el portal de datos abiertos de Argentina.

La exploración se realizó sobre los recursos correspondientes al año 2026.

---

## 2. Fuente de datos

La fuente utilizada es el dataset oficial:

Producción de petróleo y gas por pozo (Capítulo IV)

Dataset ID utilizado en la API CKAN:

produccion-de-petroleo-y-gas-por-pozo

La metadata del dataset fue obtenida mediante la API CKAN:

https://datos.gob.ar/api/3/action/package_show

La consulta se realizó utilizando el parámetro:

id=produccion-de-petroleo-y-gas-por-pozo

## 3. Recursos analizados

Durante la exploración se identificaron dos recursos correspondientes a 2026.

## 3.1 Producción de Pozos de Gas y Petróleo – 2026

Formato:

CSV

Recurso:

Producción de Pozos de Gas y Petróleo – 2026
## 3.2 Producción de Pozos de Gas y Petróleo - 2026 (DDJJ abiertas y cerradas)

Formato:

CSV

Recurso:

Producción de Pozos de Gas y Petróleo - 2026 (DDJJ abiertas y cerradas)

Ambos recursos contienen una estructura de 38 columnas.

## 4. Estructura del dataset

Las columnas identificadas son:

idempresa
anio
mes
idpozo
prod_pet
prod_gas
prod_agua
iny_agua
iny_gas
iny_co2
iny_otro
tef
vida_util
tipoextraccion
tipoestado
tipopozo
observaciones
fechaingreso
rectificado
habilitado
idusuario
empresa
sigla
formprod
profundidad
formacion
idareapermisoconcesion
areapermisoconcesion
idareayacimiento
areayacimiento
cuenca
provincia
tipo_de_recurso
proyecto
clasificacion
subclasificacion
sub_tipo_recurso
fecha_data

Total:

38 columnas

## 5. Granularidad

Durante la exploración se identificó una combinación candidata a clave natural:

idempresa + anio + mes + idpozo

Esta combinación representa conceptualmente un registro de producción/inyección de un determinado pozo, empresa y período.

Se verificó su unicidad en ambos recursos.

Resultado
Producción 2026:
653.202 registros
653.202 claves únicas

DDJJ 2026:
654.765 registros
654.765 claves únicas

No se encontraron duplicados utilizando:

idempresa
anio
mes
idpozo
Importante

Esta combinación se considera actualmente una candidate natural key.

Todavía no se la define como primary key formal del modelo porque su significado de negocio deberá documentarse en el Data Contract.

## 6. Volumen actual de datos

Durante la exploración se detectó que los recursos publicados por la fuente pueden cambiar entre diferentes descargas.

En una primera descarga se obtuvieron:

Producción: 650.281 registros
DDJJ:       651.844 registros

En una descarga posterior:

Producción: 653.202 registros
DDJJ:       654.765 registros

El incremento fue:

653.202 - 650.281 = 2.921

para Producción, y:

654.765 - 651.844 = 2.921

para DDJJ.

La diferencia entre ambos recursos se mantuvo:

654.765 - 653.202 = 1.563

Esto demuestra que los recursos publicados son dinámicos y pueden actualizarse entre diferentes ejecuciones.

## 7. Perfil de valores nulos

Durante la exploración se observaron diferentes niveles de completitud entre las columnas.

Algunas columnas presentan información prácticamente completa, mientras que otras contienen valores nulos en una cantidad significativa de registros.

Entre las columnas con mayor presencia de valores faltantes se encuentran:

vida_util
observaciones
formprod
formacion
clasificacion
subclasificacion
sub_tipo_recurso

Los valores nulos no serán eliminados automáticamente.

La estrategia de calidad deberá determinar posteriormente si un campo:

es obligatorio;
es opcional;
depende del tipo de pozo;
depende del tipo de recurso;
o representa información administrativa.
## 8. Variables de producción e inyección

Las principales variables numéricas identificadas son:

prod_pet
prod_gas
prod_agua

iny_agua
iny_gas
iny_co2
iny_otro

Durante la exploración se observó una distribución altamente sesgada.

Una gran proporción de registros presenta valores iguales a cero, mientras que una cantidad menor de pozos concentra una parte importante de la producción o inyección.

Por esta razón, valores elevados no serán eliminados automáticamente como outliers.

Primero deberán analizarse desde el punto de vista del dominio y, cuando sea necesario, contrastarse con la documentación de la fuente.

9. Valores cercanos a cero y valores negativos

Durante la exploración aparecieron algunos valores numéricos extremadamente pequeños o negativos.

Por ejemplo, en determinadas variables se observaron valores cercanos a:

-5e-16

Estos valores pueden corresponder a errores de precisión de punto flotante y no necesariamente representan una producción negativa real.

También se detectaron valores negativos en algunas variables donde será necesario comprender primero la semántica del campo.

Decisión

No se eliminarán ni corregirán automáticamente estos valores durante Data Discovery.

La transformación de estos valores será definida posteriormente mediante reglas explícitas de calidad y Data Contract.

## 10. Reconciliación Producción vs DDJJ

Se realizó una comparación utilizando como clave:

idempresa
anio
mes
idpozo

El resultado fue:

Producción: 653.202
DDJJ:       654.765

Registros compartidos: 653.202
Registros adicionales en DDJJ: 1.563

Por lo tanto:

Producción ⊆ DDJJ

para el snapshot analizado.

## 11. Comparación de columnas

Para las 653.202 claves compartidas se compararon todas las columnas no pertenecientes a la clave.

Se compararon variables de:

producción;
inyección;
estado;
empresa;
formación;
profundidad;
áreas;
yacimientos;
clasificación;
metadata;
fechas;
información administrativa.
Resultado

No se encontraron diferencias.

Ejemplos:

prod_pet:                  0 diferencias
prod_gas:                  0 diferencias
prod_agua:                 0 diferencias
iny_agua:                  0 diferencias
iny_gas:                   0 diferencias
iny_co2:                   0 diferencias
iny_otro:                  0 diferencias

tipoextraccion:            0 diferencias
tipoestado:                0 diferencias
tipopozo:                  0 diferencias

observaciones:             0 diferencias
fechaingreso:              0 diferencias
rectificado:               0 diferencias
habilitado:                0 diferencias

empresa:                   0 diferencias
sigla:                     0 diferencias
formprod:                  0 diferencias
profundidad:               0 diferencias
formacion:                 0 diferencias

idareapermisoconcesion:    0 diferencias
areapermisoconcesion:      0 diferencias
idareayacimiento:          0 diferencias
areayacimiento:            0 diferencias

clasificacion:             0 diferencias
subclasificacion:          0 diferencias
sub_tipo_recurso:          0 diferencias
fecha_data:                0 diferencias
Conclusión

Para las claves compartidas, los dos recursos contienen exactamente la misma información.

La diferencia entre ambos recursos está actualmente concentrada en los:

1.563 registros adicionales de DDJJ
## 12. Análisis de los registros exclusivos de DDJJ

Se construyó un subconjunto:

only_ddjj_df

que contiene los registros presentes en DDJJ pero ausentes en Producción.

Total:

1.563 registros

Estos registros no deben considerarse automáticamente como duplicados, errores o información administrativa.

## 13. Distribución temporal de los registros exclusivos

Los registros adicionales corresponden únicamente a dos meses:

2026-06 → 1.508 registros
2026-08 → 55 registros

Por lo tanto:

Junio 2026: 1.508
Agosto 2026: 55

No se encontraron registros adicionales correspondientes a otros meses dentro del snapshot analizado.

## 14. Distribución por empresa y provincia

Los 1.563 registros adicionales presentan una distribución muy concentrada:

Empresa	Provincia	Registros
BREST S.A. DE SERVICIOS PETROLEROS	Santa Cruz	837
VELITEC S.A.	Tierra del Fuego	671
Pilgrim Energy S.A.	Chubut	35
HATTRICK ENERGY SAS	Mendoza	20
Total	
	1.563

Esto demuestra que los registros adicionales no están distribuidos aleatoriamente.

Existe una fuerte concentración en determinadas empresas y provincias.

## 15. Actividad productiva de los registros exclusivos

Se analizaron las siguientes variables:

prod_pet
prod_gas
prod_agua
iny_agua
iny_gas
iny_co2
iny_otro

De los 1.563 registros:

1.322 → todas las variables = 0
241   → al menos una variable ≠ 0

Porcentaje:

84,6% → sin actividad en estas variables
15,4% → con actividad

Por lo tanto, los registros adicionales de DDJJ no pueden ser considerados simplemente registros administrativos sin actividad.

## 16. Producción e inyección acumulada de los registros adicionales

Los 1.563 registros exclusivos de DDJJ presentan los siguientes totales:

Variable	Total
prod_pet	14.702,602430
prod_gas	19.611,425166
prod_agua	180.287,889745
iny_agua	227.191,245800
iny_gas	0
iny_co2	0
iny_otro	0

Los valores demuestran que una parte de estos registros contiene actividad productiva o de inyección relevante.

## 17. Distribución de la actividad

Para los registros exclusivos de DDJJ:

Petróleo
Media: 9,406655
Máximo: 852,859141
Gas
Media: 12,547297
Máximo: 1.779,894296
Agua producida
Media: 115,347338
Máximo: 7.740,700000
Agua inyectada
Media: 145,355883
Máximo: 17.396,509100

Las distribuciones presentan una fuerte concentración en cero y una cola de valores positivos.

## 18. Interpretación actual de Producción vs DDJJ

A partir de la evidencia obtenida podemos establecer:

DDJJ contiene todos los registros encontrados en Producción para el snapshot analizado.
Los registros compartidos son idénticos en todas las columnas comparadas.
DDJJ contiene 1.563 registros adicionales.
Los registros adicionales están concentrados en junio y agosto de 2026.
Están concentrados en cuatro empresas/provincias.
Una parte de esos registros presenta actividad productiva o de inyección.
Por lo tanto, no es correcto descartarlos automáticamente.
Todavía no se conoce con certeza el significado funcional que diferencia ambos recursos.
## 19. Fechas y comportamiento de actualización

También se observó que fecha_data y fechaingreso representan conceptos diferentes.

Los registros pueden tener un período de producción determinado por:

anio + mes

mientras que fechaingreso puede corresponder a una fecha posterior.

Por ejemplo, entre los registros adicionales de DDJJ se observaron cargas realizadas durante agosto y septiembre para datos correspondientes a períodos anteriores.

Esto sugiere que el proceso de publicación/declaración puede incorporar información posteriormente al período de producción.

Esta interpretación debe considerarse una hipótesis de Data Discovery hasta contar con documentación funcional oficial que confirme el significado exacto de cada campo.

## 20. Naturaleza dinámica de la fuente

Uno de los hallazgos más importantes de esta fase fue comprobar que los archivos publicados pueden cambiar entre distintas ejecuciones.

La misma consulta sobre los recursos 2026 produjo:

Primera extracción
Producción: 650.281
DDJJ:       651.844
Extracción posterior
Producción: 653.202
DDJJ:       654.765

Incremento:

+2.921 registros

en ambos recursos.

Esto implica que la fuente no debe tratarse como un archivo estático.

El pipeline deberá contemplar eventualmente:

fecha de extracción;
metadata de ejecución;
versionado/snapshots;
reproducibilidad;
detección de cambios;
trazabilidad de los datos.
## 21. Decisiones de Data Engineering derivadas

A partir del Data Discovery se establecen las siguientes decisiones preliminares:

No eliminar registros DDJJ adicionales

Los 1.563 registros adicionales se conservarán hasta comprender completamente su significado.

No modificar automáticamente valores extremos

Los outliers deberán investigarse según reglas de negocio antes de ser corregidos o eliminados.

No convertir automáticamente valores negativos en cero

Los valores negativos o cercanos a cero deberán analizarse según la semántica de cada variable.

Mantener la granularidad original

La primera capa de almacenamiento deberá preservar el registro original.

Mantener metadata de ingesta

Debido a que la fuente cambia entre descargas, la ingesta deberá registrar información suficiente para reproducir y auditar cada extracción.

Utilizar una clave natural candidata

Se continuará trabajando con:

idempresa + anio + mes + idpozo

como candidate natural key hasta formalizar el Data Contract.

## 22. Preguntas todavía abiertas

Antes de considerar completamente cerrada la interpretación funcional de los datos quedan algunas preguntas:

¿Cuál es exactamente la diferencia conceptual entre Producción y DDJJ?
¿Qué representa funcionalmente una DDJJ abierta o cerrada?
¿Por qué determinados registros aparecen en DDJJ pero no en Producción?
¿Qué reglas determinan cuándo un registro pasa de DDJJ a Producción?
¿Cuál es la unidad exacta de cada variable de producción e inyección?
¿Qué significado tienen exactamente rectificado y habilitado?
¿Qué representa fecha_data frente a fechaingreso?
¿Existen reglas de negocio documentadas para valores cero, negativos y extremos?

Estas preguntas podrán resolverse posteriormente mediante documentación oficial, análisis histórico y validaciones adicionales.

## 23. Data Contract — versión preliminar

A partir del análisis realizado se puede establecer un contrato preliminar:

Identificación del registro
idempresa
anio
mes
idpozo
Dimensiones temporales
anio
mes
fecha_data
fechaingreso
Producción
prod_pet
prod_gas
prod_agua
Inyección
iny_agua
iny_gas
iny_co2
iny_otro
Información del pozo
idpozo
tipoextraccion
tipoestado
tipopozo
profundidad
vida_util
formprod
formacion
Información geográfica y administrativa
empresa
sigla
provincia
cuenca
areayacimiento
idareayacimiento
areapermisoconcesion
idareapermisoconcesion
proyecto

Este contrato es preliminar y podrá evolucionar durante las siguientes fases.

## 24. Estado de Data Discovery

La fase de Data Discovery se considera completada a nivel inicial.

Se logró:

identificar la fuente;
identificar los recursos 2026;
obtener los datos mediante la API CKAN;
analizar estructura;
analizar tipos de datos;
analizar valores faltantes;
identificar una candidate natural key;
comprobar ausencia de duplicados mediante dicha clave;
comparar Producción y DDJJ;
identificar los 1.563 registros adicionales;
analizar su distribución temporal;
analizar su distribución por empresa y provincia;
analizar su actividad productiva;
detectar que la fuente cambia entre descargas;
identificar preguntas funcionales pendientes.

## 25. Próxima fase

La siguiente etapa del proyecto será:

Fase 2 — Python Data Ingestion

Objetivo:

Construir una ingesta reproducible y reutilizable que:

CKAN API
   ↓
descubrimiento del recurso
   ↓
descarga
   ↓
validación básica
   ↓
metadata de ejecución
   ↓
almacenamiento Raw/Bronze

La implementación deberá comenzar de forma incremental.

Primero se construirá el downloader utilizando las funciones ya desarrolladas en:

src/ingestion/ckan_client.py

Posteriormente se incorporarán:

manejo de errores;
logging;
metadata;
rutas de almacenamiento;
versionado/snapshots;
validaciones;
formato Parquet.
## 26. Principio de diseño

La plataforma conservará inicialmente los datos originales antes de aplicar transformaciones destructivas.

El principio será:

SOURCE
  ↓
RAW / BRONZE
  ↓
TRANSFORMATION
  ↓
SILVER
  ↓
GOLD

De esta forma será posible:

auditar el pipeline;
reproducir transformaciones;
comparar versiones;
detectar cambios en la fuente;
investigar errores;
demostrar buenas prácticas de Data Engineering.
Resumen ejecutivo

El Data Discovery permitió determinar que el dataset 2026 contiene dos recursos relacionados: Producción y DDJJ. Para el snapshot analizado, DDJJ contiene los 653.202 registros de Producción exactamente sin diferencias en las columnas comparadas, además de 1.563 registros adicionales. Estos registros adicionales se concentran en junio y agosto de 2026 y en cuatro empresas/provincias, y 241 de ellos presentan actividad productiva o de inyección.

La fuente además demostró ser dinámica, ya que entre dos extracciones el volumen aumentó en 2.921 registros en ambos recursos. Por este motivo, la futura plataforma deberá contemplar trazabilidad, metadata de ingesta y mecanismos de versionado o snapshot.

La siguiente etapa será implementar una ingesta Python reproducible que preserve los datos originales antes de comenzar las transformaciones.