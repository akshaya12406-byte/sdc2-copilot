# Acceptance Criteria

The project is accepted only if **all** of the following are true:

## Functional Requirements

1. The app accepts a **source CSV** and a **target SCD2 CSV** via file upload.
2. The app **detects new, changed, unchanged, and missing (deleted) records** correctly.
3. The app generates a **valid updated SCD2 table** following the rules in `data_contract.md`.
4. The app **validates** the output:
   - There is only one current row per business key
   - Historical date ranges do not overlap per business key
   - No null business keys exist
   - Schema has all required SCD2 columns
   - `effective_from <= effective_to` where `effective_to` is not null
5. The app generates **human-readable explanations** for every detected change using an LLM (with deterministic template fallback).
6. The app has a **working Streamlit UI** with file upload, results display, and download buttons.

## Quality Requirements

7. The app **runs locally** with `streamlit run app/streamlit_app.py`.
8. The app **can be deployed publicly** to Streamlit Community Cloud.
9. The repo contains **automated tests** (`pytest tests/ -v` passes).
10. The E2E test produces output matching `sample-data/expected_output.csv`.

## Documentation Requirements

11. The repo contains a **prompt log** (`docs/prompt_log.md`).
12. The repo contains an **AI usage note** (`docs/ai_usage_note.md`).
13. The repo contains **sample input and expected output data** (`sample-data/`).
14. The **README** explains setup, run steps, architecture, assumptions, and limitations.

## Correctness Invariants

15. The LLM **never decides** whether a row changed — it only explains already-detected changes.
16. All SCD2 logic is **deterministic and testable** — same inputs always produce the same output.
17. The app works **without API keys** using the template explanation provider.