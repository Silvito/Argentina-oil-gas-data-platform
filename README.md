# Argentina Oil & Gas Data Platform

Plataforma de datos orientada al análisis de producción de petróleo y gas en Argentina, construida a partir de datos públicos del sector energético.

El proyecto simula un entorno profesional de **Data Engineering**, implementando progresivamente un pipeline de datos desde la extracción de información pública hasta su transformación, validación, modelado y posterior consumo analítico.

## Objetivo

Construir una plataforma de datos reproducible y escalable que permita procesar información de producción de pozos de petróleo y gas y generar datasets preparados para análisis y visualización.

El proyecto busca aplicar prácticas utilizadas en entornos reales de ingeniería de datos:

* Ingesta automatizada de datos.
* Data Lake y almacenamiento en formato Parquet.
* Procesamiento con Python y PySpark.
* Validación y Data Quality.
* Modelado dimensional.
* Transformaciones SQL mediante dbt.
* Orquestación de pipelines.
* Containerización.
* CI/CD.
* Cloud Computing.
* Analítica y visualización.

---

## Fuente de datos

Los datos utilizados provienen del portal oficial de datos abiertos del Gobierno de Argentina.

**Dataset:** Producción de petróleo y gas por pozo (Capítulo IV)

Fuente:

* Datos Argentina
* Secretaría de Energía

El proyecto utiliza la API CKAN del portal para descubrir los recursos disponibles y obtener los archivos correspondientes.

---

## Arquitectura

La arquitectura se desarrollará progresivamente a medida que avance el proyecto.

                    ┌──────────────────────────┐
                    │     Datos Argentina      │
                    │       CKAN API           │
                    └────────────┬─────────────┘
                                 │
                                 ▼
                    ┌──────────────────────────┐
                    │      Python Ingestion    │
                    │       API / CSV          │
                    └────────────┬─────────────┘
                                 │
                                 ▼
                     ___________________________            
                    │     Bronze / Raw Layer   │
                    │       ADLS / Parquet     │
                    └────────────┬─────────────┘
                                 │
                                 ▼
                    ┌──────────────────────────┐
                    │       PySpark             │
                    │   Cleaning / Processing  │
                    └────────────┬─────────────┘
                                 │
                                 ▼
                    ┌──────────────────────────┐
                    │      Silver Layer        │
                    │  Standardized Data       │
                    └────────────┬─────────────┘
                                 │
                                 ▼
                    ┌──────────────────────────┐
                    │          dbt              │
                    │ SQL Transformations      │
                    └────────────┬─────────────┘
                                 │
                                 ▼
                    ┌──────────────────────────┐
                    │       Gold Layer         │
                    │ Business-ready Data      │
                    └────────────┬─────────────┘
                                 │
                                 ▼
                    ┌──────────────────────────┐
                    │ Data Warehouse / Synapse │
                    └────────────┬─────────────┘
                                 │
                                 ▼
                    ┌──────────────────────────┐
                    │       Power BI            │
                    │ Analytics & Dashboards    │
                    └──────────────────────────┘


        Cross-cutting components

        Airflow       → Orchestration
        Docker        → Containerization
        Git/GitHub    → Version Control
        GitHub Actions→ CI/CD
        Pytest        → Data Quality
        dbt tests     → Data Quality

La arquitectura es evolutiva. Algunas tecnologías se incorporarán únicamente cuando sean necesarias para la siguiente etapa del pipeline.

Tech Stack
Data Engineering
Python
Pandas
PySpark
SQL
dbt
Data Storage
CSV
Parquet
Data Lake
Azure Data Lake Storage Gen2
Data Warehouse
Microsoft Fabric / Azure Synapse / PostgreSQL
SQL

La tecnología definitiva de serving/warehouse se definirá durante la etapa de modelado y cloud.

Orchestration
Apache Airflow
Cloud
Microsoft Azure
Azure Data Lake Storage Gen2
Azure Data Factory
Azure Synapse / Microsoft Fabric
Azure Databricks
Development
Git
GitHub
GitHub Actions
Docker
VS Code
Testing & Data Quality
Pytest
dbt tests
Data validation rules
Visualization
Power BI

Project Structure

Actualmente el proyecto se encuentra en una etapa inicial de Data Discovery.

Argentina-oil-gas-data-platform/
│
├── src/
│   └── ingestion/
│       └── ckan_client.py
│
├── notebooks/
│   └── 01_data_exploration.ipynb
│
├── docs/
│   └── data_discovery.md
│
├── data/
│   ├── raw/
│   ├── bronze/
│   ├── silver/
│   └── gold/
│
├── tests/
│
├── dbt/
│
├── airflow/
│
├── Dockerfile
├── requirements.txt
├── .gitignore
└── README.md

