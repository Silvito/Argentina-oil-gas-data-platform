from src.ai.tools.production_tool import get_well_production


TOOLS = {
    "get_well_production": get_well_production,
}


def get_tool(name: str):
    try:
        return TOOLS[name]
    except KeyError:
        raise ValueError(
            f"Herramienta no disponible: {name}"
        )