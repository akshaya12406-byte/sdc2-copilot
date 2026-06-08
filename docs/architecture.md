# Architecture

## High-Level Flow

```
Upload source CSV + target SCD2 CSV
  → Ingest & normalize schemas (ingestion.py)
  → Detect business key & tracked columns (schema.py)
  → Compare records deterministically (detect_changes.py)
  → Generate updated SCD2 table (transform_scd2.py)
  → Run validation checks (validate.py)
  → Produce LLM explanations (explain.py → providers/)
  → Display results in Streamlit (app/streamlit_app.py)
  → Save outputs for download
```

## Stack

| Layer | Technology | Version | Why |
|-------|-----------|---------|-----|
| Data engine | Polars | ≥1.40 | Fast, lazy-capable DataFrames |
| SQL validation | DuckDB | ≥1.5 | In-process SQL for complex validation queries |
| UI | Streamlit | ≥1.45 | Fastest path to public demo |
| Orchestration | Prefect 3 | ≥3.0 | `@flow`/`@task` decorators for observability |
| LLM primary | Gemini via `google-genai` | ≥2.8 | Google's unified GenAI SDK |
| LLM fallback | Groq | ≥1.4 | Fast inference fallback |
| LLM offline | Template engine | built-in | No-API deterministic fallback |
| Config | pydantic-settings | ≥2.0 | Typed `.env` loading |
| Testing | pytest | ≥8.0 | Standard Python test runner |

## Core Modules

| Module | Responsibility |
|--------|---------------|
| `config.py` | Load `.env`, expose `Settings` via pydantic-settings |
| `models.py` | Typed dataclasses: `ChangeRecord`, `ChangeReport`, `ValidationResult`, `Explanation` |
| `ingestion.py` | Load CSV → Polars DataFrame, normalize headers, type coercion |
| `schema.py` | Detect business key + tracked columns from source/target schemas |
| `detect_changes.py` | Compare source vs target current rows → `ChangeReport` |
| `transform_scd2.py` | Apply SCD2 rules → updated Polars DataFrame |
| `validate.py` | Run validation rules → `ValidationReport` |
| `explain.py` | Feed structured diffs to LLM → explanations |
| `workflow.py` | Prefect `@flow` wrapping the full pipeline |
| `providers/base.py` | Abstract `LLMProvider` protocol |
| `providers/template.py` | Deterministic template-based explanations |
| `providers/gemini.py` | Gemini API via `google-genai` |
| `providers/groq.py` | Groq API fallback |

## Design Principles

1. **Deterministic first, AI second** — LLM explains; it does not decide
2. **Keep modules small and testable** — each module has a single responsibility
3. **Type everything** — pydantic models and dataclasses for all data contracts
4. **Fail gracefully** — provider chain: Gemini → Groq → Template (always works)
5. **Make outputs easy to demo** — Streamlit download buttons, clear summaries
6. **Save evidence for submission** — screenshots, prompt logs, test results

## Deployment Plan

- **Primary target**: Streamlit Community Cloud (free, GitHub-connected)
- **Secrets**: Platform-managed secrets (not committed to repo)
- **Local fallback**: `streamlit run app/streamlit_app.py`
- **No Docker in MVP** — Streamlit Cloud handles containerization

## Data Flow Diagram

```
┌─────────────┐    ┌─────────────────┐
│ source.csv  │───▶│  ingestion.py   │
└─────────────┘    │  (load + norm)  │
                   └────────┬────────┘
┌─────────────┐             │
│ target.csv  │───▶─────────┤
└─────────────┘             ▼
                   ┌─────────────────┐
                   │   schema.py     │
                   │ (detect keys)   │
                   └────────┬────────┘
                            ▼
                   ┌─────────────────┐
                   │detect_changes.py│──▶ ChangeReport
                   └────────┬────────┘
                            ▼
                   ┌─────────────────┐
                   │transform_scd2.py│──▶ Updated SCD2 DataFrame
                   └────────┬────────┘
                            ▼
                   ┌─────────────────┐
                   │  validate.py    │──▶ ValidationReport
                   └────────┬────────┘
                            ▼
                   ┌─────────────────┐
                   │   explain.py    │──▶ List[Explanation]
                   │  (Gemini/Groq/  │
                   │   Template)     │
                   └────────┬────────┘
                            ▼
                   ┌─────────────────┐
                   │ streamlit_app   │──▶ UI display + CSV download
                   └─────────────────┘
```