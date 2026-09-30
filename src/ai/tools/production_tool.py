from pathlib import Path

import pandas as pd

from src.ai.schemas.production import (
    WellProductionQuery,
    WellProductionResult,
)


PROJECT_ROOT = Path(__file__).resolve().parents[3]

SILVER_PATH = (
    PROJECT_ROOT
    / "data"
    / "silver"
    / "production_2026.parquet"
)


def get_well_production(
    query: WellProductionQuery,
) -> WellProductionResult:

    df = pd.read_parquet(SILVER_PATH)

    filtered = df[
        (df["idpozo"] == query.well_id)
        & (df["anio"] == query.year)
        & (df["mes"] == query.month)
    ]

    if filtered.empty:
        raise ValueError(
            f"No se encontró producción para "
            f"el pozo {query.well_id} "
            f"en {query.year}-{query.month:02d}"
        )

    if len(filtered) > 1:
        raise ValueError(
            f"Se encontraron múltiples registros para "
            f"el pozo {query.well_id} "
            f"en {query.year}-{query.month:02d}"
        )

    row = filtered.iloc[0]

    return WellProductionResult(
        well_id=int(row["idpozo"]),
        year=int(row["anio"]),
        month=int(row["mes"]),
        oil_m3=float(row["prod_pet"]),
        gas_m3=float(row["prod_gas"]),
        water_m3=float(row["prod_agua"]),
    )