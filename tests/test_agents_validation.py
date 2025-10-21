import pytest

from agents.summarizer_agent import SummarizerAgent
from agents.research_agent import ResearchAgent


def make_doc(i: int):
    return {"id": f"d{i}", "title": f"Doc {i}", "text": f"This is the content of document {i}."}


def test_summarizer_validate_and_execute():
    # load summarizer config from settings via config file assumptions
    cfg = {
        "capabilities": ["summarize_text"],
        "input_schema": {
            "type": "object",
            "required": ["documents"],
            "properties": {
                "documents": {"type": "array"}
            }
        },
        "output_schema": {
            "type": "object",
            "required": ["summary"],
            "properties": {"summary": {"type": "string"}}
        }
    }

    agent = SummarizerAgent(agent_name="Summ", llm="test", agent_description="", agent_id=1, agent_config_dict=cfg, show_logger=False)

    docs = [make_doc(1), make_doc(2)]
    task = {"task_id": "t1", "task_type": "summarize_text", "payload": {"documents": docs}}

    # validate_input should pass
    assert agent.validate_input(task["payload"]) is True

    # execution returns expected keys
    res = agent.execute_task(task)
    assert "summary" in res
    assert isinstance(res["summary"], str)


def test_research_and_summarize_integration():
    research_cfg = {
        "capabilities": ["retrieve_documents"],
        "input_schema": {
            "type": "object",
            "required": ["mode"],
            "properties": {"mode": {"type": "string"}, "documents": {"type": "array"}}
        },
        "output_schema": {"type": "object", "required": ["documents"], "properties": {"documents": {"type": "array"}}}
    }

    res_agent = ResearchAgent(agent_name="Res", llm="test", agent_description="", agent_id=2, agent_config_dict=research_cfg, show_logger=False)
    summarizer_cfg = {
        "capabilities": ["summarize_text"],
        "input_schema": {
            "type": "object",
            "required": ["documents"],
            "properties": {"documents": {"type": "array"}}
        },
        "output_schema": {"type": "object", "required": ["summary"], "properties": {"summary": {"type": "string"}}}
    }

    sum_agent = SummarizerAgent(agent_name="Summ", llm="test", agent_description="", agent_id=3, agent_config_dict=summarizer_cfg, show_logger=False)

    # Provide documents directly
    payload = {"mode": "documents", "documents": [make_doc(1), make_doc(2)]}
    task = {"task_id": "t-docs", "task_type": "retrieve_documents", "payload": payload}

    out = res_agent.execute_task(task)
    assert "documents" in out and isinstance(out["documents"], list)

    # Now summarize retrieved docs
    sum_task = {"task_id": "t-sum", "task_type": "summarize_text", "payload": {"documents": out["documents"]}}
    res = sum_agent.execute_task(sum_task)
    assert "summary" in res
