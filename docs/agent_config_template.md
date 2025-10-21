# Agent Configuration Template

This document defines a complete and detailed `agent_config_dict` for agents in the Nebulae system. It explains every supported key, recommended types and values, advanced options, security notes, and examples you can copy into your agents.

`agent_config_dict` is a plain Python dict (or JSON object) passed at agent construction via the `agent_config_dict` parameter. The runtime will normalize useful fields into instance attributes (for example, `self.capabilities`, `self.input_schema`, `self.output_schema`, `self.defaults`). Constructor arguments (like `agent_name`) still take precedence over config values for backwards compatibility.

---

## Canonical template

Copy this template as a starting point and edit fields to match an agent's behavior.

```python
agent_config = {
    # REQUIRED: list of capability identifiers the agent exposes. Use stable, descriptive
    # strings (verb_noun) such as "retrieve_documents", "summarize_text".
    "capabilities": ["retrieve_documents", "summarize_text"],

    # RECOMMENDED: JSON Schema (Draft-07) describing the expected input payload for tasks
    # this agent can execute. Planner uses this to validate payloads before dispatch.
    "input_schema": {"type": "object", "properties": {}, "required": []},

    # RECOMMENDED: JSON Schema describing the output the agent returns from execute_task.
    "output_schema": {"type": "object", "properties": {}, "required": []},

    # OPTIONAL: prompt template(s) for LLM-driven agents. Can be a string or a dict of
    # named templates for multi-step flows, e.g. {"summarize": "...", "extract": "..."}
    "prompt_template": "Summarize the documents: {documents}",

    # OPTIONAL: list of tool identifiers required by this agent (resolved by runtime)
    "tools": ["web_search", "calculator"],

    # OPTIONAL: default parameter values used when a task payload omits optional fields
    "defaults": {"summary_length": "short", "max_results": 10},

    # OPTIONAL human-readable metadata
    "description": "Retrieves and summarizes documents for research tasks.",
    "version": "0.1.0",

    # OPTIONAL runtime controls
    "timeout_seconds": 30,
    "retry_on_failure": True,
    "retry_policy": {"max_retries": 2, "backoff": "exponential", "base_seconds": 1},

    # OPTIONAL planner/orchestrator hints
    "priority": 50,
    "preferred_hosts": [],

    # OPTIONAL security hints (do not store secrets here; store references to vault)
    "auth_required": False,
    "allowed_api_keys": [],

    # OPTIONAL RAG settings
    "rag": {"enabled": False, "vector_store": "pinecone", "embedding_model": "text-embedding-3-small"},

    # OPTIONAL LLM/model parameters
    "model_settings": {"llm_name": "gpt-4o", "temperature": 0.2, "max_tokens": 1024},

    # OPTIONAL operational controls
    "concurrency": 1,
    "rate_limit": {"requests_per_minute": 60},
    "health_check": {"type": "ping", "interval_seconds": 60},

    # OPTIONAL telemetry/observability
    "telemetry": {"enabled": True, "metrics_prefix": "agent"},

    # OPTIONAL adapters for transforming outputs to other agent input shapes
    "adapters": {"to_summarizer": "adapters/research_to_summarizer.py"},

    # OPTIONAL free-form tags and contact info
    "tags": ["research", "critical"],
    "maintainer": {"name": "team@example.com", "slack": "#research"},

    # OPTIONAL legacy/compat fields
    "legacy": {}
}
```

---

## Detailed key explanations and examples

Each key below includes: purpose, expected type, runtime behavior, and best-practice examples.

### capabilities (REQUIRED)
- Type: list[str]
- Purpose: Primary discovery mechanism for the Planner. Use concise, stable verbs: e.g. `"retrieve_documents"`, `"summarize_text"`, `"analyze_data"`.
- Runtime: Planner performs a cheap string match to find candidate agents before more expensive validation.
- Example: `"capabilities": ["summarize_text"]`

### input_schema (RECOMMENDED)
- Type: JSON Schema dict (Draft-07 recommended)
- Purpose: Validate task payloads before dispatch. Prevents runtime errors when an agent receives unexpected fields.
- Runtime: `BaseAgent.validate_input(payload)` should call `jsonschema.validate(instance=payload, schema=self.input_schema)` and return True/False.
- Example:
```json
{"type":"object","required":["documents"],"properties":{"documents":{"type":"array"}}}
```

### output_schema (RECOMMENDED)
- Type: JSON Schema dict
- Purpose: Validate outputs returned by `execute_task`. The Planner or orchestrator should check outputs before passing them to dependent tasks.
- Example: `{"type":"object","required":["summary"],"properties":{"summary":{"type":"string"}}}`

