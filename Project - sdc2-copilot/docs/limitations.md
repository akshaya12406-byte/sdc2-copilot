# Limitations

This is a prototype demonstrating SCD2 automation with AI-powered explanations. It is **not** a full enterprise ETL platform.

## Current Limitations

### Data Scale
- Designed for CSV inputs (small-to-medium datasets)
- No distributed processing — single-node Polars execution
- No streaming or real-time ingestion
- Large files (>100MB) may be slow in the Streamlit UI

### Data Formats
- CSV only — no Parquet, JSON, or database connectors in MVP
- Column names must not contain special characters
- Dates must be ISO format (`YYYY-MM-DD`)

### SCD2 Scope
- Type 2 only — no SCD1 (overwrite), SCD3 (separate columns), or SCD6 (hybrid)
- Single business key column (composite keys require manual column selection)
- No surrogate key generation (output uses natural business keys)

### Security & Multi-tenancy
- No authentication or authorization
- No multi-tenant data isolation
- API keys stored in environment variables (not a vault)

### LLM Explanations
- Explanations are summaries only — they do not decide changes
- Quality depends on the LLM provider's response
- If all API providers fail, deterministic template explanations are used
- No explanation caching or history

### Deployment
- Streamlit Community Cloud only — no Kubernetes, no self-managed infra
- No CI/CD pipeline in MVP
- No monitoring or alerting

### Not Included
- No custom MCP server
- No multi-agent orchestration
- No ML-based change detection
- No data lineage tracking
- No writeback to databases
- Production hardening (rate limiting, observability, error recovery) still needed