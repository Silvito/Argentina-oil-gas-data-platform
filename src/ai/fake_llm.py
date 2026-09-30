import re


class FakeLLM:

    def generate(
        self,
        messages: list[dict],
    ) -> dict:

        last_message = messages[-1]

        # Primera interacción: interpretar la pregunta
        if last_message["role"] == "user":

            user_message = last_message["content"].lower()

            # Consulta histórica
            history_match = re.search(
                r"historial.*?pozo\s+(\d+).*?(\d{4})",
                user_message,
            )

            if history_match:

                well_id = int(history_match.group(1))
                year = int(history_match.group(2))

                return {
                    "type": "tool_call",
                    "tool": "get_well_history",
                    "arguments": {
                        "well_id": well_id,
                        "year": year,
                    },
                }

            # Consulta mensual
            monthly_match = re.search(
                r"pozo\s+(\d+).*?(\d{4}).*?(?:mes|mes de)\s+(\d+)",
                user_message,
            )

            if monthly_match:

                well_id = int(monthly_match.group(1))
                year = int(monthly_match.group(2))
                month = int(monthly_match.group(3))

                return {
                    "type": "tool_call",
                    "tool": "get_well_production",
                    "arguments": {
                        "well_id": well_id,
                        "year": year,
                        "month": month,
                    },
                }

            raise ValueError(
                "FakeLLM no pudo interpretar la consulta."
            )

        # Segunda interacción: recibir resultado de la herramienta
        if last_message["role"] == "tool":

            result = last_message["content"]

            # Resultado de historial
            if isinstance(result, list):

                return {
                    "type": "final",
                    "content": (
                        f"Se encontraron {len(result)} "
                        f"registros mensuales de producción "
                        f"para el pozo {result[0]['well_id']} "
                        f"durante {result[0]['year']}."
                    ),
                }

            # Resultado mensual
            return {
                "type": "final",
                "content": (
                    f"El pozo {result['well_id']} produjo "
                    f"{result['oil_m3']} m3 de petróleo, "
                    f"{result['gas_m3']} m3 de gas y "
                    f"{result['water_m3']} m3 de agua "
                    f"en {result['year']}-{result['month']:02d}."
                ),
            }

        raise ValueError(
            "FakeLLM recibió un tipo de mensaje no soportado."
        )