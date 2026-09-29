import pandas as pd

def validate_not_empty(df: pd.DataFrame) -> bool:
    """
    Verifica que el DataFrame tenga al menos un registro.
    """
    return len(df) > 0

def validate_required_columns(df: pd.DataFrame, required_columns: list[str]) -> bool:
     """
    Verifica que todas las columnas obligatorias existan.
    """
     return all(
        column in df.columns
        for column in required_columns
    )

def validate_candidate_key_not_null(df: pd.DataFrame, key_columns: list[str]) -> bool:
    """
    Verifica que las columnas de la clave candidata
    no contengan valores NULL.
    """
    return not df[key_columns].isnull().any().any()

def validate_candidate_key_unique(df: pd.DataFrame, key_columns: list[str]) -> bool:
    """
    Verifica que la combinación de columnas de la clave
    candidata sea única.
    """
    return not df.duplicated(
        subset=key_columns
    ).any()

def validate_month_range(df: pd.DataFrame, min_month: int = 1, max_month: int = 12) -> bool:
    """
    Verifica que todos los meses estén dentro
    del rango calendario válido.
    """
    return df["mes"].between(
        min_month,
        max_month
    ).all()

def validate_year(df: pd.DataFrame, expected_year: int) -> bool:
    """
    Verifica que todos los registros correspondan
    al año esperado.
    """
    return (df["anio"] == expected_year).all()

def validate_non_negative_columns(df: pd.DataFrame, columns: list[str]) -> bool:
    """
    Verifica que las columnas numéricas de producción
    e inyección no contengan valores negativos.
    """
    return (df[columns] >= 0).all().all()

def validate_production_period(df: pd.DataFrame) -> bool:
    """
    Verifica que el período de producción indicado por
    año y mes sea consistente con fecha_data.
    """
    expected_dates = pd.to_datetime(
        df["anio"].astype(str)
        + "-"
        + df["mes"].astype(str)
        + "-01"
    )

    actual_dates = df["fecha_data"].dt.to_period("M")

    return (
        expected_dates.dt.to_period("M")
        == actual_dates
    ).all()

def find_negative_values(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    """
    Devuelve los registros que contienen valores negativos
    en alguna de las columnas indicadas.
    """

    mask = (df[columns] < 0).any(axis=1)

    return df.loc[mask].copy()

def find_material_negative_values(df: pd.DataFrame, columns: list[str], tolerance: float = 1e-10) -> pd.DataFrame:
    """
    Devuelve registros con valores negativos que
    superan la tolerancia numérica definida.
    """

    mask = (df[columns] < -tolerance).any(axis=1)

    return df.loc[mask].copy()

def run_data_quality_checks(
    df: pd.DataFrame,
    key_columns: list[str],
    required_columns: list[str],
    expected_year: int,
    production_columns: list[str]
) -> dict[str, bool]:
    """
    Ejecuta todas las validaciones de calidad
    y devuelve sus resultados.
    """

    return {
        "not_empty": validate_not_empty(df),

        "required_columns": validate_required_columns(
            df,
            required_columns
        ),

        "candidate_key_not_null": validate_candidate_key_not_null(
            df,
            key_columns
        ),

        "candidate_key_unique": validate_candidate_key_unique(
            df,
            key_columns
        ),

        "month_range": validate_month_range(df),

        "expected_year": validate_year(
            df,
            expected_year
        ),

        "no_material_negative_values": (
            len(
                find_material_negative_values(
                    df,
                    production_columns
                )
            ) == 0
        ),
    }