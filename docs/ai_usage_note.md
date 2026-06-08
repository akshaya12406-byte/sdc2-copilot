# AI Usage Note

## How AI Was Used

| Phase | AI Tool | What It Did |
|-------|---------|-------------|
| Planning | Google Antigravity (Claude Opus 4) | Read all project docs, analyzed repo state, proposed implementation plan |
| Architecture | Google Antigravity | Confirmed stack choices against official docs (google-genai SDK, pydantic-settings, etc.) |
| Scaffolding | Google Antigravity | Generated package structure, config, typed models, test fixtures |
| Documentation | Google Antigravity | Drafted/updated all docs in `docs/` directory |
| Code generation | Google Antigravity | Generated core module skeletons with type annotations |
| Testing | Google Antigravity | Generated test cases and fixtures |
| Explanations | Gemini API (runtime) | Generates natural-language explanations of SCD2 changes at runtime |

## What AI Got Right
- Correctly identified all missing packages and broken metadata in the venv
- Correctly verified sample data against expected output
- Proposed dropping Great Expectations (accepted — lightweight validator is better for MVP)
- Identified `google-genai` as the correct SDK (not `google-generativeai`)
- Generated accurate SCD2 business rules matching the data contract

## What AI Got Wrong
- Initially reported Streamlit as "broken" when it was only a metadata display issue (imports worked fine)
- PySpark was reported as "in venv" but it was a system-level install — couldn't uninstall from venv

## What Was Corrected Manually
- SCD2 transform rules verified by hand against expected_output.csv
- Business key detection logic reviewed for correctness
- Validation rules cross-checked against data_contract.md
- Date handling rules confirmed against sample data dates
- All docs reviewed for accuracy before committing

## Key Design Constraint
**The LLM explains changes — it never decides them.** All change detection, SCD2 transformation, and validation is deterministic Python code (Polars-based). The LLM only receives structured diffs and produces human-readable summaries. If the LLM is unavailable, a deterministic template engine produces explanations instead.

## Best Prompts Used
1. "Read AGENTS.md, all docs, verify environment, summarize repo state, identify gaps, create implementation plan" — produced a comprehensive project understanding
2. "Full stack audit against official docs, confirm every dependency, update all files" — caught the google-genai vs google-generativeai choice and pydantic-settings requirement

## Final Judgment
AI was used as a **development accelerator** — it read docs, proposed plans, generated scaffolding, and wrote tests. **Correctness was enforced through**:
- Deterministic SCD2 rules (not AI-decided)
- Automated tests against known expected output
- Manual review of all generated code and documentation
- Type-safe data contracts (pydantic models + dataclasses)