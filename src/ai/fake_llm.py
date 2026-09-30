import re


class FakeLLM:

    def generate_tool_call(
        self,
        user_message: str,
    ) -> dict:

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
            "tool": "get_well_production",
            "arguments": {
                "well_id": well_id,
                "year": year,
                "month": month,
            },
        }