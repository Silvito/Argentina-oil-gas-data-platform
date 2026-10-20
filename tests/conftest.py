
import pandas as pd
import pytest

from src.ai.tools import production_tool, history_tool


@pytest.fixture(autouse=True)
def silver_parquet_fixture(tmp_path, monkeypatch):
    """Create deterministic test data without relying on local datasets."""

    data = [
        {
            "idpozo": 28963,
            "anio": 2026,
            "mes": month,
            "prod_pet": oil,
            "prod_gas": 1.91 if month == 8 else 2.0,
            "prod_agua": -0.99 if month == 8 else 0.0,
        }
        for month, oil in enumerate(
            [27.05, 26.0, 25.0, 24.0, 23.0, 22.0, 21.0, 20.75],
            start=1,
        )
    ]

    path = tmp_path / "production_2026.parquet"
    pd.DataFrame(data).to_parquet(path, index=False)

    monkeypatch.setattr(production_tool, "SILVER_PATH", path)
    monkeypatch.setattr(history_tool, "SILVER_PATH", path)
