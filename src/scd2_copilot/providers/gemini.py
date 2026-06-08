"""Gemini LLM provider via google-genai SDK.

Uses the new unified ``google.genai`` SDK (v2.x) to call Gemini models
for generating human-readable change explanations.
"""

from __future__ import annotations

import logging

from google import genai

from ..models import ChangeRecord, ChangeType, Explanation
from .base import LLMProvider

logger = logging.getLogger(__name__)


class GeminiProvider(LLMProvider):
    """Generates explanations using the Gemini API."""

    MODEL = "gemini-2.0-flash"

    def __init__(self, api_key: str) -> None:
        self._client = genai.Client(api_key=api_key)

    @property
    def name(self) -> str:
        return "gemini"

    def explain_change(self, record: ChangeRecord) -> Explanation:
        prompt = _build_prompt(record)

        try:
            response = self._client.models.generate_content(
                model=self.MODEL,
                contents=prompt,
            )
            text = response.text.strip() if response.text else ""
        except Exception as e:
            logger.warning("Gemini API call failed: %s", e)
            raise

        return Explanation(
            business_key_values=record.business_key_values,
            change_type=record.change_type,
            text=text,
            provider=self.name,
        )


def _build_prompt(record: ChangeRecord) -> str:
    """Build a structured prompt for the LLM from a ChangeRecord."""
    key_str = ", ".join(f"{k}={v}" for k, v in record.business_key_values.items())

    lines = [
        "You are a data engineering assistant explaining SCD2 (Slowly Changing Dimension Type 2) changes.",
        "Explain the following change in one or two clear sentences for a business user.",
        "",
        f"Record: {key_str}",
        f"Change type: {record.change_type.value}",
    ]

    if record.change_type == ChangeType.CHANGED and record.field_changes:
        lines.append("Field changes:")
        for fc in record.field_changes:
            lines.append(f"  - {fc.column}: '{fc.old_value}' → '{fc.new_value}'")

    lines.append("")
    lines.append("Write a clear, concise explanation. Do not use markdown.")

    return "\n".join(lines)
