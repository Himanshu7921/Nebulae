from typing import List, Dict, Optional, Any
from base_agent import BaseAgent

class PlannerAgent(BaseAgent):
    """
    PlannerAgent: decomposes goals, selects agents and dispatches tasks.
    """

    def __init__(self, *, agent_name: str, agent_description: str, llm: str = "planner-llm",
                 agent_id: int = 0, agent_config_dict: Optional[Dict] = None,
                 registry: Optional[List[BaseAgent]] = None, **kwargs):
        super().__init__(agent_name=agent_name,
                         agent_description=agent_description,
                         llm=llm, agent_id=agent_id,
                         agent_config_dict=agent_config_dict or {}, **kwargs)
        # registry of available agents (populated externally or passed in)
        self.registry: List[BaseAgent] = registry or []

    def build_agent(self) -> None:
        # nothing heavy to build for now; registry should already contain agents
        pass

    def update_persona(self, persona: str) -> None:
        self.agent_persona = persona

    def run_agent(self) -> None:
        # placeholder for a continuous planner loop
        raise NotImplementedError("Use plan_and_execute(goal, registry) for now.")

    def update_memory(self) -> None:
        pass

    def get_agent_chain(self) -> Any:
        return None

    def decompose_goal(self, goal: str) -> List[Dict]:
        """
        Convert a textual goal into a list of task dicts.
        For initial implementation keep tasks explicit or rule-based.
        Each task: {task_id, task_type, payload, dependencies: [], priority}
        """
        # Simple example: a single summarize_text task
        # Real implementation: use LLM or rules to decompose
        return [{"task_id": "t1", "task_type": "summarize_text",
                 "payload": {"documents": [], "summary_length": "short"},
                 "dependencies": [], "priority": 50}]

    def select_agent_for_task(self, task: Dict) -> Optional[BaseAgent]:
        # Step 1: capability filter
        candidates = [a for a in self.registry if a.can_handle(task)]
        if not candidates:
            return None
        # Step 2: payload validation
        payload = task.get("payload", {})
        valid_candidates = [a for a in candidates if a.validate_input(payload)]
        if not valid_candidates:
            return None
        # Step 3: pick by simple policy (first valid). Replace with scoring later.
        return valid_candidates[0]

    def dispatch_task(self, agent: BaseAgent, task: Dict) -> Dict:
        """
        Call a standard agent method to execute the task.
        Agents should implement `handle_task(task)` or similar.
        Here we expect agents to expose `run_task(task)` returning a dict result.
        """
        # best if you define a stable agent.execute_task(task) contract in BaseAgent.
        if hasattr(agent, "execute_task"):
            result = agent.execute_task(task)  # implement on agent classes
        elif hasattr(agent, "run_task"):
            result = agent.run_task(task.get("payload", {}))
        else:
            raise RuntimeError(f"Agent {agent.agent_name} has no execution entrypoint.")
        # validate output if agent has schema
        if getattr(agent, "output_schema", None):
            try:
                import jsonschema
                jsonschema.validate(instance=result, schema=agent.output_schema)
            except Exception as e:
                # let caller handle failure (you can implement retries)
                raise RuntimeError(f"Output validation failed: {e}")
        return result

    def plan_and_execute(self, goal: str) -> Dict:
        tasks = self.decompose_goal(goal)
        results = {}
        for task in tasks:
            agent = self.select_agent_for_task(task)
            if not agent:
                raise RuntimeError(f"No agent available to handle task {task['task_id']}")
            res = self.dispatch_task(agent, task)
            results[task["task_id"]] = res
        return results
    
    def execute_task(self, task):
        return "Executing Task.."
# ...existing code...


