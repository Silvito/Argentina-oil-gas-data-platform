PRODUCTION_TOOL_DEFINITION = {
    "type": "function",
    "function": {
        "name": "get_well_production",
        "description": (
            "Obtiene la producción mensual de un pozo "
            "de petróleo, gas y agua."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "well_id": {
                    "type": "integer",
                    "description": "Identificador único del pozo.",
                },
                "year": {
                    "type": "integer",
                    "description": "Año del período de producción.",
                },
                "month": {
                    "type": "integer",
                    "description": "Mes del período de producción.",
                },
            },
            "required": [
                "well_id",
                "year",
                "month",
            ],
            "additionalProperties": False,
        },
    },
}