from src.ai.tools.registry import get_tool


class Agent:

    def __init__(self, llm):
        self.llm = llm

    def run(self, user_message: str):

        tool_call = self.llm.generate_tool_call(
            user_message
        )

        tool_name = tool_call["tool"]
        arguments = tool_call["arguments"]

        tool = get_tool(tool_name)

        result = tool(**arguments)

        return result