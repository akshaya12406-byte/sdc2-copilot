# Acceptance Criteria

The project is accepted only if all of the following are true:

1. The app accepts a source CSV and a target SCD2 CSV.
2. The app detects new, changed, unchanged, and missing records correctly.
3. The app generates a valid updated SCD2 table.
4. The app validates that:
   - there is only one current row per business key
   - historical date ranges do not overlap
   - duplicate business keys are detected
5. The app generates human-readable explanations for every detected change.
6. The app has a working Streamlit UI.
7. The app can be run locally.
8. The app can be deployed publicly.
9. The repo contains tests.
10. The repo contains prompt logs and an AI usage note.
11. The repo contains sample input and expected output data.
12. The README explains setup, run steps, architecture, assumptions, and limitations.