if __name__ == "__main__":
    class MyAgent(BaseAgent):
        """Example agent subclass implementing BaseAgent."""
        def update_persona(self, persona: str) -> None: 
            pass
        def run_agent(self) -> None: 
            pass
        def update_memory(self) -> None: 
            pass
        def build_agent(self) -> None: 
            pass
        def get_agent_chain(self) -> Any: 
            pass
        def execute_task(self, task):
            pass

    class ResearchAgent(BaseAgent):
        """Research-focused agent subclass implementing BaseAgent."""
        def update_persona(self, persona: str) -> None:
            pass
        def run_agent(self) -> None:
            pass
        def update_memory(self) -> None:
            pass
        def build_agent(self) -> None:
            pass
        def get_agent_chain(self) -> Any:
            pass
        def execute_task(self, task):
            pass

    class SecurityAgent(BaseAgent):
        """Security monitoring agent subclass implementing BaseAgent."""
        def update_persona(self, persona: str) -> None:
            pass
        def run_agent(self) -> None:
            pass
        def update_memory(self) -> None:
            pass
        def build_agent(self) -> None:
            pass
        def get_agent_chain(self) -> Any:
            pass
        def execute_task(self, task):
            pass

    helper_config = {
        "capabilities": ["assist", "calculate", "web_search"],
        "input_schema": {
            "type": "object",
            "required": ["query"],
            "properties": {
                "query": {"type": "string"},
                "context": {"type": "string"}
            }
        },
        "output_schema": {
            "type": "object",
            "required": ["answer"],
            "properties": {
                "answer": {"type": "string"},
                "sources": {"type": "array", "items": {"type": "string"}}
            }
        },
        "prompt_template": "Answer the user's query succinctly. Use context if provided.",
        "tools": ["calculator", "notepad", "web_search"],
        "defaults": {"answer_format": "concise"},
        "version": "0.1.0"
    }

    research_config = {
        "capabilities": ["retrieve_documents", "summarize_text", "extract_references"],
        "input_schema": {
            "type": "object",
            "required": ["query"],
            "properties": {
                "query": {"type": "string"},
                "filters": {
                    "type": "object",
                    "properties": {
                        "year_range": {"type": "array", "items": {"type": "integer"}, "minItems": 2, "maxItems": 2},
                        "source_types": {"type": "array", "items": {"type": "string"}}
                    }
                },
                "max_results": {"type": "integer", "minimum": 1}
            }
        },
        "output_schema": {
            "type": "object",
            "required": ["documents"],
            "properties": {
                "documents": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "required": ["id", "title", "text"],
                        "properties": {
                            "id": {"type": "string"},
                            "title": {"type": "string"},
                            "text": {"type": "string"},
                            "source": {"type": "string"}
                        }
                    }
                },
                "metadata": {"type": "object"}
            }
        },
        "prompt_template": "Search and return relevant documents for the query.",
        "tools": ["paper_search", "summarizer", "reference_manager"],
        "defaults": {"max_results": 10},
        "version": "0.1.0"
    }

    security_config = {
        "capabilities": ["scan_logs", "analyze_incident", "raise_alert"],
        "input_schema": {
            "type": "object",
            "required": ["logs"],
            "properties": {
                "logs": {"type": "array", "items": {"type": "string"}},
                "time_range": {
                    "type": "object",
                    "properties": {
                        "start": {"type": "string", "format": "date-time"},
                        "end": {"type": "string", "format": "date-time"}
                    }
                },
                "severity_threshold": {"type": "string", "enum": ["low", "medium", "high"]}
            }
        },
        "output_schema": {
            "type": "object",
            "required": ["findings"],
            "properties": {
                "findings": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "id": {"type": "string"},
                            "description": {"type": "string"},
                            "severity": {"type": "string"}
                        }
                    }
                },
                "summary": {"type": "string"}
            }
        },
        "prompt_template": "Analyze logs and surface incidents above the severity threshold.",
        "tools": ["log_parser", "intrusion_detector", "alert_system"],
        "version": "0.1.0"
    }

    agent1 = MyAgent(
        agent_name="HelperBot",
        llm="Google Gemini",
        agent_description="A friendly assistant",
        agent_tools=["calculator", "notepad", "web_search"],
        agent_id=101,
        agent_role="math tutor",
        rag_enabled=True,
        vector_store="FAISS",
        agent_memory="MySQLMemory()",
        interactions="ResearchBot, SecureBot",
        agent_config_dict=helper_config,
        show_logger=False
    )

    agent2 = ResearchAgent(
        agent_name="ResearchBot",
        llm="GPT-4",
        agent_description="Research assistant for academic queries",
        agent_tools=["paper_search", "summarizer", "reference_manager"],
        agent_id=102,
        agent_role="research assistant",
        rag_enabled=True,
        vector_store="Pinecone",
        agent_memory="PostgresMemory()",
        interactions="HelperBot, SecureBot",
        agent_config_dict=research_config,
        show_logger=False
    )

    agent3 = SecurityAgent(
        agent_name="SecureBot",
        llm="Claude 2",
        agent_description="Monitors system and network security",
        agent_tools=["log_parser", "intrusion_detector", "alert_system"],
        agent_id=103,
        agent_role="security monitor",
        rag_enabled=False,
        vector_store=None,
        agent_memory=None,
        interactions="HelperBot, ResearchBot",
        agent_config_dict=security_config,
        show_logger=False
    )


    planner_config = {
        "capabilities": [
            "decompose_goal",
            "plan_tasks",
            "select_agent",
            "dispatch_tasks",
            "simulate_plan",
            "validate_plan"
        ],
        "input_schema": {
            "type": "object",
            "required": ["goal"],
            "properties": {
                "goal": {"type": "string"},
                "constraints": {
                    "type": "object",
                    "properties": {
                        "deadline": {"type": "string", "format": "date-time"},
                        "budget": {"type": "number"},
                        "must_use_agents": {"type": "array", "items": {"type": "string"}}
                    }
                },
                "desired_output_format": {"type": "string"},
                "priority": {"type": "integer"}
            }
        },
        "output_schema": {
            "type": "object",
            "required": ["plan"],
            "properties": {
                "plan": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "required": ["task_id", "task_type", "payload"],
                        "properties": {
                            "task_id": {"type": "string"},
                            "task_type": {"type": "string"},
                            "payload": {"type": "object"},
                            "dependencies": {"type": "array", "items": {"type": "string"}},
                            "priority": {"type": "integer"},
                            "estimated_cost": {"type": "number"},
                            "preferred_agents": {"type": "array", "items": {"type": "string"}}
                        }
                    }
                },
                "metadata": {"type": "object"}
            }
        },
        "prompt_template": (
            "You are a Planner that decomposes a user goal into a sequence of tasks. "
            "Return a JSON plan with tasks, dependencies, priorities and payloads. "
            "Respect constraints and preferred agents."
        ),
        "tools": ["task_graph_builder", "simulator", "validator"],
        "defaults": {"max_parallel_tasks": 3, "retry_on_failure": True},
        "version": "0.1.0"
    }

    # Example usage
    planner_agent = PlannerAgent(
        agent_name="Planner Agent",
        agent_description="Responsible for goal decomposition and task orchestration",
        llm="Planner-LLM",
        agent_id=1,
        agent_config_dict = planner_config,
        registry=[agent1, agent2, agent3]  # existing agents
    )
    
    tasks = planner_agent.decompose_goal(goal="Summarize recent papers about retrieval-augmented generation")
    for task in tasks:
        agent = planner_agent.select_agent_for_task(task)
        if not agent:
            print(f"No available agent for task {task.get('task_id')}, task_type={task.get('task_type')}")
            continue
        try:
            result = planner_agent.dispatch_task(agent, task)
            print(f"Task {task['task_id']} handled by {agent.agent_name}: {result}")
        except Exception as e:
            print(f"Error executing task {task['task_id']} with agent {agent.agent_name}: {e}")