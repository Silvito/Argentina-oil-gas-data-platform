from src.ai.tools.production_tool import get_well_production


def test_get_well_production():

    result = get_well_production(
        well_id=28963,
        year=2026,
        month=8,
    )

    assert result.well_id == 28963
    assert result.year == 2026
    assert result.month == 8
    assert result.oil_m3 == 20.75
    assert result.gas_m3 == 1.91
    assert result.water_m3 == -0.99


def test_well_not_found():

    try:
        get_well_production(
            well_id=999999999,
            year=2026,
            month=8,
        )

        assert False

    except ValueError as error:
        assert "No se encontró producción" in str(error)


def test_period_not_found():

    try:
        get_well_production(
            well_id=28963,
            year=2026,
            month=12,
        )

        assert False

    except ValueError as error:
        assert "No se encontró producción" in str(error)