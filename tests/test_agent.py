from src.ai.agent import Agent
from src.ai.fake_llm import FakeLLM


def test_agent_get_well_production():

    agent = Agent(FakeLLM())

    result = agent.run(
        "Cuanto produjo el pozo 28963 en 2026 mes 8?"
    )

    assert "El pozo 28963 produjo" in result
    assert "20.75 m3 de petróleo" in result
    assert "1.91 m3 de gas" in result
    assert "-0.99 m3 de agua" in result


class FakeLLMInvalidTool:

    def generate(
        self,
        messages: list[dict],
    ) -> dict:

        return {
            "type": "tool_call",
            "tool": "non_existing_tool",
            "arguments": {},
        }


def test_agent_invalid_tool():

    agent = Agent(FakeLLMInvalidTool())

    try:
        agent.run("consulta")
        assert False

    except ValueError as error:
        assert "Herramienta no disponible" in str(error)