# Demo Script

## Opening (30 seconds)

**Say**: "SCD2 tables are used across enterprise data warehouses to track historical changes — customer addresses, employee departments, product attributes. Teams repeatedly hand-code this logic, and it's error-prone. SCD2 Copilot automates the entire process: comparison, transformation, validation, and explanation."

---

## Step 1 — Upload Files (15 seconds)

1. Open the app at the Streamlit URL
2. Upload `source_today.csv` (today's data — 4 customers)
3. Upload `target_yesterday.csv` (yesterday's SCD2 table — 3 customers)
4. **Show**: The auto-detected business key (`customer_id`) and tracked columns (`name`, `city`, `tier`)

---

## Step 2 — Run Pipeline (10 seconds)

1. Click **"Run SCD2 Pipeline"**
2. **Show**: The pipeline progress (ingest → detect → transform → validate → explain)

---

## Step 3 — Change Summary (20 seconds)

**Show the change summary panel**:
- ✅ 1 **changed** record (customer 101: city Chennai → Bengaluru)
- ✅ 2 **unchanged** records (customers 102, 103)
- ✅ 1 **new** record (customer 104: Kiran, Hyderabad, Bronze)
- ✅ 0 **deleted** records

**Say**: "Every change category is detected deterministically — no AI decides whether something changed."

---

## Step 4 — Updated SCD2 Table (15 seconds)

**Show the output table**:
- Customer 101 has two rows: old (closed) + new (current)
- Customer 102, 103 have one current row each
- Customer 104 has one new current row

**Say**: "The old row for customer 101 is closed with today's date, and a new current row is inserted. The full history is preserved."

---

## Step 5 — Validation Report (15 seconds)

**Show the validation panel**:
- ✅ One current row per business key — PASS
- ✅ No overlapping date ranges — PASS
- ✅ No null business keys — PASS
- ✅ Schema completeness — PASS
- ✅ Date consistency — PASS

**Say**: "Five validation rules run automatically to catch common SCD2 errors."

---

## Step 6 — LLM Explanations (20 seconds)

**Show the explanation cards**:
- "Customer 101 (Ravi): city changed from Chennai to Bengaluru on 2026-06-08. The previous record was closed and a new current record was created."
- "Customer 104 (Kiran): new customer added with city Hyderabad, tier Bronze on 2026-06-08."

**Say**: "The AI explains every change in plain English. But it only explains what the deterministic engine already detected — it never decides the changes."

---

## Step 7 — Download (10 seconds)

1. Click **"Download Updated SCD2 Table"** (CSV)
2. Click **"Download Full Report"** (JSON with change summary + validation + explanations)

---

## Closing (15 seconds)

**Say**: "SCD2 Copilot saves engineering time, improves auditability, and makes SCD2 understandable to business stakeholders. The deterministic engine ensures correctness, while the AI layer makes it explainable."

**Total time**: ~2.5 minutes