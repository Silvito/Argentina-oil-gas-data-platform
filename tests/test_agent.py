from src.ai.agent import Agent
from src.ai.fake_llm import FakeLLM


def test_agent_get_well_production():

    agent = Agent(FakeLLM())

    result = agent.run(
        "Cuanto produjo el pozo 28963 en 2026 mes 8?"
    )

    assert result.well_id == 28963
    assert result.year == 2026
    assert result.month == 8
    assert result.oil_m3 == 20.75
    assert result.gas_m3 == 1.91
    assert result.water_m3 == -0.99


class FakeLLMInvalidTool:

    def generate_tool_call(
        self,
        user_message: str,
    ) -> dict:

        return {
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