La estructura se irá ampliando a medida que se incorporen nuevas etapas.

Current Progress
Phase 0 — Project Design

Definición del objetivo

Definición de arquitectura inicial

Selección de fuente de datos

Creación del repositorio

Configuración del entorno Python

Phase 1 — Data Discovery

Identificación del dataset mediante CKAN API

Identificación de recursos disponibles

Identificación de recursos correspondientes a 2026

Descarga exploratoria de los datasets

Análisis inicial de estructura

Identificación de 38 columnas

Análisis inicial de valores nulos

Análisis de valores cero

Investigación preliminar de granularidad

Identificación de diferencias entre recursos

Phase 2 — Python Ingestion

Diseño del ingestion pipeline

Descarga automatizada

Manejo de errores y reintentos

Logging

Persistencia en Raw/Bronze

Configuración parametrizable

Phase 3 — Data Quality

Definición de Data Contract

Validación de esquema

Validación de tipos

Validación de claves

Validación de valores

Tests automatizados con Pytest

Phase 4 — Data Lake & Parquet

Conversión CSV → Parquet

Diseño de particiones

Bronze Layer

Silver Layer

Phase 5 — PySpark

Procesamiento distribuido

Transformaciones

Optimización

Escritura de datasets Silver

Phase 6 — Data Warehouse

Definición del modelo dimensional

Fact tables

Dimension tables

Star Schema

SQL analytics

Phase 7 — dbt

Staging models

Intermediate models

Mart models

Tests

Documentation

Lineage

Incremental models

Phase 8 — Cloud

Azure Data Lake Storage

Azure Data Factory

Databricks

Synapse / Fabric

Cloud architecture

Phase 9 — Orchestration

Airflow DAG

Pipeline dependencies

Scheduling

Monitoring

Phase 10 — Containerization

Dockerfile

Docker Compose

Reproducible environment

Phase 11 — CI/CD

GitHub Actions

Automated tests

Pipeline validation

Deployment workflow

Phase 12 — Analytics

Analytical queries

KPIs

Power BI dashboard

Production analysis

Well performance analysis

Geographic analysis

Data Discovery — Initial Findings

The 2026 dataset currently being investigated contains approximately 650,000 records and 38 columns.

The preliminary investigation indicates that:

idempresa + anio + mes + idpozo can act as a candidate natural key.
The current dataset appears to represent production information at a company + well + month level.
The standard Production resource and the DDJJ resource contain a different number of records.
1,563 records were identified in the DDJJ resource that were not present in the Production resource under the candidate key.
Several production and injection variables contain a high proportion of zero values.
iny_co2 contains only zero values in the 2026 sample investigated so far.
Some variables contain missing values and require business interpretation before defining data-quality rules.
Extreme values and near-zero floating-point values have been identified and require investigation rather than automatic removal.

These findings are preliminary and will be validated during the Data Discovery phase.

Detailed findings are documented in:

docs/data_discovery.md
Data Pipeline Principles

The project follows several principles commonly used in professional Data Engineering environments.

1. Understand the data before transforming it

Business meaning, grain, keys, units and source behavior will be investigated before implementing cleaning rules.

2. Preserve raw data

The original source data should remain available so that transformations can be reproduced and audited.

3. Separate storage layers

The pipeline will progressively separate:

Raw → Bronze → Silver → Gold

Each layer will have a clearly defined responsibility.

4. Validate before trusting

Data quality checks will be implemented before datasets are promoted to downstream layers.

5. Automate repetitive work

Manual downloads and transformations will progressively be replaced by reproducible pipelines.

6. Build incrementally

Technologies will be introduced when they solve a concrete problem instead of adding tools solely for the sake of the stack.

Expected Final Result

At the end of the project, the platform should be capable of:

Discovering new source resources automatically.
Ingesting production data.
Persisting raw source data.
Transforming and standardizing datasets.
Validating data quality automatically.
Processing data using distributed technologies.
Building dimensional analytical models.
Publishing business-ready datasets.
Orchestrating the complete pipeline.
Running automated tests through CI/CD.
Exposing analytical data through SQL and Power BI.

The final objective is to have a complete, reproducible end-to-end Data Engineering project that demonstrates practical knowledge of modern data platforms.

Learning Objectives

This project is also being developed as a practical learning environment to gain experience with:

Data ingestion
ETL / ELT
Data Lakes
Data Warehousing
Dimensional modeling
Distributed processing
Data quality
SQL analytics
Cloud data platforms
Pipeline orchestration
CI/CD
Infrastructure and containerization
Data visualization

The implementation will prioritize understanding why each technology is used, rather than simply assembling a large technology stack.

Author

Silvio Martinez

Data Engineering / Systems / Cloud

Argentina