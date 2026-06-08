# SCD2 Copilot

An AI-assisted Slowly Changing Dimension Type 2 (SCD2) builder that:
- accepts a source CSV and yesterday's SCD2 CSV
- generates the updated SCD2 table
- validates correctness
- explains every change using an LLM

## Why this exists
Enterprise teams repeatedly hand-code SCD2 logic. This project automates the repetitive parts while keeping correctness deterministic.

## Stack
- Streamlit
- Prefect
- Polars
- DuckDB
- Great Expectations
- Gemini / Groq / OpenRouter
- Google Antigravity for development

## Project Structure
See `docs/architecture.md`

## Setup
1. Create a virtual environment
2. Install dependencies
3. Add API keys to `.env`
4. Run the app

## Run
```bash
streamlit run app/streamlit_app.py