from typing import Dict, Any
from .base_agent import BaseAgent


class ResearchAgent(BaseAgent):
    """Minimal ResearchAgent used for tests and local orchestration.

    Supports two modes matching the research_agent.json schema:
    - mode == 'documents' : accepts provided documents and returns them
    - mode == 'query'     : simulates a retrieval by returning a small list
    """

    def __init__(self, *args, agent_config_dict: Dict = None, **kwargs):
        super().__init__(*args, agent_config_dict=agent_config_dict or {}, **kwargs)

    def execute_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        payload = task.get("payload", {})
        if not self.validate_input(payload):
            raise ValueError("Invalid payload for ResearchAgent")

        mode = payload.get("mode")
        if mode == "documents":
            docs = payload.get("documents", [])
            # Ensure each document has id/title/text
            normalized = []
            for i, d in enumerate(docs):
                normalized.append({
                    "id": d.get("id", f"doc-{i}"),
                    "title": d.get("title", d.get("id", f"doc-{i}")),
                    "text": d.get("text", ""),
                    "source": d.get("source")
                })
            return {"documents": normalized, "metadata": {"retrieval_mode": "provided"}}

        # simulate query retrieval
        query = payload.get("query", "")
        simulated = [
            {"id": "sim-1", "title": f"Result for: {query}", "text": f"Simulated content for query '{query}'", "source": "simulator"}
        ]
        return {"documents": simulated, "metadata": {"query": query}}

    def update_persona(self, persona: str) -> None:
        self.agent_persona = persona

    def run_agent(self) -> None:
        return None

    def update_memory(self) -> None:
        return None

    def build_agent(self) -> None:
        return None

    def get_agent_chain(self):
        return None