### prompt_template (OPTIONAL)
- Type: str or dict
- Purpose: Templates for LLM prompts. Use placeholders that the agent code knows to replace (e.g., `{documents}`, `{context}`). Keep templates concise and add a `version` when changing.
- Example: `"prompt_template": "Summarize the following documents: {documents}"`

### tools (OPTIONAL)
- Type: list[str]
- Purpose: Names of runtime tools that the agent calls (e.g., `web_search`, `pdf_parser`). The orchestrator should map names to implementations.
- Example: `"tools": ["paper_search","reference_manager"]`

### defaults (OPTIONAL)
- Type: dict
- Purpose: Default values for optional task parameters. Planner should merge task payloads with these defaults when preparing the final payload.
- Example: `"defaults": {"summary_length": "short"}`

### description, version
- Type: str
- Purpose: Human metadata. Use semantic versioning for `version` to track changes.

### timeout_seconds, retry_on_failure, retry_policy
- Type: number / bool / dict
- Purpose: Operational controls. `retry_policy` may include `max_retries`, `backoff` (e.g., `"linear"` or `"exponential"`), and `base_seconds` for backoff.

### priority, preferred_hosts
- Type: int / list
- Purpose: Planner selection hints. Higher `priority` biases selection; `preferred_hosts` allows affinity (e.g., for GPU-bound agents).

### auth_required, allowed_api_keys
- Type: bool / list
- Purpose: Security hints. Do not store raw secrets in the config. Use references to a secure vault.

### rag
- Type: dict
- Purpose: Flags and parameters if the agent uses Retrieval-Augmented Generation (RAG). Include `enabled`, `vector_store`, and `embedding_model`.

### model_settings
- Type: dict
- Purpose: LLM configuration (model name, temperature, max tokens). Agents should merge these settings with runtime overrides.

### concurrency, rate_limit, health_check
- Type: int / dict
- Purpose: Controls for parallelism, throttling, and health monitoring.

### telemetry
- Type: dict
- Purpose: Toggle metrics/tracing and provide naming prefixes for observability.

### adapters
- Type: dict
- Purpose: Paths or identifiers for code that transforms this agent's outputs into shapes expected by other agents. Use to decouple tightly-coupled agents.

### tags, maintainer
- Type: list / dict
- Purpose: Free-form metadata and contact information for on-call and discovery.

### legacy
- Type: dict
- Purpose: Backwards compatibility entries you intend to remove later.

---

## Behavior and precedence rules

- Precedence: explicit constructor arguments (e.g., `agent_name`, `agent_tools`, `agent_role`) should override values found in `agent_config_dict`. This preserves backwards compatibility while enabling config-first workflows.
- Normalization: `BaseAgent.__init__` should normalize and set `self.capabilities`, `self.input_schema`, `self.output_schema`, `self.defaults`, `self.rag`, `self.model_settings`, etc., using `agent_config_dict` when explicit arguments are not provided.
- Planner selection flow (recommended):
  1. Filter agents by `capabilities` (cheap string match).
  2. Validate the task payload against the agent's `input_schema` with `jsonschema`.
  3. Score candidates by `priority`, `latency`, `cost`, or other policy.
  4. Dispatch task to chosen agent and validate the returned result against `output_schema`.

---

## Security & secrets

- Never store raw secrets in `agent_config_dict` in source control. Store references (IDs) to secret managers and have runtime resolve them.
- Use `auth_required` and `allowed_api_keys` as metadata flags; the orchestrator must enforce authentication and authorization.

---

## Examples

### Helper agent (full)

```python
helper_config = {
    "capabilities": ["assist", "calculate", "web_search"],
    "input_schema": {
        "type": "object",
        "required": ["query"],
        "properties": {"query": {"type": "string"}, "context": {"type": "string"}}
    },
    "output_schema": {
        "type": "object",
        "required": ["answer"],
        "properties": {"answer": {"type": "string"}, "sources": {"type": "array", "items": {"type": "string"}}}
    },
    "prompt_template": "Answer the user's query succinctly. Use context if provided.",
    "tools": ["calculator", "notepad", "web_search"],
    "defaults": {"answer_format": "concise"},
    "version": "0.1.0",
    "timeout_seconds": 15,
    "retry_on_failure": False,
    "priority": 40
}
```

### Planner agent (full)

```python
planner_config = {
    "capabilities": ["decompose_goal","plan_tasks","select_agent","dispatch_tasks"],
    "input_schema": {"type":"object","required":["goal"],"properties":{"goal":{"type":"string"}}},
    "output_schema": {"type":"object","required":["plan"],"properties":{"plan":{"type":"array"}}},
    "prompt_template": "Decompose the goal into a JSON plan with tasks and dependencies.",
    "tools": ["task_graph_builder","validator"],
    "defaults": {"max_parallel_tasks": 3},
    "version": "0.1.0",
    "priority": 90
}
```