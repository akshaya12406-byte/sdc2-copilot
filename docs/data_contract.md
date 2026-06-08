# Data Contract

## Input 1: Source CSV

Represents today's **full snapshot** of the entity table.

### Expected columns
- **Business key column(s)**: e.g., `customer_id`, `employee_id` — identifies the entity uniquely
- **Tracked attribute columns**: e.g., `name`, `city`, `tier`, `department` — columns monitored for changes
- **Optional metadata columns**: will be ignored during change detection

### Example
```csv
customer_id,name,city,tier
101,Ravi,Bengaluru,Gold
102,Priya,Mumbai,Silver
103,Arun,Delhi,Gold
104,Kiran,Hyderabad,Bronze
```

### Constraints
- Business key must be unique in the source (duplicates trigger a validation error)
- No SCD2 metadata columns (`effective_from`, `effective_to`, `is_current`) should be present
- Empty source is valid (means all target records become soft-deleted)

---

## Input 2: Target CSV

Represents yesterday's **SCD2 table** (may contain historical and current rows).

### Expected columns
- Business key column(s) — must match the source
- Tracked attribute columns — must match the source
- `effective_from` — date the row became active (ISO format `YYYY-MM-DD`)
- `effective_to` — date the row was closed (empty/null for current rows)
- `is_current` — boolean flag (`true` / `false`)

### Example
```csv
customer_id,name,city,tier,effective_from,effective_to,is_current
101,Ravi,Chennai,Gold,2026-06-07,,true
102,Priya,Mumbai,Silver,2026-06-07,,true
103,Arun,Delhi,Gold,2026-06-07,,true
```

### Constraints
- May contain multiple rows per business key (historical + current)
- Only `is_current=true` rows participate in change detection
- Empty target is valid (means all source records are new inserts)

---

## SCD2 Column Constants

These column names are reserved and auto-detected:

| Column | Type | Description |
|--------|------|-------------|
| `effective_from` | `date` (YYYY-MM-DD) | Date the row became active |
| `effective_to` | `date` or null | Date the row was closed |
| `is_current` | `bool` | Whether this is the active version |

---

## SCD2 Transform Rules

| Scenario | In Source? | Current in Target? | Action |
|----------|-----------|-------------------|--------|
| **NEW** | ✅ Yes | ❌ No | Insert: `effective_from=today, effective_to=null, is_current=true` |
| **CHANGED** | ✅ Yes | ✅ Yes, values differ | Close old: `effective_to=today, is_current=false`. Insert new: `effective_from=today, effective_to=null, is_current=true` |
| **UNCHANGED** | ✅ Yes | ✅ Yes, values match | Keep existing row as-is |
| **DELETED** | ❌ No | ✅ Yes | Close: `effective_to=today, is_current=false` (soft delete) |

---

## Date Rules

- `effective_from` = processing date (default: `date.today()`, user-overridable)
- `effective_to` = processing date for rows being closed; empty/null for current rows
- Format: ISO `YYYY-MM-DD`

---

## Change Detection Rules

- Compare **only tracked columns** (not keys, not SCD2 metadata)
- Use **field-by-field comparison** (not hashing) to identify *which* fields changed
- Only compare against `is_current=true` rows in the target
- Historical rows (`is_current=false`) are always preserved unchanged

---

## Output Contract

The system outputs:

| Output | Format | Description |
|--------|--------|-------------|
| Updated SCD2 table | Polars DataFrame / CSV | Full table with all historical + current rows |
| Change summary | `ChangeReport` dataclass | Counts and details of new/changed/unchanged/deleted |
| Validation report | `ValidationReport` dataclass | Pass/fail for each rule |
| Explanations | `list[Explanation]` | Human-readable description of each change |

---

## Validation Rules (Post-Transform)

1. **One current row per business key**: No key has more than one `is_current=true` row
2. **No overlapping date ranges**: Per key, `[effective_from, effective_to]` ranges don't overlap
3. **No null business keys**: Every row has a non-null business key
4. **Schema completeness**: Output has all required SCD2 columns
5. **Date consistency**: `effective_from <= effective_to` where `effective_to` is not null