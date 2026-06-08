"""SCD2 Copilot — Streamlit UI.

Upload source and target CSVs, run the SCD2 pipeline, view results,
and download outputs.
"""

from __future__ import annotations

import sys
from datetime import date
from pathlib import Path

import streamlit as st
import polars as pl

# Add project root to path so src package is importable
_project_root = Path(__file__).resolve().parent.parent
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))

from src.scd2_copilot.config import get_settings, LLMProvider
from src.scd2_copilot.ingestion import load_csv, validate_csv_columns
from src.scd2_copilot.schema import detect_business_key, detect_tracked_columns
from src.scd2_copilot.detect_changes import detect_changes
from src.scd2_copilot.transform_scd2 import apply_scd2
from src.scd2_copilot.validate import validate_scd2
from src.scd2_copilot.explain import explain_changes
from src.scd2_copilot.models import ValidationStatus

# ── Page Config ────────────────────────────────────────
st.set_page_config(
    page_title="SCD2 Copilot",
    page_icon="🔄",
    layout="wide",
)

st.title("🔄 SCD2 Copilot")
st.caption("AI-assisted Slowly Changing Dimension Type 2 builder")


# ── Sidebar: Settings ─────────────────────────────────
with st.sidebar:
    st.header("⚙️ Settings")

    processing_date = st.date_input(
        "Processing Date",
        value=date.today(),
        help="The date to stamp on new/changed rows (effective_from).",
    )

    # Load settings to check available keys
    settings = get_settings()

    # Build provider options with availability hints
    provider_options = ["template"]
    provider_labels = {"template": "🔧 Template (offline, no API key)"}

    if settings.has_gemini_key:
        provider_options.insert(0, "gemini")
        provider_labels["gemini"] = "✅ Gemini (API key configured)"
    else:
        provider_options.append("gemini")
        provider_labels["gemini"] = "❌ Gemini (no API key in .env)"

    if settings.has_groq_key:
        provider_options.insert(1 if "gemini" in provider_options[:1] else 0, "groq")
        provider_labels["groq"] = "✅ Groq (API key configured)"
    else:
        provider_options.append("groq")
        provider_labels["groq"] = "❌ Groq (no API key in .env)"

    # Default to gemini if key available, else template
    default_idx = 0 if settings.has_gemini_key else provider_options.index("template")

    llm_choice = st.selectbox(
        "LLM Provider",
        options=provider_options,
        index=default_idx,
        format_func=lambda x: provider_labels.get(x, x),
        help="Choose the explanation engine. 'template' works without API keys.",
    )

    st.divider()
    st.markdown(
        "**SCD2 Copilot** detects changes deterministically. "
        "The LLM only explains — it never decides."
    )


# ── File Upload ────────────────────────────────────────
st.header("📁 Upload Data")

col1, col2 = st.columns(2)

with col1:
    source_file = st.file_uploader(
        "Source CSV (today's data)",
        type=["csv"],
        key="source_upload",
        help="Upload today's full snapshot CSV.",
    )

with col2:
    target_file = st.file_uploader(
        "Target CSV (yesterday's SCD2 table)",
        type=["csv"],
        key="target_upload",
        help="Upload yesterday's SCD2 table with effective_from, effective_to, is_current columns.",
    )


# ── Pipeline Execution ────────────────────────────────
if source_file and target_file:
    try:
        source_df = load_csv(source_file)
        target_df = load_csv(target_file)
    except Exception as e:
        st.error(f"❌ Error loading CSVs: {e}")
        st.stop()

    # Validate CSV compatibility
    errors = validate_csv_columns(source_df, target_df)
    if errors:
        for err in errors:
            st.error(f"❌ {err}")
        st.stop()

    # Detect schema
    try:
        business_key = detect_business_key(source_df, target_df)
        tracked_columns = detect_tracked_columns(source_df, business_key)
    except ValueError as e:
        st.error(f"❌ Schema detection error: {e}")
        st.stop()

    # Show detected schema
    st.subheader("🔑 Detected Schema")
    col_a, col_b = st.columns(2)
    with col_a:
        bk_override = st.multiselect(
            "Business Key",
            options=source_df.columns,
            default=business_key,
            help="Auto-detected business key. Override if needed.",
        )
    with col_b:
        st.write("**Tracked Columns:**", tracked_columns)

    if bk_override:
        business_key = bk_override
        tracked_columns = detect_tracked_columns(source_df, business_key)

    # Run pipeline button
    if st.button("🚀 Run SCD2 Pipeline", type="primary", use_container_width=True):
        with st.spinner("Running pipeline..."):
            # Override LLM provider from sidebar selection
            settings.llm_provider = LLMProvider(llm_choice)

            # Step 1: Detect changes
            change_report = detect_changes(
                source_df, target_df, business_key, tracked_columns, processing_date
            )

            # Step 2: Transform
            scd2_output = apply_scd2(
                source_df, target_df, change_report,
                business_key, tracked_columns, processing_date
            )

            # Step 3: Validate
            validation_report = validate_scd2(scd2_output, business_key)

            # Step 4: Explain (now returns ExplainResult with warnings)
            explain_result = explain_changes(change_report, settings=settings)
            explanations = explain_result.explanations

        # ── Results Display ────────────────────────────
        st.success("✅ Pipeline completed!")

        # Show LLM provider warnings (e.g. fallback to template)
        for warning in explain_result.warnings:
            st.warning(warning)

        # Change Summary
        st.subheader("📊 Change Summary")
        summary = change_report.summary
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("New", summary["new"])
        m2.metric("Changed", summary["changed"])
        m3.metric("Unchanged", summary["unchanged"])
        m4.metric("Deleted", summary["deleted"])

        # Updated SCD2 Table
        st.subheader("📋 Updated SCD2 Table")
        st.dataframe(scd2_output.to_pandas(), use_container_width=True)

        # Validation Report
        st.subheader("✅ Validation Report")
        for rule in validation_report.rules:
            if rule.status == ValidationStatus.PASS:
                st.markdown(f"✅ **{rule.name}**: {rule.message}")
            elif rule.status == ValidationStatus.FAIL:
                st.markdown(f"❌ **{rule.name}**: {rule.message}")
                for detail in rule.details:
                    st.caption(f"  → {detail}")
            else:
                st.markdown(f"⚠️ **{rule.name}**: {rule.message}")

        # Explanations
        st.subheader("💬 Change Explanations")
        if explanations:
            for exp in explanations:
                key_str = ", ".join(f"{k}={v}" for k, v in exp.business_key_values.items())
                icon = "🤖" if exp.provider != "template" else "🔧"
                with st.expander(f"{icon} {exp.change_type.value.upper()} — {key_str}"):
                    st.write(exp.text)
                    st.caption(f"Provider: {exp.provider}")
        else:
            st.info("No changes to explain.")

        # Downloads
        st.subheader("📥 Downloads")
        csv_data = scd2_output.write_csv()
        st.download_button(
            label="⬇️ Download Updated SCD2 Table (CSV)",
            data=csv_data,
            file_name="scd2_output.csv",
            mime="text/csv",
            use_container_width=True,
        )

else:
    st.info("👆 Upload both source and target CSV files to begin.")
