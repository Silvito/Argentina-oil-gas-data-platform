from typing import Protocol


class LLM(Protocol):

    def generate_tool_call(
        self,
        user_message: str,
    ) -> dict:
        ...