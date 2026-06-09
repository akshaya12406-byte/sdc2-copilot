# SCD2 Copilot - Documentation Cleanup Plan

This document outlines the consolidation and cleanup plan for all files under the `docs/` directory to prepare the repository for final hackathon submission.

---

## Documentation Classification & Cleanup Matrix

| File | Proposed Action | Target Location / Action details | Rationale |
| :--- | :---: | :--- | :--- |
| `project_brief.md` | **KEEP** | Retain under `docs/project_brief.md` | Provides critical original context and project scope. |
| `architecture.md` | **MERGE & ARCHIVE** | Merged into main `README.md`; archive original | Consolidates high-level system diagrams and modular structure in one entrypoint. |
| `data_contract.md` | **MERGE & ARCHIVE** | Merged into main `README.md`; archive original | Ensures column schema requirements are explicitly clear to developers in the main page. |
| `acceptance_criteria.md`| **MERGE & ARCHIVE** | Merged into main `README.md`; archive original | Outlines functional requirements checklist in the master README. |
| `decision_log.md` | **ARCHIVE** | Retain for developer reference | Documents early design rationale (e.g. why Prefect was chosen). |
| `prompt_log.md` | **MERGE & ARCHIVE** | Merged into main `README.md`; archive original | Highlights key AI interaction prompts in the submission overview. |
| `ai_usage_note.md` | **MERGE & ARCHIVE** | Merged into main `README.md`; archive original | Combines AI usage history and tool contribution breakdown in the README. |
| `demo_script.md` | **KEEP** | Retain under `docs/demo_script.md` | Serves as a direct testing script for judges evaluating the Streamlit GUI. |
| `limitations.md` | **MERGE & ARCHIVE** | Merged into main `README.md`; archive original | Ensures known project limits are transparently visible in the primary documentation. |
| `deployment_notes.md` | **MERGE & ARCHIVE** | Merged into main `README.md`; archive original | Consolidates environment setup and deployment commands in the README. |
| `comp_report.md` | **KEEP** | Retain under `docs/comp_report.md` | Acts as the comprehensive assessment report for repository auditors. |
| `judge_readiness_report.md` | **KEEP** | Retain under `docs/judge_readiness_report.md` | Critical Q&A script for panels and interviews. |
| `final_saturation_audit.md` | **KEEP** | Retain under `docs/final_saturation_audit.md` | Final saturation checklist confirming passing test suites and performance metrics. |
| `report_test.md` | **REMOVE** | Propose deletion | Deprecated, early validation test report. Superseded by `final_saturation_audit.md`. |
| `report_test_final.md` | **REMOVE** | Propose deletion | Redundant intermediate test audit. Replaced by `final_saturation_audit.md`. |

---

## Next Steps

1.  **Draft Master README:** Generate the unified, enterprise-grade `README.md` at the repository root.
2.  **Operator Review:** Present this cleanup plan to the user.
3.  **Action Plan Execution:** Upon explicit approval, delete `report_test.md` and `report_test_final.md`, and move the archived files to a `docs/archive/` subdirectory to keep the root `docs/` folder clean and focused.
