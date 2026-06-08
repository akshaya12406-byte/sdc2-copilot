"""Shared test fixtures and helpers."""

from __future__ import annotations

import sys
from datetime import date
from pathlib import Path

import polars as pl
import pytest

# Ensure src is importable
_project_root = Path(__file__).resolve().parent.parent
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))

SAMPLE_DATA_DIR = _project_root / "sample-data"


@pytest.fixture
def source_df() -> pl.DataFrame:
    """Standard source_today.csv as a Polars DataFrame."""
    return pl.read_csv(SAMPLE_DATA_DIR / "source_today.csv", try_parse_dates=True)


@pytest.fixture
def target_df() -> pl.DataFrame:
    """Standard target_yesterday.csv as a Polars DataFrame, with normalized types."""
    from src.scd2_copilot.ingestion import load_csv
    return load_csv(SAMPLE_DATA_DIR / "target_yesterday.csv")


@pytest.fixture
def expected_output_df() -> pl.DataFrame:
    """Standard expected_output.csv as a Polars DataFrame, with normalized types."""
    from src.scd2_copilot.ingestion import load_csv
    return load_csv(SAMPLE_DATA_DIR / "expected_output.csv")


@pytest.fixture
def business_key() -> list[str]:
    return ["customer_id"]


@pytest.fixture
def tracked_columns() -> list[str]:
    return ["name", "city", "tier"]


@pytest.fixture
def processing_date() -> date:
    return date(2026, 6, 8)
