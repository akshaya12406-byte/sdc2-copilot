# AI Usage Note and Prompt Documentation

This document describes how Artificial Intelligence was utilized during the design, development, and validation of the **SCD2 Copilot** project, conforming to the guidelines of the Infinite Computer Solutions submission.

## Tools Used
* **Google Antigravity**: Primary AI assistant utilized for repository auditing, plan generation, code scaffolding, test design, and theme creation.
* **Claude**: Underlay LLM option for the development agent's reasoning.
* **Gemini (SDK & API)**: Primary LLM runtime engine used to generate natural-language explanations of dimension changes using structured outputs.
* **Groq (API)**: Secondary LLM runtime engine used as the primary fallback provider.
* **Streamlit**: Web application framework for the enterprise operations console.
* **Python**: Core programming language using Polars for dataframes, DuckDB for local SQL queries, and Prefect 3 for orchestration.

---

## 1. Development History Analysis

All AI interactions throughout the project lifecycle have been categorized and audited below:

| Development Category | What AI Helped With / Generated | Required Human Decisions | Acceptance / Modification / Rejection |
| :--- | :--- | :--- | :--- |
| **1. Planning** | Read initial repository files (`AGENTS.md`, `README.md`) and proposed a structured multi-phase execution sequence. | Deciding on final project scope and data handling strategies. | **Accepted**: Build sequence and phase layout. <br>**Modified**: Rejected Great Expectations in favor of a lightweight custom validator to avoid dependency bloat. |
| **2. Architecture Design** | Formulated modular structure and generated sequence/system diagrams in Mermaid. Verified stack compatibility against official documentation. | Confirming the separation of deterministic transformations and probabilistic LLM tasks. | **Accepted**: Zero LLM involvement in change detection. <br>**Modified**: Replaced DuckDB with Polars for temporal checks due to rowid instability. |
| **3. SCD2 Logic Design** | Generated core delta-checking logic (`detect_changes.py`) and historical row handling (`transform_scd2.py`). | Specifying key handling rules, daily granularity date casting, and soft-delete behavior. | **Accepted**: Tuple-based business keys.<br>**Modified**: Enabled user-configurable processing dates for historical simulation. |
| **4. Validation Logic** | Generated assertions checking duplicates, null values, schema completeness, and date overlap boundary conditions. | Establishing strict definitions for overlapping validity dates. | **Accepted**: 5 core integrity rules.<br>**Modified**: Ported DuckDB SQL queries to Polars expressions to resolve query execution binder failures. |
| **5. UI/UX Design** | Created CSS definitions for a dark theme and mapped 12 color tokens to UI components. | Defining the visual identity as an operational console rather than a consumer landing page. | **Accepted**: Dark mode color tokens.<br>**Modified**: Replaced colored emojis with inline SVG monoline icons for clean typography. |
| **6. Streamlit Development** | Structured layouts, file upload controls, data tables, and download interfaces. | Designing layout structure and implementing configuration screens. | **Accepted**: Session state persistence for run history.<br>**Modified**: Replaced deprecated `use_container_width=True` with `width="stretch"` for data tables. |
| **7. LLM Integration** | Created prompts requesting explanations of changed records. Generated Pydantic validation schemas. | Defining the explanation style and selecting which columns are monitored. | **Accepted**: Gemini JSON schema-constrained response format.<br>**Modified**: Combined changes into a single batch call to reduce API cost. |
| **8. Provider Fallback Design** | Structured fallback routing flow through different providers and offline engines. | Selecting Groq as the secondary provider and writing template strings for offline mode. | **Accepted**: Gemini → Groq → Template fallback chain.<br>**Modified**: Enabled partial record-by-record fallback for missing JSON IDs. |
| **9. Testing** | Generated unit, integration, and composite key test cases. Created a property-based test generator. | Establishing boundary testing values and defining mock behaviors. | **Accepted**: Mocking live network calls for pytest runs. <br>**Modified**: Added comprehensive security injection test cases. |
| **10. Performance Optimization** | Developed execution time and memory tracking scripts to analyze system performance on datasets from 1K to 100K rows. | Defining the practical limits for interactive web execution. | **Accepted**: Linear scaling profiles. <br>**Modified**: Highlighted Python-loop dictionary conversions as a future vectorization target. |
| **11. Documentation** | Generated draft layout and contents for briefs, logs, demo scripts, and reports. | Reviewing generated text for accuracy against the codebase. | **Accepted**: All markdown reports in `docs/`. |
| **12. Deployment Preparation** | Defined Python environments, dependency lists, and secret loader paths. | Setting deployment target as Streamlit Community Cloud and managing API keys. | **Accepted**: Secrets vault lookup structure. <br>**Modified**: Dropped Docker containerization requirement. |
| **13. Enterprise Readiness** | Integrated Prefect `@flow` and `@task` wrappers. Designed a trust score calculation formula. | Defining variables and weights for calculating operational confidence. | **Accepted**: Formula integrating validation results and model quality. |

