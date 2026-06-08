"""Groq LLM provider for fallback explanation generation.

Uses the Groq Python SDK to call fast-inference models.
"""

from __future__ import annotations

import logging

import groq as groq_sdk

from ..models import ChangeRecord, ChangeType, Explanation
from .base import LLMProvider

logger = logging.getLogger(__name__)


class GroqProvider(LLMProvider):
    """Generates explanations using the Groq API."""

    MODEL = "llama-3.3-70b-versatile"

    def __init__(self, api_key: str) -> None:
        self._client = groq_sdk.Groq(api_key=api_key)

    @property
    def name(self) -> str:
        return "groq"

    def explain_change(self, record: ChangeRecord) -> Explanation:
        prompt = _build_prompt(record)

        try:
            response = self._client.chat.completions.create(
                model=self.MODEL,
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are a data engineering assistant explaining SCD2 "
                            "(Slowly Changing Dimension Type 2) changes. "
                            "Write clear, concise explanations for business users. "
                            "Do not use markdown."
                        ),
                    },
                    {"role": "user", "content": prompt},
                ],
                max_tokens=200,
                temperature=0.3,
            )
            text = response.choices[0].message.content.strip()
        except Exception as e:
            logger.warning("Groq API call failed: %s", e)
            raise

        return Explanation(
            business_key_values=record.business_key_values,
            change_type=record.change_type,
            text=text,
            provider=self.name,
        )


def _build_prompt(record: ChangeRecord) -> str:
    """Build a prompt for the Groq model."""
    key_str = ", ".join(f"{k}={v}" for k, v in record.business_key_values.items())

    lines = [
        f"Record: {key_str}",
        f"Change type: {record.change_type.value}",
    ]

    if record.change_type == ChangeType.CHANGED and record.field_changes:
        lines.append("Field changes:")
        for fc in record.field_changes:
            lines.append(f"  - {fc.column}: '{fc.old_value}' → '{fc.new_value}'")

    lines.append("")
    lines.append("Explain this SCD2 change in one or two clear sentences.")

    return "\n".join(lines)
