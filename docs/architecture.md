# Architecture

## High-Level Flow
Upload source CSV + target SCD2 CSV
→ Detect schema and business key
→ Compare records deterministically
→ Generate updated SCD2 table
→ Run validation checks
→ Produce LLM explanations
→ Display results in Streamlit
→ Save outputs for download

## Recommended Stack
- Streamlit for UI
- Prefect for workflow orchestration
- Polars for data transforms
- DuckDB for SQL validation / local analytical queries
- Great Expectations for correctness rules
- Gemini API as primary LLM
- Groq or OpenRouter as fallback
- Google Antigravity for AI-assisted development

## Core Modules
- ingestion.py
- schema.py
- detect_changes.py
- transform_scd2.py
- validate.py
- explain.py
- workflow.py
- streamlit_app.py

## Design Principles
- Deterministic first, AI second
- LLM explains; it does not decide
- Keep modules small and testable
- Make outputs easy to demo
- Save evidence for submission and review

## Deployment Plan
- Package as a containerized Streamlit app
- Deploy to Hugging Face Spaces or Render
- Use secrets for API keys
- Keep local fallback mode for development

## Future Enhancements
- Writeback to PostgreSQL
- More file formats
- More advanced lineage metadata
- Optional MCP wrapper later