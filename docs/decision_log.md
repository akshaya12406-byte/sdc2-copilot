# Decision Log

## Decision 1
Use Streamlit for UI.

Reason:
Fastest path to a clean public demo.

## Decision 2
Use Prefect for workflow orchestration.

Reason:
Pythonic, testable, and easy to explain.

## Decision 3
Use Polars + DuckDB instead of PySpark.

Reason:
Better fit for CSV-driven prototype, faster local execution, easier deployment.

## Decision 4
Use Great Expectations for validation.

Reason:
Deterministic correctness checks are required for SCD2.

## Decision 5
Use Gemini as primary LLM API.

Reason:
Good runtime path, managed API, suitable for explanation generation.

## Decision 6
Use Groq / OpenRouter as fallback.

Reason:
Provider flexibility and resilience.

## Decision 7
Use Antigravity as development accelerator, not runtime.

Reason:
Best used for scaffolding, parallel coding, verification, and artifacts.

## Decision 8
Do not build a full MCP server in MVP.

Reason:
Too much complexity for the project timeline and not required for core value.