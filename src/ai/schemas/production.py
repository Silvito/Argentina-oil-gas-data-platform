from pydantic import BaseModel


class WellProductionQuery(BaseModel):
    well_id: int
    year: int
    month: int


class WellProductionResult(BaseModel):
    well_id: int
    year: int
    month: int
    oil_m3: float
    gas_m3: float
    water_m3: float