---

## 2. What AI Helped With

The AI assistant acted as a development accelerator across the following specific domains:
* **Architecture Planning & Project Structuring**: Proposed package layout and created file scaffolds under `src/scd2_copilot/` and `app/`.
* **Streamlit UI Generation & Enterprise Redesign**: Generated a unified dark theme stylesheet (`dashboard_theme.css`) implementing a premium 12-token palette and replaced native emojis with custom SVG icon mappings.
* **Validation Framework & Testing**: Wrote 154 unit, integration, and security tests. Created a property-based test script (`run_saturation_audit.py`) that successfully ran the pipeline over 1,000 randomized datasets.
* **Prompt Engineering & LLM Integration**: Formulated structured system prompts and JSON schemas to request batch descriptions, reducing API token costs by 90% and ensuring deterministic parser matching.
* **Performance Benchmark Planning**: Wrote load testing tools to measure execution runtime and peak memory usage across scale.
* **Documentation & Report Generation**: Authored clear logs, data contracts, deployment notes, and the master compliance report.

---

## 3. What AI Got Wrong

Several issues occurred during AI-assisted development that required manual correction:
* **DuckDB SQL RowID Binder Failure**: The AI initially wrote the temporal overlap validation check using DuckDB SQL querying over Polars dataframes. This query failed at runtime because Polars dataframes in memory do not expose stable `rowid` values to DuckDB. The check was manually rewritten in pure Polars expressions.
* **Expander Typography Corruption**: The AI implemented a global font override in CSS that inadvertently corrupted Streamlit's default collapse icons, resulting in raw text fragments like `_arrowright_` and `_arrowReight_` displaying inside accordion headers. This was resolved by refining CSS selector isolation.
* **File Uploader Visual Clash**: The AI's initial dashboard theme left the inner dropzone divs of the file uploader white, causing a bright white block to stand out in the dark-themed dashboard. This was manually corrected by targeting specific Streamlit file uploader CSS classes.
* **Same-Day Modification Collision**: In early SCD2 transformation iterations, the AI did not account for multiple updates occurring on the same processing date. This led to duplicate rows in the output instead of overwriting the active record. This was resolved by checking if `effective_from` matched the processing date.
* **Environment Assessment Errors**: During initial repo analysis, the AI inaccurately classified Streamlit as "broken" because of a minor metadata packaging error in the local virtual environment. It also incorrectly reported that PySpark was uninstalled, failing to recognize it was a system-level install outside the venv.

---

## 4. Best Prompts Used

### Architecture
> **Prompt**: "Recheck all stack choices against current official docs. Confirm google-genai vs google-generativeai. Update requirements.txt, all docs, scaffolding. Keep SCD2 deterministic."
* **Value**: Ensured the project avoided using deprecated SDKs and selected `google-genai` (v2.8.0) for unified Gemini integration.
* **Outcome**: Standardized dependencies, preventing library migration issues.

### SCD2 Logic
> **Prompt**: "Write a slowly changing dimension Type 2 transformer in transform_scd2.py that takes source and target DataFrames, closes existing active versions by updating effective_to and is_current, and inserts new records. Ensure that historical records are preserved untouched."
* **Value**: Provided a decoupled, clean implementation of SCD2 merging using Polars operations.
* **Outcome**: A deterministic transform engine passing all logical tests.

### Testing
> **Prompt**: "Create a property-based test runner that generates 1,000 randomized source and target datasets with multiple records, executing them through the change detector, transformer, and validation suite. Check for row leakage, chronological integrity, and current record uniqueness."
* **Value**: Verified the stability and correctness of the pipeline across tens of thousands of mock records.
* **Outcome**: Identified and proved the reliability of the date overlap checks.

### Validation
> **Prompt**: "Write validation rules to check that there is only one current record per key, no overlapping valid date ranges, no null keys, and date consistency. Refactor any SQL query dependencies into pure Polars expression chains."
* **Value**: Eliminated the unstable DuckDB rowid dependency.
* **Outcome**: Fast, local, and reliable validation execution.

### UI/UX
> **Prompt**: "Create a dark enterprise theme stylesheet for Streamlit using background #0B1220, surface #111827, borders #243041, and accent #4F8CFF. Target file uploader dropzones, card hover states, and input fields to ensure a unified operations dashboard feel."
* **Value**: Styled custom components, ensuring high contrast and professional typography.
* **Outcome**: Replaced Streamlit's default consumer look with a premium operational dark theme.

