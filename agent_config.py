# Planner Agent
# Purpose: Decompose user goals into task graphs, assign/select agents, dispatch and validate plans.
# Key capabilities: plan_decomposition, task_assignment, dependency_resolution, simulate_plan, validate_plan
# IO: input = {goal, constraints}, output = {plan: [tasks with payloads, dependencies, metadata]}

# Research Agent
# Purpose: Retrieve relevant documents / evidence (RAG) and return structured documents + metadata.
# Key capabilities: retrieve_documents, cite_sources, metadata_extraction
# IO: input = {query, filters, max_results}, output = {documents: [...], metadata}

# Summarizer Agent
# Purpose: Condense text into summaries and key points for downstream use.
# Key capabilities: summarize_text, extract_keypoints, shorten_content
# IO: input = {documents, summary_length}, output = {summary, highlights, sources}

# Data Analysis Agent
# Purpose: Compute statistics, analyses and generate visualizations from structured data.
# Key capabilities: analyze_data, generate_plots, compute_statistics
# IO: input = {data, analysis_type}, output = {insights, plots}

# Writer Agent
# Purpose: Compose final reports (Markdown/PDF) from summaries, analyses and context.
# Key capabilities: generate_report, format_markdown, export_pdf
# IO: input = {sections, style}, output = {report_markdown, report_pdf}

# Critic Agent
# Purpose: Review and refine outputs for factual accuracy, coherence and quality.
# Key capabilities: review_content, fact_check, propose_revisions
# IO: input = {content, context}, output = {revisions, score}

# Memory Agent
# Purpose: Persist contextual memory, embeddings and historical records for reuse.
# Key capabilities: store_memory, retrieve_memory, summarize_history
# IO: input = {event, metadata}, output = {embedding_id, record}

# Reviewer Agent
# Purpose: Process human/system feedback and propose iterative improvements.
# Key capabilities: ingest_feedback, prioritize_changes, propose_updates
# IO: input = {feedback, source}, output = {actions}

# Knowledge Updater Agent
# Purpose: Scheduled refreshes of indices / knowledge and periodic updates.
# Key capabilities: scheduled_retrieve, refresh_index, cache_invalidate
# IO: input = {schedule, targets}, output = {updated_items}


from sympy import false

agent_config_template = {
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


# Writing the agent_config for Research Agent

## Research Agent:
