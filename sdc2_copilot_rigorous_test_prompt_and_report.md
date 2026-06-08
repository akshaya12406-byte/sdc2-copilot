# Rigorous Test Prompt and Preliminary Report Scaffold for `sdc2-copilot`

> **Important note**
> This file is a testing prompt plus a report scaffold. It is designed to be run against the repository by an agent that has direct code access. I cannot fully verify the entire codebase from the screenshot alone.

## 1) Deep Rigorous Testing Prompt

Use this prompt in your agentic coding tool:

```text
You are auditing the entire `sdc2-copilot` application for correctness, reliability, efficiency, and judge-readiness.

Your job is not to make small patches. Your job is to deeply test the full system, uncover hidden logical errors, and iterate until every meaningful test passes.

Hard requirements:
1. Inspect the complete codebase end-to-end:
   - UI layer
   - upload/parsing layer
   - schema detection
   - SCD2 transformation logic
   - validation rules
   - LLM prompt construction
   - LLM response parsing
   - fallback behavior
   - reporting/output formatting
   - caching / retries / error handling
   - token and API usage paths

2. Build a full test strategy that includes:
   - unit tests
   - integration tests
   - property-based tests if helpful
   - edge-case tests
   - regression tests for known bugs
   - performance checks
   - prompt quality checks
   - judge-expectation checks

3. Test the best-to-worst possible scenarios:
   - fully valid input
   - single-row input
   - duplicate business keys
   - duplicate current rows
   - missing columns
   - wrong column names
   - extra irrelevant columns
   - null values in business keys
   - null effective_from
   - null effective_to
   - overlapping SCD2 periods
   - same-day changes
   - out-of-order rows
   - repeated identical snapshots
   - deleted/missing records between snapshots
   - malformed CSVs
   - type coercion issues
   - timezone/date-format inconsistencies
   - empty files
   - extremely large files
   - unicode / special characters
   - mixed data types in the same column
   - reruns with the same inputs
   - partial failures mid-pipeline
   - LLM timeout / invalid JSON / low-confidence responses
   - API rate-limit errors
   - provider fallback failures

4. Validate the business logic, not just the code path:
   - SCD2 rules are correct
   - historical versions are preserved correctly
   - current row logic is correct
   - unchanged rows stay unchanged
   - changed rows close the previous version and open a new one
   - new rows create a fresh version
   - deleted rows are handled explicitly or intentionally excluded
   - validation messages are deterministic and actionable
   - no silent WARN fallback where FAIL is required

5. Deeply test the no-overlapping-dates logic:
   - no hidden overlaps
   - no false positives
   - no false negatives
   - no dependence on unstable SQL row identifiers
   - verify output for each business key independently
   - verify consecutive-period comparison
   - verify open-ended current rows
   - verify rows with identical timestamps
   - verify one-row history and multi-row history
   - verify NULL handling is deterministic

6. Verify the LLM layer:
   - ensure the LLM is only used where deterministic logic is insufficient
   - ensure prompts are short, structured, and stable
   - ensure prompts do not waste tokens
   - ensure outputs are constrained to the desired schema
   - ensure invalid/empty responses are handled gracefully
   - ensure confidence scoring is meaningful and not cosmetic
   - ensure LLM explanations match the underlying detected change exactly
   - ensure hallucinated reasons are not shown to the user

7. Audit all external calls:
   - count every API call path
   - identify unnecessary calls
   - identify repeated calls that can be cached
   - identify prompt text that can be shortened
   - identify duplicated model calls for the same record set
   - identify whether deterministic checks are incorrectly delegated to the LLM
   - identify whether the app can batch explanations instead of one call per row
   - identify whether a local model-free fallback is possible

8. Iterate until done:
   - run tests
   - fix failures
   - rerun tests
   - repeat until all critical tests pass
   - do not stop at the first green run
   - prove that edge cases are handled
   - prove that regressions are covered

9. Output format:
   Produce a final report with:
   - root causes found
   - files changed
   - tests added
   - tests passed / failed
   - remaining risks
   - token and API efficiency findings
   - reliability findings
   - judge-readiness assessment
   - business value assessment
   - final verdict

10. Acceptance criteria:
   - no silent validation warnings for known deterministic checks
   - no brittle SQL row-identifier logic
   - no hidden overlap bugs
   - no unnecessary LLM calls
   - no excessive token usage
   - no incorrect explanations
   - no unstable behavior on reruns
   - output must be deterministic, auditable, and judge-ready
```

