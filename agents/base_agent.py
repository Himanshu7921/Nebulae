from abc import ABC, abstractmethod
import logging
from typing import Any, Callable, List, Optional, Dict

class Color:
    """ANSI color codes for styled console output."""
    HEADER: str = '\033[95m'
    BLUE: str = '\033[94m'
    CYAN: str = '\033[96m'
    GREEN: str = '\033[92m'
    YELLOW: str = '\033[93m'
    RED: str = '\033[91m'
    BOLD: str = '\033[1m'
    END: str = '\033[0m'

# Logger setup (safe: don't add duplicate handlers on repeated imports)
logger = logging.getLogger("AgentLogger")
if not logger.handlers:
    logger.setLevel(logging.INFO)
    console_handler = logging.StreamHandler()
    formatter = logging.Formatter("%(message)s")  # Simple output format
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)


class BaseAgent(ABC):
    """
    Abstract base class for AI agents.

    This class provides a common structure for all agents, including
    attributes for agent identity, LLM, tools, memory, and RAG usage.
    It also handles logging of agent initialization details.

    Attributes:
        agent_name (str): Name of the agent.
        agent_description (str): Brief description of the agent's purpose.
        agent_tools (List[Any]): Tools available to the agent.
        llm (str): Language model used by the agent.
        agent_id (int): Unique identifier for the agent.
        agent_config_dict (Optional[dict]): Optional configuration dictionary.
        agent_memory (Optional[Any]): Optional memory object associated with the agent.
        agent_persona (Optional[str]): Optional persona of the agent.
        agent_prompt (Optional[str]): Optional prompt string for agent behavior.
        verbose (bool): Flag to enable verbose logging.
        logger (Optional[logging.Logger]): Custom logger if provided.
        update_strategy (Optional[Callable]): Optional callable for update strategy.
        agent_role (Optional[str]): Role of the agent.
        rag_enabled (bool): Flag indicating if RAG (Retrieval-Augmented Generation) is enabled.
        vector_store (Optional[str]): Name of the vector store if RAG is enabled.
    """

    def __init__(self, *,
                 agent_name: str,
                 agent_description: str,
                 agent_tools: Optional[List[Any]] = None,
                 llm: str,
                 agent_id: int,
                 agent_config_dict: Optional[Dict] = None,
                 agent_memory: Optional[Any] = None,
                 agent_persona: Optional[str] = None,
                 agent_prompt: Optional[str] = None,
                 verbose: bool = True,
                 logger: Optional[logging.Logger] = None,
                 update_strategy: Optional[Callable] = None,
                 agent_role: Optional[str] = None,
                 rag_enabled: bool = False,
                 vector_store: Optional[str] = None,
                 interactions: Optional[str] = None,
                 show_logger: bool = True):

        """
        Initialize the agent with required attributes.

        Args:
            agent_name (str): Name of the agent.
            agent_description (str): Brief description of the agent.
            agent_tools (Optional[List[Any]]): Tools available to the agent. Defaults to [].
            llm (str): Language model used by the agent.
            agent_id (int): Unique identifier for the agent.
            agent_config_dict (Optional[Dict]): Optional configuration dictionary.
            agent_memory (Optional[Any]): Optional memory object.
            agent_persona (Optional[str]): Optional persona description.
            agent_prompt (Optional[str]): Optional prompt string.
            verbose (bool): Flag for verbose logging. Defaults to True.
            logger (Optional[logging.Logger]): Optional custom logger.
            update_strategy (Optional[Callable]): Optional callable for update strategy.
            agent_role (Optional[str]): Role of the agent. Defaults to None.
            rag_enabled (bool): Whether Retrieval-Augmented Generation is enabled. Defaults to False.
            vector_store (Optional[str]): Name of the vector store if RAG is enabled.
            interactions (Optional[str]): Defines other agents this agent communicates or collaborates with.
        """

        self.llm: str = llm
        self.agent_name: str = agent_name
        self.agent_description: str = agent_description
        # Init and normalize config dictionary
        self.agent_id: int = agent_id
        self.agent_config_dict: Dict = dict(agent_config_dict or {})

        # prefer explicit constructor args; fall back to config values
        self.agent_tools: List[Any] = list(agent_tools) if agent_tools is not None else list(self.agent_config_dict.get("tools", []))
        self.agent_memory: Optional[Any] = agent_memory
        self.agent_persona: Optional[str] = agent_persona
        self.agent_prompt: Optional[str] = agent_prompt
        self.verbose: bool = verbose
        self.update_strategy: Optional[Callable] = update_strategy

        # Role and interactions: explicit arg wins, otherwise read from config
        self.agent_role: Optional[str] = agent_role if agent_role is not None else self.agent_config_dict.get("role") or self.agent_config_dict.get("agent_role")
        self.interactions: Optional[str] = interactions if interactions is not None else self.agent_config_dict.get("interactions")

        # RAG and vector store: explicit arg preferred; otherwise read from config.rag or keys
        if rag_enabled is not None and rag_enabled:
            self.rag_enabled: bool = True
        else:
            self.rag_enabled: bool = bool(self.agent_config_dict.get("rag", {}).get("enabled", self.agent_config_dict.get("rag_enabled", False)))
        self.vector_store: Optional[str] = vector_store if vector_store is not None else self.agent_config_dict.get("vector_store") or self.agent_config_dict.get("rag", {}).get("vector_store")

        # agent visibility/behavior
        self.show_logger: bool = show_logger

        # Capabilities and schemas come from config (empty list/dict if absent)
        self.capabilities: List[str] = list(self.agent_config_dict.get("capabilities", []))
        self.input_schema = self.agent_config_dict.get("input_schema")
        self.output_schema = self.agent_config_dict.get("output_schema")

        # Final logger resolution (explicit logger -> module-level logger)
        self.logger: logging.Logger = logger if logger is not None else globals().get("logger")

        # Log the agent's initialization details
        if self.show_logger:
            self.log_agent_details()
            print()

    @abstractmethod
    def update_persona(self, persona: str) -> None:
        """Update the agent's persona."""

    @abstractmethod
    def run_agent(self) -> None:
        """Run the agent's main behavior loop."""
        pass

    @abstractmethod
    def update_memory(self) -> None:
        """Update the agent's memory after interactions."""
        pass

    @abstractmethod
    def build_agent(self) -> None:
        """Construct or initialize the agent's internal chain or pipeline."""
        pass

    @abstractmethod
    def get_agent_chain(self) -> Any:
        """Retrieve the agent's processing chain or workflow."""
        pass

    def log_agent_details(self) -> None:
        """
        Log detailed information about the agent.

        Includes agent name, role, ID, LLM, RAG usage, memory, tools, and interactions.
        Provides a visually formatted output using ANSI color codes.
        """
        log = self.logger if self.logger is not None else globals().get("logger")

        # Header
        log.info(Color.CYAN + "------------------------ 🤖 Agent Details ------------------------" + Color.END)

        # Name and role
        log.info(
            f"{Color.BOLD}{self.agent_name}{Color.END} is initialized as {Color.YELLOW}{self.agent_role}{Color.END} role | "
            f"Agent_id = {Color.GREEN}{self.agent_id}{Color.END}"
        )

        # LLM information
        if self.llm:
            log.info(f"Agent LLM: {Color.BLUE}{self.llm}{Color.END}")

        # RAG information
        if self.rag_enabled:
            rag_line = f"This agent will use {Color.BLUE}RAG Technology{Color.END}"
            if self.vector_store:
                rag_line += f" | Vector Store: {Color.GREEN}{self.vector_store}{Color.END}"
            log.info(rag_line)

        # Memory information
        if self.agent_memory:
            log.info(f"This agent will also use Memory associated to {Color.YELLOW}{self.agent_memory}{Color.END}")

        # Tools information
        if self.agent_tools:
            tools_list = ", ".join(str(tool) for tool in self.agent_tools)
            log.info(f"Tools available for this agent: {Color.GREEN}{tools_list}{Color.END}")

        # Interactions information
        if self.interactions:
            log.info(f"Interacts with other agents: {Color.CYAN}{self.interactions}{Color.END}")

        # Footer
        log.info(Color.CYAN + "------------------------------------------------------------------" + Color.END)
    
    def can_handle(self, task: Dict) -> bool:
        """
        Cheap capability check: returns True if task.task_type is in self.capabilities.
        This is intentionally lightweight; use validate_input() for stricter checks.
        """
        if not isinstance(task, dict):
            return False
        task_type = task.get("task_type")
        return bool(task_type and task_type in self.capabilities)
    
    @abstractmethod
    def execute_task(self, task: Dict) -> Dict:
        """
        Execute the provided task and return a result dict.
        Concrete agents must implement this entrypoint used by the Planner.
        """
        raise NotImplementedError

    def validate_input(self, payload: Dict) -> bool:
        """
        Validate payload against input_schema using jsonschema.
        - Returns True if no schema is defined or if validation passes.
        - Returns False and logs a warning if validation fails.
        """
        if not self.input_schema:
            return True
        try:
            import jsonschema  # optional dependency
            jsonschema.validate(instance=payload, schema=self.input_schema)
            return True
        except Exception as e:
            log = self.logger or globals().get("logger")
            if log:
                log.warning(f"[{self.agent_name}] input validation failed: {e}")
            return False

if __name__ == "__main__":
    # Concrete implementations of BaseAgent (subclasses)
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
        def execute_task(self):
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
        def execute_task(self):
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
        def execute_task(self):
            pass

    # Initialize agents with interactions
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
        show_logger = False
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
        show_logger = False
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
        interactions="HelperBot, ResearchBot"
    )