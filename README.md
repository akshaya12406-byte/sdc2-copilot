<p align="center">
  <h1 align="center">🗄️ SCD2 Copilot</h1>
  <p align="center">
    <em>AI-Assisted Slowly Changing Dimension Type 2 Pipeline & Enterprise Observability Console</em>
  </p>
  <p align="center">
    <img src="https://img.shields.io/badge/Python-3.12+-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python 3.12+"/>
    <img src="https://img.shields.io/badge/Polars-1.40+-CD792C?style=flat-square&logo=polars&logoColor=white" alt="Polars"/>
    <img src="https://img.shields.io/badge/Streamlit-1.45+-FF4B4B?style=flat-square&logo=streamlit&logoColor=white" alt="Streamlit"/>
    <img src="https://img.shields.io/badge/Prefect-3.0+-024DFD?style=flat-square&logo=prefect&logoColor=white" alt="Prefect"/>
    <img src="https://img.shields.io/badge/Gemini_API-Integrated-4285F4?style=flat-square&logo=google&logoColor=white" alt="Gemini"/>
    <img src="https://img.shields.io/badge/Tests-178_Passed-2ea44f?style=flat-square" alt="178 Tests Passed"/>
  </p>
</p>

---

## Table of Contents

- [Business Problem](#business-problem)
- [Solution Overview](#solution-overview)
- [Key Features](#key-features)
- [Architecture](#architecture)
- [Pipeline Workflow](#pipeline-workflow)
- [AI Capabilities & Safety Boundary](#ai-capabilities--safety-boundary)
- [Deterministic Engine](#deterministic-engine)
- [Validation Framework](#validation-framework)
- [Confidence Assessment](#confidence-assessment)
- [Token Usage & Cost Tracking](#token-usage--cost-tracking)
- [Business Impact Panel](#business-impact-panel)
- [Sample Use Case](#sample-use-case)
- [Repository Structure](#repository-structure)
- [Installation](#installation)
- [Running the Application](#running-the-application)
- [Running Tests](#running-tests)
- [Sample Data](#sample-data)
- [Testing Strategy](#testing-strategy)
- [Scale Benchmarks](#scale-benchmarks)
- [AI-Assisted Development](#ai-assisted-development)
- [Known Limitations](#known-limitations)
- [Future Enhancements](#future-enhancements)
- [Challenge Requirement Mapping](#challenge-requirement-mapping)
- [Submission Checklist](#submission-checklist)

---

## Business Problem

Slowly Changing Dimensions (SCD Type 2) track historical values of records in data warehouses by closing old rows (stamping `effective_to` and setting `is_current = false`) and inserting new active rows.

Implementing this pattern traditionally introduces major challenges:

| Challenge | Description |
|:---|:---|
| **Repetitive Manual SQL** | Writing and maintaining complex MERGE or windowing queries is highly error-prone and developer-intensive. |
| **Auditability Gap** | Business compliance teams cannot easily interpret *why* customer states changed — the logic is hidden inside SQL scripts. |
| **Silent Data Corruption** | Schema drift (added/removed columns) or unexpected type coercion breaks pipelines silently, leading to corrupted point-in-time reports. |

---

## Solution Overview

SCD2 Copilot automates this entire lifecycle with a **hybrid architecture** that enforces a strict separation between deterministic computation and generative AI:

| Layer | Technology | Responsibility |
|:---|:---|:---|
| **Deterministic Engine** | Polars (local) | Change detection, SCD2 transformation, validation — fully deterministic, reproducible results |
| **AI Explanation Layer** | Gemini / Groq API | Batch natural-language explanations for detected changes — the LLM **explains**, it never **decides** |
| **Enterprise Dashboard** | Streamlit | Interactive UI with cost trackers, token metrics, pipeline latency, business impact statistics, and overrides |

> **Core Safety Principle:** The LLM does not influence which rows are classified as NEW, CHANGED, UNCHANGED, or DELETED. All classification and transformation logic executes locally in deterministic Polars code. The LLM is invoked only after all data decisions are finalized, solely to generate human-readable explanations.

---

## Key Features

1. **Heuristic Schema Detection** — Automatically infers business key(s) and tracked attributes from raw CSV inputs  
   → `src/scd2_copilot/schema.py`

2. **Deterministic SCD2 Transformer** — Identifies `NEW`, `CHANGED`, `UNCHANGED`, `DELETED` records and outputs correct SCD2 timestamps  
   → `src/scd2_copilot/detect_changes.py`, `src/scd2_copilot/transform_scd2.py`

3. **5-Point Invariant Validator** — Programmatically validates output tables for schema completeness, overlaps, duplicate active rows, null keys, and date consistency  
   → `src/scd2_copilot/validate.py`

4. **Batch AI Explanations** — Groups all changed records into a single optimized system-prompt call with Pydantic-structured output to reduce LLM costs  
   → `src/scd2_copilot/explain.py`, `src/scd2_copilot/providers/gemini.py`

5. **Multi-Model API Fallback Chain** — Automatically falls back through 5 Gemini models → Groq → offline templates if all APIs fail  
   → `src/scd2_copilot/providers/`

6. **Token & Cost Tracker** — Displays exact token counts (from API metadata) or safe character-based estimations, with real-time cost computation  
   → `app/ui_components.py: render_ai_usage_panel()`

7. **ROI Business Impact Panel** — Highlights time saved, records processed, and audit compliance metrics for decision-makers  
   → `app/ui_components.py: render_business_impact_panel()`

8. **Confidence Assessment Framework** — Honest, transparent scoring (0–100%) based on validation outcomes and provider runtime mode  
   → `app/ui_components.py: compute_confidence_assessment()`

---

## Architecture

The project uses a **decoupled architecture** where the data engine operates independently of the AI components. The LLM is never involved in data classification or transformation decisions — it only generates explanations after all processing is complete.

```
┌─────────────────────────┐
│   Source CSV (Today)    │
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│   Target SCD2 Table     │
│   (Yesterday)           │
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────────────────┐
│   Deterministic SCD2 Engine        │
│                                    │
│   • Schema Detection               │
│   • Change Detection               │
│   • SCD2 Transformation            │
│   • Historical Preservation        │
└────────────┬───────────────────────┘
             │
             ▼
┌─────────────────────────┐
│   Validation Layer      │
│   5 Integrity Rules     │
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│   LLM Explanation       │
│   Generator             │
│   Gemini / Groq         │
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│   Streamlit Dashboard   │
│   Reports & Metrics     │
└─────────────────────────┘
```

| Layer | Responsibility |
|:---|:---|
| **Input Layer** | Accept source and target CSV files |
| **SCD2 Engine** | Detect changes and create valid SCD2 history |
| **Validation** | Verify data integrity against 5 invariant rules |
| **AI Layer** | Generate natural-language explanations for detected changes |
| **Dashboard** | Visualize results, metrics, downloads, and audit trail |

### Technology Stack

| Component | Technology | Purpose |
|:---|:---|:---|
| Data Engine | **Polars** ≥1.40 | DataFrame operations, change detection, SCD2 transforms |
| Orchestration | **Prefect** ≥3.0 | Pipeline task observability with `@flow` and `@task` decorators |
| Web UI | **Streamlit** ≥1.45 | Interactive dashboard with dark theme |
| Primary LLM | **Gemini** (google-genai ≥2.8) | Structured batch explanations via Pydantic schema |
| Fallback LLM | **Groq** ≥1.4 | Secondary API provider |
| Config | **Pydantic Settings** | Environment-based configuration from `.env` |
| Testing | **Pytest** ≥8.0 | 178 automated tests |

---

## Pipeline Workflow

Every execution progresses through **6 sequential stages**, orchestrated by Prefect tasks in `src/scd2_copilot/workflow.py`:

```
Step 1: Ingest & Normalize   → Parse CSVs, strip whitespace, coerce types
Step 2: Schema Match          → Detect business key & tracked columns
Step 3: Compute Diffs         → Deterministic change detection (NEW/CHANGED/UNCHANGED/DELETED)
Step 4: Transform SCD2        → Write effective_from/effective_to, update is_current flags
Step 5: Run Invariants        → Validate output against 5 integrity rules
Step 6: Generate Explanations → Batch LLM call for natural-language explanations
```

---

## AI Capabilities & Safety Boundary

### What AI Does
- **Explains** detected changes in clear business language  
  *Example: "Customer Ravi moved from Chennai to Bengaluru — city field updated."*
- Uses **JSON-Schema constrained output** via Pydantic models (`list[ExplanationItem]`) to ensure structured, parseable responses
- **Optimizes token usage**: Only `NEW`, `CHANGED`, and `DELETED` records are sent to the LLM; `UNCHANGED` records are skipped entirely

### What AI Does NOT Do
- ❌ Does NOT decide whether a row changed
- ❌ Does NOT influence which records are classified as NEW/CHANGED/DELETED
- ❌ Does NOT modify any data in the SCD2 output table
- ❌ Has no access to the transformation logic

### Provider Fallback Chain

```
Gemini 3.5 Flash → Gemini 3.1 Flash Lite → Gemini 3 Flash → Gemini 2.5 Flash Lite → Gemini 2.5 Flash → Groq → Template (offline)
```

Each Gemini model has separate daily quotas. If one is exhausted or unavailable, the system automatically tries the next. If all online providers fail, the system degrades gracefully to **offline template explanations** — the pipeline never fails due to an API outage.

---

## Deterministic Engine

All change analysis and timestamp transformations are performed **locally** by Polars — no network calls, no LLM involvement. Results are fully reproducible across runs:

| Module | File | Logic |
|:---|:---|:---|
| **Change Detection** | `detect_changes.py` | Maps target active records into a lookup dict by business key; compares source inputs field-by-field |
| **SCD2 Transform** | `transform_scd2.py` | Preserves historical closed rows untouched; closes modified records by setting `effective_to = processing_date` and `is_current = False`; appends new active records |
| **Ingestion** | `ingestion.py` | Loads CSVs, strips whitespace, validates column compatibility between source and target |
| **Schema Inference** | `schema.py` | Heuristic detection of business key (highest cardinality ID-like column) and tracked attributes |

---

## Validation Framework

Every generated output is validated against **5 deterministic integrity rules** implemented in `src/scd2_copilot/validate.py`:

| # | Rule Name | Description |
|:---:|:---|:---|
| 1 | `schema_completeness` | Confirms that `effective_from`, `effective_to`, and `is_current` columns exist |
| 2 | `one_current_per_key` | Confirms each business key has at most one row marked `is_current = True` |
| 3 | `no_null_keys` | Confirms that business key values are non-null |
| 4 | `no_overlapping_dates` | Verifies that historical timelines for any key never overlap |
| 5 | `date_consistency` | Verifies that `effective_from ≤ effective_to` for closed rows |

---

## Confidence Assessment

Computes system trustworthiness transparently based on validation outcomes and provider mode.  
Implemented in `app/ui_components.py: compute_confidence_assessment()`.

| Level | Score | Conditions |
|:---|:---:|:---|
| **Very High** | ≥ 90% | All 5 validation rules pass + online LLM provider completed successfully |
| **High** | 75–89% | All validation rules pass + template fallback mode |
| **Medium** | 50–74% | Validation warnings present |
| **Low** | < 50% | One or more validation rules failed |

The assessment is displayed with a progress bar and an honest, transparent explanation of *why* that score was assigned — no misleading "100% accuracy" claims.

---

## Token Usage & Cost Tracking

The **AI Usage & Efficiency** panel (`app/ui_components.py: render_ai_usage_panel()`) displays:

| Metric | Source | Description |
|:---|:---|:---|
| Provider & Model | `LLMMetrics.provider`, `.model` | Active service identity |
| Token Counts | API `usage_metadata` or estimation | `prompt_tokens + completion_tokens` — labeled as "Exact" or "Estimated" |
| Estimated Cost | Computed from published rates | Gemini: $0.075/1M prompt, $0.30/1M completion |
| API Latency | `time.perf_counter()` | Request duration in seconds |
| Avg Tokens/Change | `total_tokens / num_changes` | Per-record efficiency metric |
| Efficiency Badge | Threshold-based | `Excellent` (≤150), `Good` (≤350), `Moderate` (≤750), `Expensive` (>750) |

When API metadata is unavailable, tokens are estimated using the formula `Characters ÷ 4` and clearly labeled as "Estimated Tokens" in the UI.

---

## Business Impact Panel

The **Business Impact** panel (`app/ui_components.py: render_business_impact_panel()`) provides executives with a side-by-side comparison:

| Dimension | Traditional (Manual) | SCD2 Copilot (Automated) |
|:---|:---|:---|
| **Process** | Manual SQL, validation, documentation, analysis | Automated generation, validation, detection, AI explanations |
| **Time** | 30–60 minutes per iteration | < 1 minute |
| **Audit Trail** | Manual trace logs | Automatic, downloadable reports |

Additionally displays live operational metrics: Records Processed, Changes Detected, Historical Records Preserved, Validation Rules Passed.

---

## Sample Use Case

### Scenario: Customer Address & Tier Update

**Source data** (`sample-data/source_today.csv`):
```
customer_id, name,  city,      tier
101,         Ravi,  Bengaluru, Gold     ← city changed from Chennai
102,         Priya, Mumbai,    Silver   ← unchanged
103,         Arun,  Delhi,     Gold     ← unchanged
104,         Kiran, Hyderabad, Bronze   ← new customer
```

**Target data** (`sample-data/target_yesterday.csv`):
```
customer_id, name,  city,    tier,   effective_from, effective_to, is_current
101,         Ravi,  Chennai, Gold,   2026-06-07,     ,             true
102,         Priya, Mumbai,  Silver, 2026-06-07,     ,             true
103,         Arun,  Delhi,   Gold,   2026-06-07,     ,             true
```

**SCD2 Output** (`sample-data/expected_output.csv`):
| customer_id | name | city | tier | effective_from | effective_to | is_current |
|:---:|:---|:---|:---|:---:|:---:|:---:|
| 101 | Ravi | Chennai | Gold | 2026-06-07 | 2026-06-08 | false |
| 101 | Ravi | Bengaluru | Gold | 2026-06-08 | | true |
| 102 | Priya | Mumbai | Silver | 2026-06-07 | | true |
| 103 | Arun | Delhi | Gold | 2026-06-07 | | true |
| 104 | Kiran | Hyderabad | Bronze | 2026-06-08 | | true |

**AI Explanation:** *"Customer Ravi's city changed from Chennai to Bengaluru."*

---

## Repository Structure

```
sdc2-copilot/
├── README.md                        # This file
├── Project - sdc2-copilot/          # Root project workspace
│   ├── app/                         # Streamlit frontend
│   │   ├── streamlit_app.py         # Application entry point (318 lines)
│   │   ├── ui_components.py         # HTML/CSS dashboard components (905 lines)
│   │   └── dashboard_theme.css      # Dark-mode design system (19KB)
│   │
│   ├── src/scd2_copilot/            # Core pipeline package
│   │   ├── config.py                # Pydantic Settings (.env loader)
│   │   ├── models.py                # Data models (ChangeRecord, LLMMetrics, PipelineResult)
│   │   ├── ingestion.py             # CSV loading & schema matching
│   │   ├── schema.py                # Heuristic business key inference
│   │   ├── detect_changes.py        # Local deterministic change detection
│   │   ├── transform_scd2.py        # SCD2 date versioning & status flags
│   │   ├── validate.py              # 5-rule post-transform invariant checks
│   │   ├── explain.py               # LLM fallback orchestration & metrics
│   │   ├── workflow.py              # Prefect @flow/@task pipeline wrapper
│   │   └── providers/               # LLM provider clients
│   │       ├── base.py              # Abstract LLMProvider base class
│   │       ├── gemini.py            # Gemini API (5-model fallback chain)
│   │       ├── groq.py              # Groq API fallback provider
│   │       └── template.py          # Offline template provider (zero API calls)
│   │
│   ├── tests/                       # Pytest test suites (178 tests)
│   │   ├── conftest.py              # Shared fixtures
│   │   ├── test_detect_changes.py   # Change detection unit tests
│   │   ├── test_transform_scd2.py   # SCD2 transformation tests
│   │   ├── test_validate.py         # Validation rule tests
│   │   ├── test_explain.py          # Explanation orchestration tests
│   │   ├── test_e2e_sample.py       # End-to-end sample data tests
│   │   ├── test_smoke.py            # Smoke tests
│   │   ├── test_rigorous.py         # Rigorous edge case tests
│   │   ├── test_ultra_audit.py      # Comprehensive audit tests
│   │   ├── run_saturation_audit.py  # Property-based saturation audit
│   │   └── adversarial/             # Adversarial & performance tests
│   │       ├── test_adversarial_scenarios.py  # 17 adversarial edge cases
│   │       ├── test_performance_benchmarks.py # Scale benchmarks (1K–100K rows)
│   │       └── benchmark_results.json         # Cached benchmark metrics
│   │
│   ├── docs/                        # Architecture & reports
│   │   ├── project_brief.md         # Problem statement & success criteria
│   │   ├── decision_log.md          # Technical decision log
│   │   ├── demo_script.md           # Demo walkthrough script
│   │   ├── comp_report.md           # Comprehensive implementation report
│   │   ├── judge_readiness_report.md # Judge presentation document
│   │   └── final_saturation_audit.md # Post-validation engineering audit
│   │
│   ├── sample-data/                 # Reference CSV files
│   │   ├── source_today.csv         # 4 customer records (today's snapshot)
│   │   ├── target_yesterday.csv     # 3 active SCD2 rows (yesterday's table)
│   │   └── expected_output.csv      # Verified expected SCD2 output
│   │
│   ├── AGENTS.md                    # AI assistant guidelines & constraints
│   ├── requirements.txt             # Python package dependencies
│   ├── .env.example                 # Environment configuration template
│   └── .gitignore                   # Git ignore rules
```

---

## Installation

### Prerequisites

- **Python 3.12+**
- **Git**
- A **Gemini API key** (free tier available at [ai.google.dev](https://ai.google.dev)) — optional, the app works fully offline with template explanations

### Setup Steps

```powershell
# Clone the repository
git clone https://github.com/akshaya12406-byte/sdc2-copilot.git
cd sdc2-copilot

# Enter the project directory
cd "Project - sdc2-copilot"

# Create a virtual environment
python -m venv .venv

# Activate the virtual environment (Windows PowerShell)
.\.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Configure API keys (optional — app works without them)
copy .env.example .env
# Edit .env and set GEMINI_API_KEY and/or GROQ_API_KEY
```

---

## Running the Application

> **Important:** Always run Streamlit via Python's module launcher to avoid path issues with virtual environment executables on Windows.

```powershell
# From the "Project - sdc2-copilot" directory, with .venv activated:
python -m streamlit run app/streamlit_app.py
```

The dashboard will open at `http://localhost:8501`.

### Quick Start
1. Upload `sample-data/source_today.csv` as **Source CSV**
2. Upload `sample-data/target_yesterday.csv` as **Target CSV**
3. Select a provider (Template works without API keys)
4. Click **Run SCD2 Pipeline**
5. Explore results across 6 tabs: Overview, Updated Table, Validation, Explanations, Explorer, History

---

## Running Tests

```powershell
# Run all 178 tests
python -m pytest

# Run with verbose output
python -m pytest -v

# Run adversarial scenarios only
python -m pytest tests/adversarial/test_adversarial_scenarios.py -v

# Run performance benchmarks with output
python -m pytest tests/adversarial/test_performance_benchmarks.py -s

# Run core unit tests only
python -m pytest tests/test_detect_changes.py tests/test_transform_scd2.py tests/test_validate.py -v
```

---

## Sample Data

The `sample-data/` folder contains reference files for immediate testing:

| File | Records | Description |
|:---|:---:|:---|
| `source_today.csv` | 4 | Today's customer snapshot (includes 1 new, 1 changed, 2 unchanged) |
| `target_yesterday.csv` | 3 | Yesterday's active SCD2 table |
| `expected_output.csv` | 5 | Verified correct SCD2 output (used by `test_e2e_sample.py`) |

---

## Testing Strategy

Our test strategy implements **4 layers of verification** totaling **178 automated tests** (all passing):

### Layer 1: Unit Tests
Tests individual pipeline modules in isolation:
- `test_detect_changes.py` — Change detection logic
- `test_transform_scd2.py` — SCD2 transformation output
- `test_validate.py` — Validation rule correctness (7 tests)
- `test_explain.py` — Explanation orchestration & fallback

### Layer 2: End-to-End Tests
- `test_e2e_sample.py` — Full pipeline execution against sample data
- `test_smoke.py` — Smoke tests for import and basic functionality

### Layer 3: Adversarial Suite (17 tests in `tests/adversarial/`)
Covers edge cases that break production SCD2 implementations:

| Test | Scenario |
|:---|:---|
| `test_duplicate_source_keys` | Duplicate business keys in source input |
| `test_duplicate_current_target_records` | Multiple active rows for same key in target |
| `test_composite_key_configurations` | Single, dual, and triple composite keys (parameterized) |
| `test_schema_drift_added_column` | Source has columns not in target |
| `test_schema_drift_removed_column` | Source missing columns from target |
| `test_type_drift_coercion` | Integer vs string type mismatches |
| `test_null_business_keys` | Null values in business key columns |
| `test_empty_files` | Empty DataFrames |
| `test_large_text_fields` | 10,000+ character field values |
| `test_unicode_fields` | Unicode characters (CJK, emoji, diacritics) |
| `test_whitespace_variations` | Leading/trailing/internal whitespace |
| `test_case_variations` | Case-sensitive value comparisons |
| `test_future_effective_dates` | Processing dates in the future |
| `test_historical_gap_detection` | Gaps in SCD2 date timelines |
| `test_overlapping_date_detection` | Overlapping date intervals |
| `test_massive_change_volume` | 1,000-record change set |
| `test_api_failure_simulation` | Mocked Gemini 429 quota error |

### Layer 4: Rigorous Audit & Property Tests
- `test_rigorous.py` — 37K+ lines of comprehensive edge case coverage
- `test_ultra_audit.py` — 33K+ lines covering composites, performance, prompts, isolation
- `run_saturation_audit.py` — Property-based randomized data variation testing

---

## Scale Benchmarks

Performance benchmarks executed via `tests/adversarial/test_performance_benchmarks.py`, measuring runtime, memory usage, and throughput. Results stored in `tests/adversarial/benchmark_results.json`:

| Rows | Detect Time | Transform Time | Total Time | Peak Memory | Throughput |
|:---:|:---:|:---:|:---:|:---:|:---:|
| **1,000** | 0.03s | 0.03s | 0.06s | 1.0 MB | 17,328 rows/s |
| **10,000** | 0.34s | 0.32s | 0.65s | 9.5 MB | 15,330 rows/s |
| **25,000** | 0.93s | 0.95s | 1.88s | 25.3 MB | 13,301 rows/s |
| **50,000** | 1.63s | 1.84s | 3.47s | 48.0 MB | 14,421 rows/s |
| **100,000** | 3.47s | 3.89s | 7.36s | 96.9 MB | 13,581 rows/s |

All benchmarks passed validation checks. Throughput remains consistently above **13,000 rows/second** across all dataset sizes.

---

## AI-Assisted Development

AI (Google Antigravity) was used to accelerate development across multiple phases:

| Phase | AI Contribution | Human Oversight |
|:---|:---|:---|
| **Architecture Planning** | Scaffolded module structure, provider interfaces | Reviewed and refined separation of concerns |
| **Code Generation** | Generated Polars DataFrame operations, CSS dark theme, pytest harness | Applied manual corrections for edge cases |
| **Testing** | Generated adversarial test scenarios, benchmark framework | Verified test assertions match actual behavior |
| **Documentation** | Drafted README sections, demo script, audit reports | Cross-validated every claim against codebase |

### Key Self-Corrections Applied Manually
- Converted DuckDB `rowid` stability issues to Polars native expressions
- Fixed Streamlit expander arrow text corruption in CSS styling
- Resolved same-day multi-row overwrite edge cases in `transform_scd2.py`

### Contribution Split (Approximate)
- Planning: ~75% AI, ~25% Human
- Coding: ~80% AI, ~20% Human
- Testing: ~85% AI, ~15% Human
- Documentation: ~90% AI, ~10% Human

---

## Known Limitations

1. **Single-Node Memory Bound** — Large transformations (>100M rows) are constrained by single-node RAM. The current Polars engine operates in-process without distributed compute.

2. **Chronological Processing Assumption** — Incoming snapshots must be processed in chronological order. Out-of-order processing may produce incorrect `effective_from`/`effective_to` stamps.

3. **CSV-Only Input** — The MVP supports flat-file CSV inputs. Direct database connectors (Snowflake, BigQuery) are deferred to future versions.

4. **LLM Rate Limits** — Free-tier Gemini API has daily request quotas. The 5-model fallback chain mitigates this, but sustained high-volume usage may exhaust all models.

5. **No Persistent Storage** — Session state is in-memory only. Run history is lost on page refresh. A database-backed audit log is a future enhancement.

---

## Future Enhancements

1. **Vectorized Matching** — Port remaining Python loops in `detect_changes.py` to native Polars join expressions for further performance gains.

2. **Incremental AI Explanations** — Store previous audit results to prevent re-explaining unchanged attributes across consecutive runs.

3. **SQL Database Connectors** — Add direct connection managers for Snowflake, BigQuery, and Databricks to move beyond CSV-only input.

4. **Persistent Audit Log** — Add SQLite or DuckDB-backed run history for durable session tracking.

5. **Deployment Automation** — Containerized deployment with Docker and CI/CD pipeline configuration.

---

## Challenge Requirement Mapping

| Requirement | Evidence in Repository | Status |
|:---|:---|:---:|
| **SCD2 Table Generation** | `transform_scd2.py` outputs `effective_from`, `effective_to`, `is_current` columns. Verified by `test_transform_scd2.py` and `test_e2e_sample.py`. | ✅ **Fully Satisfied** |
| **Change Detection** | `detect_changes.py` classifies records as `NEW`, `CHANGED`, `UNCHANGED`, `DELETED`. Verified by `test_detect_changes.py`. | ✅ **Fully Satisfied** |
| **LLM Change Explainer** | `explain.py` orchestrates batch calls through Gemini/Groq/Template. Structured output via Pydantic models. Verified by `test_explain.py`. | ✅ **Fully Satisfied** |
| **Workflow Tool** | Prefect `@flow` and `@task` decorators in `workflow.py` provide pipeline observability. | ✅ **Fully Satisfied** |
| **Functionality Testing** | 178 tests covering unit, E2E, adversarial, and scale benchmarks. All passing. | ✅ **Fully Satisfied** |
| **UI Dashboard** | Streamlit console with 6 tabs, KPI strip, file uploaders, filters, and CSV downloads. Custom dark theme. | ✅ **Fully Satisfied** |
| **Observability** | Token metrics, latency tracking, cost estimation, efficiency badges, confidence assessment, and business impact panel. | ✅ **Fully Satisfied** |
| **Sample Data** | `sample-data/` contains source, target, and expected output CSVs. | ✅ **Fully Satisfied** |
| **Documentation** | README, AGENTS.md, project brief, decision log, demo script, judge readiness report, saturation audit. | ✅ **Fully Satisfied** |

---

## Submission Checklist

- [x] Functional SCD2 pipeline (Polars/Python deterministic engine)
- [x] Dynamic Streamlit web dashboard with dark-mode design system
- [x] Multi-Model API fallback orchestration (Gemini → Groq → Template)
- [x] 178 automated tests — all passing
- [x] 17 adversarial edge case tests
- [x] Scale benchmarks: 1K → 100K rows (13K+ rows/sec throughput)
- [x] 5-point validation invariant framework
- [x] Token, latency, and cost observability
- [x] Business impact and confidence assessment panels
- [x] Complete documentation and reports
- [x] Sample data with verified expected output
- [x] AI usage transparency and contribution tracking

---

<p align="center">
  <strong>SCD2 Copilot</strong> · Deterministic change detection · AI-powered explanations<br/>
  Built for <strong>Infinite Computer Solutions</strong> AI Prototype Challenge
</p>
