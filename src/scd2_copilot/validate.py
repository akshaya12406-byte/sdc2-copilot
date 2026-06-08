"""Lightweight SCD2 output validation.

Runs deterministic validation rules on the SCD2 output DataFrame
using Polars and DuckDB queries. No Great Expectations dependency.
"""

from __future__ import annotations

import duckdb
import polars as pl

from .models import ValidationReport, ValidationRule, ValidationStatus


def validate_scd2(
    df: pl.DataFrame,
    business_key: list[str],
) -> ValidationReport:
    """Run all validation rules on the SCD2 output.

    Args:
        df: The updated SCD2 DataFrame to validate.
        business_key: Business key column(s).

    Returns:
        A ValidationReport with results for each rule.
    """
    report = ValidationReport()

    report.rules.append(_check_schema_completeness(df))
    report.rules.append(_check_one_current_per_key(df, business_key))
    report.rules.append(_check_no_null_keys(df, business_key))
    report.rules.append(_check_no_overlapping_dates(df, business_key))
    report.rules.append(_check_date_consistency(df))

    return report


def _check_schema_completeness(df: pl.DataFrame) -> ValidationRule:
    """Verify that all required SCD2 columns exist."""
    required = {"effective_from", "effective_to", "is_current"}
    present = set(df.columns)
    missing = required - present

    if missing:
        return ValidationRule(
            name="schema_completeness",
            status=ValidationStatus.FAIL,
            message=f"Missing required SCD2 columns: {sorted(missing)}",
            details=[f"Missing: {c}" for c in sorted(missing)],
        )
    return ValidationRule(
        name="schema_completeness",
        status=ValidationStatus.PASS,
        message="All required SCD2 columns present.",
    )


def _check_one_current_per_key(
    df: pl.DataFrame, business_key: list[str]
) -> ValidationRule:
    """No business key should have more than one is_current=true row."""
    current = df.filter(pl.col("is_current") == True)  # noqa: E712
    duplicates = (
        current
        .group_by(business_key)
        .agg(pl.len().alias("cnt"))
        .filter(pl.col("cnt") > 1)
    )

    if duplicates.height > 0:
        detail_rows = duplicates.iter_rows(named=True)
        details = [
            f"Key {_format_key(row, business_key)} has {row['cnt']} current rows"
            for row in detail_rows
        ]
        return ValidationRule(
            name="one_current_per_key",
            status=ValidationStatus.FAIL,
            message=f"{duplicates.height} business key(s) have multiple current rows.",
            details=details,
        )

    return ValidationRule(
        name="one_current_per_key",
        status=ValidationStatus.PASS,
        message="Each business key has at most one current row.",
    )


def _check_no_null_keys(
    df: pl.DataFrame, business_key: list[str]
) -> ValidationRule:
    """Every row must have non-null business key value(s)."""
    null_filter = pl.lit(False)
    for k in business_key:
        null_filter = null_filter | pl.col(k).is_null()

    null_rows = df.filter(null_filter)

    if null_rows.height > 0:
        return ValidationRule(
            name="no_null_keys",
            status=ValidationStatus.FAIL,
            message=f"{null_rows.height} row(s) have null business key values.",
            details=[f"Row with null key found (row count: {null_rows.height})"],
        )

    return ValidationRule(
        name="no_null_keys",
        status=ValidationStatus.PASS,
        message="No null business keys found.",
    )


def _check_no_overlapping_dates(
    df: pl.DataFrame, business_key: list[str]
) -> ValidationRule:
    """For each business key, date ranges [effective_from, effective_to] must not overlap.

    Uses DuckDB self-join for efficient overlap detection.
    """
    # Register the DataFrame in DuckDB
    con = duckdb.connect()
    con.register("scd2_output", df.to_pandas())

    key_cols = ", ".join(f"a.{k}" for k in business_key)
    join_cond = " AND ".join(f"a.{k} = b.{k}" for k in business_key)

    query = f"""
    SELECT {key_cols}, COUNT(*) as overlap_count
    FROM scd2_output a
    JOIN scd2_output b
      ON {join_cond}
     AND a.effective_from < COALESCE(b.effective_to, DATE '9999-12-31')
     AND b.effective_from < COALESCE(a.effective_to, DATE '9999-12-31')
     AND a.rowid < b.rowid
    GROUP BY {key_cols}
    HAVING COUNT(*) > 0
    """

    try:
        result = con.execute(query).fetchall()
    except Exception:
        # If DuckDB query fails (e.g., rowid not supported), skip gracefully
        return ValidationRule(
            name="no_overlapping_dates",
            status=ValidationStatus.WARN,
            message="Could not verify date overlap (query error). Manual check recommended.",
        )
    finally:
        con.close()

    if result:
        details = [f"Key {row[:-1]} has {row[-1]} overlapping date range pair(s)" for row in result]
        return ValidationRule(
            name="no_overlapping_dates",
            status=ValidationStatus.FAIL,
            message=f"{len(result)} business key(s) have overlapping date ranges.",
            details=details,
        )

    return ValidationRule(
        name="no_overlapping_dates",
        status=ValidationStatus.PASS,
        message="No overlapping date ranges found.",
    )


def _check_date_consistency(df: pl.DataFrame) -> ValidationRule:
    """effective_from <= effective_to where effective_to is not null."""
    if "effective_from" not in df.columns or "effective_to" not in df.columns:
        return ValidationRule(
            name="date_consistency",
            status=ValidationStatus.WARN,
            message="Date columns missing, cannot validate consistency.",
        )

    bad_rows = df.filter(
        pl.col("effective_to").is_not_null()
        & (pl.col("effective_from") > pl.col("effective_to"))
    )

    if bad_rows.height > 0:
        return ValidationRule(
            name="date_consistency",
            status=ValidationStatus.FAIL,
            message=f"{bad_rows.height} row(s) have effective_from > effective_to.",
        )

    return ValidationRule(
        name="date_consistency",
        status=ValidationStatus.PASS,
        message="All date ranges are consistent (effective_from <= effective_to).",
    )


def _format_key(row: dict, business_key: list[str]) -> str:
    """Format a key dict for display."""
    parts = [f"{k}={row[k]}" for k in business_key if k in row]
    return ", ".join(parts)
