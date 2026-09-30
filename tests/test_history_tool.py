from src.ai.tools.history_tool import get_well_history


def test_get_well_history():

    result = get_well_history(
        well_id=28963,
        year=2026,
    )

    assert len(result) == 8

    assert result[0].month == 1
    assert result[0].oil_m3 == 27.05

    assert result[-1].month == 8
    assert result[-1].oil_m3 == 20.75


def test_well_history_not_found():

    try:
        get_well_history(
            well_id=999999999,
            year=2026,
        )

        assert False

    except ValueError as error:
        assert "No se encontró historial" in str(error)