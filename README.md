# SCD2 Copilot

An AI-assisted Slowly Changing Dimension Type 2 (SCD2) builder that:
- accepts a source CSV (today's data) and yesterday's SCD2 CSV
- detects new, changed, unchanged, and deleted records deterministically
- generates the updated SCD2 table
- validates correctness with business rules
- explains every change in natural language using an LLM

## Why This Exists

Enterprise teams repeatedly hand-code SCD2 logic for data warehouse tables. This is repetitive, error-prone, and hard to maintain. SCD2 Copilot automates the comparison, transformation, validation, and explanation — so data engineers can focus on business logic, not merge boilerplate.

## Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| UI | Streamlit | File upload, results display, download |
| Data Engine | Polars + DuckDB | Fast DataFrame ops + SQL validation |
| Orchestration | Prefect 3 | Workflow observability (`@flow`/`@task`) |
| LLM (primary) | Google Gemini (`google-genai`) | Natural-language change explanations |
| LLM (fallback) | Groq | Fallback if Gemini is unavailable |
| LLM (offline) | Template engine | Deterministic fallback, no API needed |
| Config | pydantic-settings | Typed `.env` loading |
| Deployment | Streamlit Community Cloud | Free, public demo |

## Project Structure

```
sdc2-copilot/
├── AGENTS.md                    # AI assistant instructions
├── README.md                    # This file
├── requirements.txt             # Python dependencies
├── .env.example                 # Environment variable template
├── .gitignore
│
├── src/scd2_copilot/            # Core application package
│   ├── __init__.py
│   ├── config.py                # Settings via pydantic-settings
│   ├── models.py                # Typed dataclasses (ChangeReport, etc.)
│   ├── ingestion.py             # CSV loading + schema normalization
│   ├── schema.py                # Business key & tracked column detection
│   ├── detect_changes.py        # Deterministic change detection
│   ├── transform_scd2.py        # SCD2 table generation
│   ├── validate.py              # Lightweight validation rules
│   ├── explain.py               # LLM explanation orchestration
│   ├── workflow.py              # Prefect flow wrapping the pipeline
│   └── providers/               # LLM provider implementations
│       ├── base.py
│       ├── template.py
│       ├── gemini.py
│       └── groq.py
│
├── app/
│   └── streamlit_app.py         # Streamlit UI
│
├── tests/                       # pytest test suite
│   ├── conftest.py
│   ├── test_detect_changes.py
│   ├── test_transform_scd2.py
│   ├── test_validate.py
│   ├── test_explain.py
│   └── test_e2e_sample.py
│
├── sample-data/                 # Reference datasets
│   ├── source_today.csv
│   ├── target_yesterday.csv
│   ├── expected_output.csv
│   └── edge_cases/
│
└── docs/                        # Project documentation
    ├── project_brief.md
    ├── architecture.md
    ├── data_contract.md
    ├── acceptance_criteria.md
    ├── decision_log.md
    ├── prompt_log.md
    ├── ai_usage_note.md
    ├── demo_script.md
    ├── limitations.md
    └── deployment_notes.md
```

## Setup

### Prerequisites
- Python 3.12+
- A Gemini API key (optional — the app works without one using template explanations)

### Installation

```bash
# Clone the repo
git clone https://github.com/akshaya12406-byte/sdc2-copilot.git
cd sdc2-copilot

# Create virtual environment
python -m venv .venv

# Activate (Windows PowerShell)
.\.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Copy and fill environment variables
copy .env.example .env
# Edit .env and add your API keys
```

### Run

```bash
# Activate venv first
.\.venv\Scripts\Activate.ps1

# Start the app
streamlit run app/streamlit_app.py
```

### Test

```bash
.\.venv\Scripts\Activate.ps1
pytest tests/ -v
```

## Architecture

See [docs/architecture.md](docs/architecture.md) for the full architecture diagram and design principles.

## Key Design Decision

**The LLM explains changes — it never decides them.** All change detection and SCD2 transformation is deterministic (Polars-based). The LLM only receives structured diffs and produces human-readable summaries.

## Assumptions

- Source CSV represents today's full snapshot (not incremental)
- Target CSV is yesterday's SCD2 table (may contain historical rows)
- Business key is user-selectable (auto-detected by default)
- Processing date defaults to today, but is configurable
- Missing source records are treated as soft deletes

## Limitations

See [docs/limitations.md](docs/limitations.md).

## License

MIT