## 2) Suggested Deep Test Matrix

### Core SCD2 correctness
- change detection on one field
- multiple fields changing at once
- unchanged rows
- newly added business key
- deleted business key
- reopened business key after deletion
- same business key across many versions

### Validation correctness
- schema completeness
- one current row per key
- null business keys
- date consistency
- overlap detection
- duplicate current rows
- duplicate source rows
- invalid/ambiguous date ranges

### Input robustness
- empty CSV
- one-row CSV
- missing headers
- reordered columns
- extra columns
- malformed dates
- mixed types
- unicode and special characters
- large datasets
- file encoding issues

### LLM quality
- explanation matches actual change
- explanation does not invent causes
- prompt stays concise
- output format is stable
- low-confidence outputs are flagged
- invalid JSON is handled
- timeout and retry behavior are tested

### Performance / efficiency
- no repeated deterministic LLM calls
- cache repeated schema inspections
- batch explanations where possible
- avoid sending full tables to the LLM
- limit context to only changed rows and relevant metadata
- measure latency and token cost per run

## 3) Efficiency Review Checklist

A good implementation should keep deterministic work local and reserve the LLM for explanation or summarization only. That is usually the right pattern for validation-heavy pipelines because local validation is cheaper, easier to test, and more reliable. Polars supports sorting by columns and row iteration with named dictionaries, which makes local overlap checks practical, and pytest fixtures are intended to provide stable, repeatable test contexts. DuckDB is an in-process analytical database, while OpenRouter offers a unified API with fallback routing and a free-model router; Groq focuses on fast, low-cost inference. Those facts support an architecture where deterministic validation stays local and model calls are minimized. citeturn766280search1turn766280search6turn766280search22turn766280search23turn766280search18turn766280search4turn766280search10

### Efficiency improvements to check
- cache parsed schema and inferred business keys
- compute deterministic validations before any LLM call
- call the LLM only for changed / ambiguous / user-facing explanation work
- batch explanations into one prompt per change set instead of one prompt per row
- cap prompt size and remove repeated context
- deduplicate identical records before explanation
- add retries only around transient provider errors
- record token counts, latency, and fallback usage
- use a confidence threshold to suppress weak explanations

## 4) Preliminary Findings Based on Current Evidence

These are the only points that can be treated as verified from the conversation so far:

- The old `no_overlapping_dates` path was failing because DuckDB did not expose `rowid` on the registered dataframe in the way the query expected, which produced a Binder Error. DuckDB’s documentation describes it as an in-process analytical database, and the tested command reproduced the binder failure directly. citeturn766280search5turn766280search10
- The switch to a local deterministic overlap scan is conceptually sound because Polars can sort by keys and let you iterate rows by name, which is enough to compare adjacent records per business key. citeturn766280search1turn766280search6
- Test stability should rely on fixtures with fixed in-memory datasets rather than fragile workspace files; pytest fixtures are designed to provide reliable and consistent context. citeturn766280search22turn766280search12
- For model routing, OpenRouter’s unified API and fallback routing can reduce provider lock-in, while Groq is optimized for fast, low-cost inference. That matters if the app needs both reliability and speed. citeturn766280search18turn766280search23turn766280search4turn766280search8

## 5) Final Report Template

Create a test_report.md file to store the test results.
as mentioned below and run the tests to fill the report.

### Scope
- application modules tested:
- validations tested:
- LLM paths tested:
- performance paths tested:

### Bugs Found
1. 
2. 
3. 

### Fixes Applied
1. 
2. 
3. 

### Tests Added
1. 
2. 
3. 

### Test Results
- passed:
- failed:
- flaky:
- blocked:

### Efficiency Findings
- unnecessary API calls:
- duplicated prompts:
- token-heavy prompts:
- caching opportunities:
- batching opportunities:

### Business Value Assessment
- problem solved:
- uniqueness:
- enterprise value:
- judge-readiness:

### Final Verdict
- production readiness:
- demo readiness:
- remaining risks:
- next steps:

## 6) Bottom-Line Recommendation

Treat deterministic SCD2 logic as code to be proven by tests, not as behavior to be inferred from LLM output. Use the LLM only for explanation, summarization, and human-friendly context; keep validation, overlap checks, and row versioning local and deterministic. That gives you better speed, lower cost, easier debugging, and stronger judge confidence. 
