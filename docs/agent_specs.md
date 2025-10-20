# Nebulae – Agent Specifications

**Version:** Draft 0.1  
**Author:** Himanshu Singh  
**Last Updated:** October 2025  

---

## 1. Overview

This document defines the internal specifications for each agent within the **Nebulae** ecosystem — outlining their **purpose**, **inputs**, **outputs**, and **interaction logic**.

Each agent follows a standardized structure for interoperability and orchestration consistency.

---

## 2. Agent Specification Template

| Field | Description |
|-------|--------------|
| **Name** | Agent identifier |
| **Objective** | Core task or function |
| **Inputs** | Data or context received |
| **Outputs** | Expected structured result |
| **Techniques Used** | Algorithms, frameworks, or methods |
| **Interactions** | Other agents it communicates with |
| **Status** | Planned / In Progress / Complete |

---

## 3. Defined Agents

### 3.1 Planner Agent
| Field | Details |
|-------|----------|
| **Objective** | Decompose user goals into structured tasks and assign them to agents. |
| **Inputs** | User research goal or analytical objective. |
| **Outputs** | Task graph with dependency order and execution plan. |
| **Techniques Used** | Task Scheduling, Dependency Graph Analysis |
| **Interactions** | Research Agent, Summarizer Agent, Data Analysis Agent |
| **Status** | Planned |
| **Capabilities** | plan_decomposition, task_assignment, dependency_resolution |
| **Input Schema** | {"type": "object", "properties": {"goal": {"type": "string"}, "constraints": {"type": "object"}}, "required": ["goal"]} |
| **Output Schema** | {"type": "object", "properties": {"tasks": {"type": "array"}, "dependencies": {"type": "array"}}, "required": ["tasks"]} |

---

### 3.2 Research Agent
| Field | Details |
|-------|----------|
| **Objective** | Retrieve relevant information using the RetrievalMind RAG framework. |
| **Inputs** | Task parameters and research context. |
| **Outputs** | Structured retrieved data and metadata. |
| **Techniques Used** | Retrieval-Augmented Generation, Query Expansion |
| **Interactions** | Summarizer Agent, Data Analysis Agent |
| **Status** | Planned |
| **Capabilities** | retrieve_documents, cite_sources, metadata_extraction |
| **Input Schema** | {"type": "object", "properties": {"query": {"type": "string"}, "filters": {"type": "object"}}, "required": ["query"]} |
| **Output Schema** | {"type": "object", "properties": {"documents": {"type": "array"}, "metadata": {"type": "object"}}, "required": ["documents"]} |

---

### 3.3 Summarizer Agent
| Field | Details |
|-------|----------|
| **Objective** | Compress and synthesize large text blocks into focused summaries. |
| **Inputs** | Retrieved text data. |
| **Outputs** | Concise knowledge snippets for internal use. |
| **Techniques Used** | Prompt Chaining, Context Reduction |
| **Interactions** | Writer Agent, Critic Agent |
| **Status** | Planned |
| **Capabilities** | summarize_text, extract_keypoints, shorten_content |
| **Input Schema** | {"type": "object", "properties": {"documents": {"type": "array"}, "summary_length": {"type": "string"}}, "required": ["documents"]} |
| **Output Schema** | {"type": "object", "properties": {"summary": {"type": "string"}, "highlights": {"type": "array"}}, "required": ["summary"]} |

---

### 3.4 Data Analysis Agent
| Field | Details |
|-------|----------|
| **Objective** | Perform quantitative analysis, generate statistics, and create visualizations. |
| **Inputs** | Structured data or retrieved datasets. |
| **Outputs** | Analytical insights and plots. |
| **Techniques Used** | Pandas, NumPy, Matplotlib |
| **Interactions** | Writer Agent, Critic Agent |
| **Status** | Planned |
| **Capabilities** | analyze_data, generate_plots, compute_statistics |
| **Input Schema** | {"type": "object", "properties": {"data": {"type": "array"}, "analysis_type": {"type": "string"}}, "required": ["data"]} |
| **Output Schema** | {"type": "object", "properties": {"insights": {"type": "array"}, "plots": {"type": "array"}}, "required": ["insights"]} |

---

