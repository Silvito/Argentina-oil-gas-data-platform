from src.ai.tools.registry import get_tool


class Agent:

    def __init__(self, llm):
        self.llm = llm

    def run(self, user_message: str):

        messages = [
            {
                "role": "user",
                "content": user_message,
            }
        ]

        while True:

            response = self.llm.generate(messages)

            if response["type"] == "final":
                return response["content"]

            if response["type"] != "tool_call":
                raise ValueError(
                    "Respuesta del LLM no soportada."
                )

            tool_name = response["tool"]
            arguments = response["arguments"]

            tool = get_tool(tool_name)

            result = tool(**arguments)

            if isinstance(result, list):
                result_dict = [
                    item.model_dump()
                    for item in result]
            else:
                result_dict = result.model_dump()

            messages.append(
                {
                    "role": "assistant",
                    "content": response,
                }
            )

            messages.append(
                {
                    "role": "tool",
                    "content": result_dict,
                }
            )