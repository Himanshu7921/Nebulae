from typing import Dict, Any
from .base_agent import BaseAgent


class SummarizerAgent(BaseAgent):
    """Minimal SummarizerAgent used for tests and local orchestration.

    This implementation is intentionally small: it validates the incoming
    payload using BaseAgent.validate_input and returns a simulated summary
    that conforms to the example `summarizer_agent.json` output_schema.
    """

    def __init__(self, *args, agent_config_dict: Dict = None, **kwargs):
        super().__init__(*args, agent_config_dict=agent_config_dict or {}, **kwargs)

    def update_persona(self, persona: str) -> None:
        self.agent_persona = persona

    def run_agent(self) -> None:
        # no background loop for the minimal agent
        return None

    def update_memory(self) -> None:
        return None

    def build_agent(self) -> None:
        return None

    def get_agent_chain(self):
        return None

    def execute_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        payload = task.get("payload", {})
        if not self.validate_input(payload):
            raise ValueError("Invalid payload for SummarizerAgent")

        documents = payload.get("documents", [])

        # Basic simulated summary: concat document texts (trimmed)
        combined = "\n\n".join(d.get("text", "") for d in documents)
        summary = (combined[:800] + "...") if len(combined) > 800 else combined

        highlights = [d.get("text", "")[:200] for d in documents][:3]
        sources = [{"id": d.get("id"), "title": d.get("title")} for d in documents]

        return {"summary": summary, "highlights": highlights, "sources": sources}
