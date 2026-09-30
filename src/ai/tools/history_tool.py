from pathlib import Path

import pandas as pd

from src.ai.schemas.production import WellProductionResult


PROJECT_ROOT = Path(__file__).resolve().parents[3]

SILVER_PATH = (
    PROJECT_ROOT
    / "data"
    / "silver"
    / "production_2026.parquet"
)


def get_well_history(
    well_id: int,
    year: int,
) -> list[WellProductionResult]:

    df = pd.read_parquet(SILVER_PATH)

    filtered = df[
        (df["idpozo"] == well_id)
        & (df["anio"] == year)
    ].copy()

    if filtered.empty:
        raise ValueError(
            f"No se encontró historial para "
            f"el pozo {well_id} "
            f"en {year}"
        )

    filtered = filtered.sort_values("mes")

    results = []

    for _, row in filtered.iterrows():

        results.append(
            WellProductionResult(
                well_id=int(row["idpozo"]),
                year=int(row["anio"]),
                month=int(row["mes"]),
                oil_m3=float(row["prod_pet"]),
                gas_m3=float(row["prod_gas"]),
                water_m3=float(row["prod_agua"]),
            )
        )

    return results