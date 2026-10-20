
import csv
import os
import tempfile
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]

RAW_PATH = PROJECT_ROOT / "data" / "raw" / "production_2026.csv"
BRONZE_PATH = PROJECT_ROOT / "data" / "bronze" / "production_2026.parquet"

REQUIRED_COLUMNS = {"idpozo", "anio", "mes"}


def convert_raw_to_bronze() -> None:
    """Convierte el CSV RAW validado a Parquet en Bronze."""

    if not RAW_PATH.is_file():
        raise FileNotFoundError(
            f"No se encontró el archivo RAW: {RAW_PATH}"
        )

    if RAW_PATH.stat().st_size == 0:
        raise ValueError("El archivo RAW está vacío.")

    print(f"Leyendo archivo RAW: {RAW_PATH}", flush=True)

    with RAW_PATH.open("r", encoding="utf-8-sig", errors="strict") as file:
        sample = file.read(65536)

    if not sample.strip():
        raise ValueError("El archivo RAW no contiene datos.")

    try:
        delimiter = csv.Sniffer().sniff(
            sample,
            delimiters=",;\t|",
        ).delimiter
    except csv.Error:
        delimiter = ","

    df = pd.read_csv(
        RAW_PATH,
        sep=delimiter,
        low_memory=False,
    )

    df.columns = [
        column.strip().lstrip("\ufeff")
        for column in df.columns
    ]

    missing_columns = REQUIRED_COLUMNS - set(
        column.lower() for column in df.columns
    )

    if missing_columns:
        raise ValueError(
            f"Faltan columnas obligatorias en RAW: "
            f"{sorted(missing_columns)}"
        )

    if df.empty:
        raise ValueError("El CSV no contiene registros.")

    BRONZE_PATH.parent.mkdir(parents=True, exist_ok=True)

    temp_path = None

    try:
        with tempfile.NamedTemporaryFile(
            dir=BRONZE_PATH.parent,
            prefix="production_2026_",
            suffix=".parquet",
            delete=False,
        ) as temp_file:
            temp_path = Path(temp_file.name)

        df.to_parquet(
            temp_path,
            engine="pyarrow",
            index=False,
        )

        os.replace(temp_path, BRONZE_PATH)
        temp_path = None

    finally:
        if temp_path is not None:
            temp_path.unlink(missing_ok=True)

    print(f"Bronze generado: {BRONZE_PATH}", flush=True)
    print(f"Registros: {len(df):,}", flush=True)
    print(f"Columnas: {len(df.columns)}", flush=True)
    print("Conversión RAW → Bronze completada.", flush=True)


def main() -> None:
    convert_raw_to_bronze()


if __name__ == "__main__":
    main()
