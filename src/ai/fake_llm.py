import re


class FakeLLM:

    def generate(
        self,
        messages: list[dict],
    ) -> dict:

        last_message = messages[-1]

        # Primera interacción: interpretar la pregunta
        if last_message["role"] == "user":

            user_message = last_message["content"]

            match = re.search(
                r"pozo\s+(\d+).*?(\d{4}).*?(?:mes|mes de)\s+(\d+)",
                user_message.lower(),
            )

            if not match:
                raise ValueError(
                    "FakeLLM no pudo interpretar la consulta."
                )

            well_id = int(match.group(1))
            year = int(match.group(2))
            month = int(match.group(3))

            return {
                "type": "tool_call",
                "tool": "get_well_production",
                "arguments": {
                    "well_id": well_id,
                    "year": year,
                    "month": month,
                },
            }

        # Segunda interacción: recibir resultado de la herramienta
        if last_message["role"] == "tool":

            result = last_message["content"]

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