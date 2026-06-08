# Decision Log

All major technical and design decisions are recorded here with rationale.

---

## Decision 1 — Use Streamlit for UI
**Date**: 2026-06-08
**Status**: Confirmed

**Reason**: Fastest path to a clean public demo. Streamlit Community Cloud offers free deployment with GitHub integration. No Docker needed for MVP.

**Alternatives considered**: Gradio (less flexible for tables), Flask+React (too heavy), plain HTML (no interactivity).

---

## Decision 2 — Use Prefect 3 as a thin workflow wrapper
**Date**: 2026-06-08
**Status**: Confirmed

**Reason**: `@flow` and `@task` decorators provide observability and structured logging without running a separate Prefect server. The pipeline runs inline within the Streamlit process.

**Alternatives considered**: No orchestration (loses observability), Dagster (heavier), plain functions (no retry/logging).

---

## Decision 3 — Use Polars + DuckDB instead of PySpark
**Date**: 2026-06-08
**Status**: Confirmed

**Reason**: CSV-driven prototype with small-to-medium data. Polars is faster for single-node work, DuckDB provides SQL for complex validation queries. Both are lightweight and deployment-friendly. PySpark adds ~200MB and requires JVM.

**Alternatives considered**: PySpark (too heavy for MVP), pandas-only (slower, no SQL), DuckDB-only (less ergonomic for transforms).

---

## Decision 4 — Use custom lightweight validator instead of Great Expectations
**Date**: 2026-06-08
**Status**: Confirmed

**Reason**: The 5 validation rules needed (one-current-per-key, no date overlaps, no null keys, schema completeness, date consistency) are simple enough to implement with Polars + DuckDB queries. Great Expectations adds 700+ sub-dependencies, complex data context setup, slow imports, and complicates deployment.

**Alternatives considered**: Great Expectations (too heavy), Pandera (pandas-focused), Soda Core (adds server complexity).

---

## Decision 5 — Use Google GenAI SDK (`google-genai`) for Gemini
**Date**: 2026-06-08
**Status**: Confirmed

**Reason**: `google-genai` (v2.8.0) is Google's new unified SDK, replacing `google-generativeai`. It has a cleaner API, supports both Gemini and Vertex AI, and is actively maintained.

**Alternatives considered**: `google-generativeai` (older, being deprecated), direct REST API (more code).

---

## Decision 6 — Use Groq as fallback LLM provider
**Date**: 2026-06-08
**Status**: Confirmed

**Reason**: Groq provides fast inference at the free tier. Good backup if Gemini is unavailable or rate-limited.

---

## Decision 7 — Defer OpenRouter to post-MVP
**Date**: 2026-06-08
**Status**: Deferred

**Reason**: Two LLM providers (Gemini + Groq) plus a deterministic template fallback is sufficient for MVP. OpenRouter adds complexity without proportional value at this stage.

---

## Decision 8 — No custom MCP server in MVP
**Date**: 2026-06-08
**Status**: Confirmed

**Reason**: Not required for core value. Too much complexity for the project timeline.

---

## Decision 9 — Use pydantic-settings for configuration
**Date**: 2026-06-08
**Status**: Confirmed

**Reason**: Typed `.env` loading with validation. `pydantic-settings` is the official way to handle environment-based config in Pydantic v2. Replaces `BaseSettings` from core pydantic (which was moved to `pydantic-settings`).

---

## Decision 10 — Streamlit Community Cloud as deployment target
**Date**: 2026-06-08
**Status**: Confirmed

**Reason**: Free tier, direct GitHub repo connection, automatic deploys on push, built-in secrets management. No Docker or Dockerfile needed.

**Alternatives considered**: Hugging Face Spaces (good but extra step), Render (more control but needs Dockerfile), self-hosted (not suitable for public demo).

---

## Decision 11 — Processing date is user-selectable
**Date**: 2026-06-08
**Status**: Confirmed

**Reason**: The `effective_from` date for new/changed rows should default to `date.today()` but be overridable in the UI. This supports testing with historical dates and makes the demo more flexible.

---

## Decision 12 — Missing records treated as soft deletes
**Date**: 2026-06-08
**Status**: Confirmed

**Reason**: When a business key exists in the target (current row) but not in the source, the row is closed with `effective_to = processing_date, is_current = false`. This is the standard SCD2 soft-delete pattern.

---

## Decision 13 — Field-by-field comparison, not hashing
**Date**: 2026-06-08
**Status**: Confirmed

**Reason**: Direct field comparison (not hash-based) is needed so we can report *which* fields changed. This information feeds into the LLM explanation prompt.

---

## Decision 14 — No Dockerfile in MVP
**Date**: 2026-06-08
**Status**: Confirmed

**Reason**: Streamlit Community Cloud handles containerization. A Dockerfile adds maintenance burden without value until a different deployment target is chosen.