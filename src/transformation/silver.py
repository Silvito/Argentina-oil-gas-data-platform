from pathlib import Path

import pandas as pd


def transform_to_silver(df: pd.DataFrame) -> pd.DataFrame:
    """
    Transforma un DataFrame Bronze en una versión Silver.

    Transformaciones:
    - Convierte fechaingreso a datetime.
    - Convierte fecha_data a datetime.
    - Convierte rectificado de t/f a boolean.
    - Convierte habilitado de t/f a boolean.
    """

    df_silver = df.copy()

    df_silver["fechaingreso"] = pd.to_datetime(
        df_silver["fechaingreso"],
        errors="coerce"
    )

    df_silver["fecha_data"] = pd.to_datetime(
        df_silver["fecha_data"],
        errors="coerce"
    )

    df_silver["rectificado"] = df_silver["rectificado"].map({
        "t": True,
        "f": False
    })

    df_silver["habilitado"] = df_silver["habilitado"].map({
        "t": True,
        "f": False
    })

    return df_silver


def save_silver(df: pd.DataFrame, output_path: Path) -> None:
    """
    Guarda el DataFrame Silver en formato Parquet.
    """

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    df.to_parquet(
        output_path,
        engine="pyarrow",
        index=False
    )