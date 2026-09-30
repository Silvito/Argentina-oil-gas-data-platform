from src.ai.tools.production_tool import get_well_production
from src.ai.tools.history_tool import get_well_history


TOOLS = {
    "get_well_production": get_well_production,
    "get_well_history": get_well_history,
}


def get_tool(name: str):
    try:
        return TOOLS[name]
    except KeyError:
        raise ValueError(
            f"Herramienta no disponible: {name}"
        )