### Enterprise Review
> **Prompt**: "Formulate a trust score calculation in python that integrates validation rule results and LLM provider quality into a single percentage. Give validation status a 80% weight and provider capability a 20% weight."
* **Value**: Exposed a clear, business-focused KPI summarizing pipeline health to operators.
* **Outcome**: Trust score widget integrated successfully on the dashboard overview.

### Performance
> **Prompt**: "Generate a benchmarking script that creates synthetic tables of sizes 1K, 10K, 25K, 50K, and 100K rows, measuring execution time and peak memory footprint. Output the metrics in a clean markdown table."
* **Value**: Provided a realistic scalability map showing linear scaling properties.
* **Outcome**: Documented benchmark results confirming that 100K records process in 7.58s under 129MB RAM.

### Final Audit
> **Prompt**: "Review all project brief files, business rules, and source code. Generate a master saturation audit report detailing logical verdicts, edge cases, vulnerabilities, and a list of 50 tough technical questions simulating a technical review panel."
* **Value**: Acted as an adversarial tester challenging the application's correctness.
* **Outcome**: Generated the comprehensive audit log (`report_test_final.md`) proving the system is production-ready.

---

## 5. Prompt Documentation

| Date / Phase | Purpose | Result |
| :--- | :--- | :--- |
| **2026-06-08 (Planning)** | Analyze repository files, check environments, and propose a detailed development roadmap. | Scaffolding and phased plan approved. Great Expectations swapped for lightweight validator. |
| **2026-06-08 (Scaffolding)** | Perform stack audit, verify API SDK packages, and generate folder scaffold. | Scaffolds created. Packages pinned to `google-genai` and `pydantic-settings`. |
| **2026-06-08 (Core Development)** | Build deterministic Polars-based change detection and SCD2 transformation routines. | Implementations created in `detect_changes.py` and `transform_scd2.py`. |
| **2026-06-08 (Validation)** | Implement 5 data validation checks checking overlaps, null keys, and duplicates. | Ported DuckDB checks to pure Polars to fix runtime binder issues. |
| **2026-06-09 (UI Redesign)** | Redesign Streamlit application to use custom CSS themes, layout columns, and tabs. | Dark operations dashboard created; sidebar replaced with inline settings workspace. |
| **2026-06-09 (UI Polish)** | Remove colored emojis and replace them with monoline SVG icons. Fix CSS expander corruption. | Visual rendering bugs resolved. Typography and theme verified clean. |
| **2026-06-09 (Audit & Audit suite)** | Build adversarial test suites, run property tests, and generate performance scalability benchmarks. | 154 passing tests confirmed. 1,000 property-test runs passed. Performance scalability cataloged. |

---

## 6. AI Contribution Assessment

* **Planning**: **~75%** (AI drafted structure and checklists; human refined scope and tool selection).
* **Coding**: **~80%** (AI generated core templates, css layouts, and test structures; human verified algorithms and refactored logic).
* **Testing**: **~85%** (AI generated exhaustive test suites, mocks, and property-test runners; human directed boundary parameters).
* **Documentation**: **~90%** (AI compiled markdown logs and reports based on codebase queries; human reviewed details).
* **Human Validation**: **Required** (Code reviews, boundary overrides, and manual UI verification).

---

## 7. Final Project Maturity Assessment

* **Business Readiness**: **Excellent**. Core SCD2 logical states (New, Changed, Unchanged, Deleted) and soft-deletes are handled deterministically.
* **Enterprise Readiness**: **High**. Coupled with Prefect for ETL monitoring, and outputs are fully compatible with Snowflake or BigQuery. Lacks native multi-user RBAC or database connection forms in the UI.
* **Technical Quality**: **Excellent**. Deterministic data transformations are strictly decoupled from LLM tasks.
* **Maintainability**: **High**. Modular design with strict type-safety and standard dependency constraints.
* **Test Coverage**: **Excellent**. 154 tests covering edge cases, duplicate scenarios, and property validations.
* **Documentation Quality**: **Excellent**. Comprehensive logs, data contracts, and audit reports exist in `docs/`.

### Strengths
1. **Perfect Decoupling**: Database changes are evaluated by local Polars code, completely eliminating hallucination risk.
2. **High Token Efficiency**: Batching changed records and using JSON schemas minimizes LLM runtime costs.
3. **Resilient Fallback**: Multiple providers and local templates guarantee application execution during API outages.

### Remaining Limitations
1. **Row-Loop Hotspot**: Rebuilding output dataframes from row dictionaries (`apply_scd2` step 6) is CPU-bound. For datasets exceeding 250K rows, a vectorized join-based rewrite is recommended.
2. **Interactive UI Memory Ceiling**: Large CSV displays may cause browser rendering lag in Streamlit.