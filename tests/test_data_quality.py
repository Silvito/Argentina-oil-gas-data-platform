import pandas as pd

from src.quality.data_quality import (
    validate_not_empty,
)


def test_validate_not_empty():
    df = pd.DataFrame({
        "id": [1, 2, 3]
    })

    assert validate_not_empty(df) is True