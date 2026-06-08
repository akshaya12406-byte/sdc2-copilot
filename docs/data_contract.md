# Data Contract

## Input 1: Source CSV
Represents today's current state.

Expected columns:
- business_key column, such as customer_id or employee_id
- tracked attributes such as name, city, tier, department
- optional source metadata columns

Example:
customer_id,name,city,tier
101,Ravi,Chennai,Gold
102,Priya,Mumbai,Silver

## Input 2: Target CSV
Represents yesterday's SCD2 table.

Expected columns:
- business_key
- tracked attributes
- effective_from
- effective_to
- is_current
- optional surrogate key

Example:
customer_id,name,city,tier,effective_from,effective_to,is_current
101,Ravi,Chennai,Gold,2026-06-07,,true
102,Priya,Mumbai,Silver,2026-06-07,,true

## SCD2 Rules
- New record: insert with effective_from = today, effective_to = null, is_current = true
- Changed record: close old row and insert a new current row
- Unchanged record: keep row unchanged
- Missing record: treat as soft delete or close based on configuration

## Date Rules
- effective_from = processing date
- effective_to = processing date for the row being closed
- use ISO date format YYYY-MM-DD

## Key Rules
- Business key must identify the entity
- Business key should be unique in source
- Duplicate keys should trigger validation failure

## Change Detection Rules
- Compare only the selected tracked columns
- Ignore metadata columns like effective_from and effective_to
- Use hashing or direct field comparison to detect changes

## Output Contract
The system must output:
- updated SCD2 table
- change summary
- validation report
- LLM explanation text