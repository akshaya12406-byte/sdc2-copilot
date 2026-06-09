# Streamlit UI Redesign Plan

## 1) UI goal

Turn the app into an **internal enterprise data operations dashboard**.

The UI should feel like:

* a serious business tool
* an audit console
* a data workflow control panel

Not like:

* a hackathon page
* a flashy demo
* a consumer SaaS landing screen

---

## 2) Exact page sections

### A. Top header

Show:

* app name
* short subtitle
* current processing date
* current provider status
* pipeline status badge

### B. KPI summary strip

Show four to six compact cards:

* New records
* Changed records
* Unchanged records
* Deleted records
* Validation status
* Execution time

Optional extra cards:

* API available
* Model used
* Token usage
* Trust score

### C. Input workspace

Show:

* source CSV uploader
* target CSV uploader
* processing date picker
* business key selector
* tracked columns selector
* delete policy selector

### D. Run controls

Show:

* Run pipeline button
* Reset session button
* Download config / input mapping button if needed

### E. Results workspace as tabs

Use tabs for:

1. Overview
2. Updated SCD2 Table
3. Validation
4. Change Explanations
5. Data Explorer
6. Run History / Audit

### F. Hidden advanced panel

Show only when expanded:

* raw prompt
* raw LLM response
* token details
* fallback path
* schema debug info
* internal warnings
* execution logs

---

## 3) Component order

Use this exact order in the main page:

1. Title + subtitle
2. KPI strip
3. Input/upload area
4. Schema detection area
5. Run button
6. Status / success / error banner
7. Tabs for outputs
8. Download area
9. Advanced details expander

This order matters because it gives the user a clean flow:
**setup → run → inspect → validate → explain → download**.

---

## 4) Color tokens

Use a dark enterprise palette with restrained accents.

### Core palette

* Background: `#0B1220`
* Surface 1: `#111827`
* Surface 2: `#1F2937`
* Border: `#243041`
* Primary accent: `#4F8CFF`
* Success: `#22C55E`
* Warning: `#F59E0B`
* Error: `#EF4444`
* Info: `#38BDF8`
* Text primary: `#E5E7EB`
* Text secondary: `#94A3B8`
* Muted text: `#64748B`

### UI style rules

* Use one primary accent only.
* Use semantic colors only for status.
* Avoid neon colors.
* Avoid rainbow charts.
* Keep contrast high.
* Keep spacing generous.
* Use rounded cards and subtle shadows only.

---

## 5) Layout wireframe

### Recommended screen structure

```text
┌──────────────────────────────────────────────────────────────────────┐
│ SCD2 Copilot                                                         │
│ AI-assisted Slowly Changing Dimension Type 2 builder                │
│ [Processing Date] [Provider Status] [Pipeline Status]               │
├──────────────────────────────────────────────────────────────────────┤
│ KPI Cards: New | Changed | Unchanged | Deleted | Validation | Time   │
├──────────────────────────────────────────────────────────────────────┤
│ Input & Settings                                                     │
│ [Source CSV]   [Target CSV]                                          │
│ [Business Key] [Tracked Columns]                                     │
│ [Processing Date] [Delete Policy]                                    │
│ [Run Pipeline]                                                       │
├──────────────────────────────────────────────────────────────────────┤
│ Tabs: Overview | Updated Table | Validation | Explanations | Explorer│
├──────────────────────────────────────────────────────────────────────┤
│ Download buttons                                                     │
├──────────────────────────────────────────────────────────────────────┤
│ Advanced details (collapsed by default)                              │
└──────────────────────────────────────────────────────────────────────┘
```

---

## 6) What each panel should show

### Overview tab

Show:

* run summary
* selected key
* selected tracked columns
* row counts
* processing duration
* validation result
* provider used
* trust score

### Updated SCD2 Table tab

Show:

* the full output table
* filters for business key and row type
* row count
* optional sort by key or date

### Validation tab

Show:

* rule-by-rule status
* pass/fail badge
* explanation for each rule
* issue table if any rule fails

### Change Explanations tab

Show:

* collapsible cards by change type
* one explanation per record
* provider label
* confidence / trust score per explanation
* fallback warning if applicable

### Data Explorer tab

Show:

* source preview
* target preview
* changed records only
* deleted records only
* schema preview
* row-level diff view

### Run History / Audit tab

Show:

* timestamp
* file names
* row counts
* provider
* tokens used
* validation status
* downloadable run artifact

---

## 7) What should be hidden by default

These should be hidden behind expanders or advanced tabs:

* raw prompt text
* raw model response
* token-by-token diagnostics
* provider fallback chain internals
* debug logs
* schema inference scoring details
* internal config dumps
* stack traces unless an error occurs
* hidden file paths
* low-level execution metadata

### Reason

These are useful for debugging, but they should not clutter the main product flow.

---

## 8) UX upgrades that matter most

### Add these immediately

* top KPI cards
* trust score
* model/provider status
* execution time
* clear success/error banners
* download bundle section
* row-level diff explorer
* collapsible advanced panel

### Add later if time permits

* run history timeline
* change trend chart
* validation trend chart
* per-run cost summary
* explanation quality score
* key/column selection confidence

---

## 9) Should the CSV output be displayed better?

Yes.

The output table should not just be shown as a raw dataframe.

## Better presentation options

* a dedicated **Updated Table** tab
* default sort by business key and date
* row type badges: NEW / CHANGED / CURRENT / CLOSED
* a compact “changed rows only” view
* a “download” panel beside the preview
* a row detail expander for one selected key

### Best practice

Show:

* summary first
* table second
* row-level detail last

That makes the output easier to understand.

---

## 10) Should you add a dedicated CSV viewer / data explorer?

**Yes, but keep it lightweight inside Streamlit.**

You do not need a heavy external viewer right now.

### Best Streamlit-friendly approach

Create a dedicated **Data Explorer** tab with:

* source preview
* target preview
* output preview
* changed rows only
* deleted rows only
* schema view
* row-level inspection

### Why this is enough

It gives you:

* clarity
* structure
* business feel
* faster implementation
* lower risk

### When to use a more advanced grid

Only if you later want:

* paging
* column pinning
* advanced filtering
* spreadsheet-like editing

For now, Streamlit native tables are sufficient if organized well.

---