### 3.5 Writer Agent
| Field | Details |
|-------|----------|
| **Objective** | Generate structured research papers and analytical reports. |
| **Inputs** | Summarized findings, analytical results, and context. |
| **Outputs** | Formatted research report (Markdown / PDF). |
| **Techniques Used** | Structured Generation, Reflection |
| **Interactions** | Critic Agent, Reviewer Agent |
| **Status** | Planned |
| **Capabilities** | generate_report, format_markdown, export_pdf |
| **Input Schema** | {"type": "object", "properties": {"sections": {"type": "array"}, "style": {"type": "string"}}, "required": ["sections"]} |
| **Output Schema** | {"type": "object", "properties": {"report_markdown": {"type": "string"}, "report_pdf": {"type": ["string", "null"]}}, "required": ["report_markdown"]} |

---

### 3.6 Critic Agent
| Field | Details |
|-------|----------|
| **Objective** | Evaluate and refine outputs for factual accuracy and coherence. |
| **Inputs** | Generated reports or insights. |
| **Outputs** | Reviewed and corrected content. |
| **Techniques Used** | Self-Reflection, Validation Heuristics |
| **Interactions** | Writer Agent, Memory Agent |
| **Status** | Planned |
| **Capabilities** | review_content, fact_check, propose_revisions |
| **Input Schema** | {"type": "object", "properties": {"content": {"type": "string"}, "context": {"type": "object"}}, "required": ["content"]} |
| **Output Schema** | {"type": "object", "properties": {"revisions": {"type": "array"}, "score": {"type": "number"}}, "required": ["revisions"]} |

---

### 3.7 Memory Agent
| Field | Details |
|-------|----------|
| **Objective** | Maintain contextual memory and past research knowledge. |
| **Inputs** | Agent states, user feedback, project data. |
| **Outputs** | Memory embeddings and historical records. |
| **Techniques Used** | Vector Storage, JSON/SQLite Persistence |
| **Interactions** | All agents |
| **Status** | Planned |
| **Capabilities** | store_memory, retrieve_memory, summarize_history |
| **Input Schema** | {"type": "object", "properties": {"event": {"type": "object"}, "metadata": {"type": "object"}}, "required": ["event"]} |
| **Output Schema** | {"type": "object", "properties": {"embedding_id": {"type": "string"}, "record": {"type": "object"}}, "required": ["embedding_id"]} |

---

### 3.8 Reviewer Agent
| Field | Details |
|-------|----------|
| **Objective** | Process user feedback and suggest iterative improvements. |
| **Inputs** | Human or system-generated review data. |
| **Outputs** | Adjusted agent parameters or updated insights. |
| **Techniques Used** | Feedback Loop Optimization |
| **Interactions** | Memory Agent, Critic Agent |
| **Status** | Planned |
| **Capabilities** | ingest_feedback, prioritize_changes, propose_updates |
| **Input Schema** | {"type": "object", "properties": {"feedback": {"type": "array"}, "source": {"type": "string"}}, "required": ["feedback"]} |
| **Output Schema** | {"type": "object", "properties": {"actions": {"type": "array"}}, "required": ["actions"]} |

---

### 3.9 Knowledge Updater Agent
| Field | Details |
|-------|----------|
| **Objective** | Periodically update internal knowledge and datasets. |
| **Inputs** | Scheduled retrieval instructions or triggers. |
| **Outputs** | Updated local knowledge base. |
| **Techniques Used** | Scheduling, Web Retrieval, Caching |
| **Interactions** | Research Agent, Memory Agent |
| **Status** | Planned |
| **Capabilities** | scheduled_retrieve, refresh_index, cache_invalidate |
| **Input Schema** | {"type": "object", "properties": {"schedule": {"type": "string"}, "targets": {"type": "array"}}, "required": ["targets"]} |
| **Output Schema** | {"type": "object", "properties": {"updated_items": {"type": "array"}}, "required": ["updated_items"]} |

---

## 4. TODO (Documentation Tasks)

- [ ] Finalize communication protocol between agents.  
- [ ] Define response schemas for each agent.  
- [ ] Add implementation references once code modules are complete.  
- [ ] Expand critic-reviewer feedback cycle documentation.

---
