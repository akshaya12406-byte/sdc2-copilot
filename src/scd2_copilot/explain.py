"""Explanation orchestration: generate explanations for all detected changes.

Routes change records through the provider chain: primary → fallback → template.
"""

from __future__ import annotations

import logging
from typing import Optional

from .config import LLMProvider as LLMProviderEnum, Settings
from .models import ChangeRecord, ChangeReport, Explanation
from .providers.base import LLMProvider
from .providers.gemini import GeminiProvider
from .providers.groq import GroqProvider
from .providers.template import TemplateProvider

logger = logging.getLogger(__name__)


def get_provider(settings: Settings) -> LLMProvider:
    """Create the appropriate LLM provider based on settings.

    Falls back through: configured provider → next available → template.
    """
    effective = settings.get_effective_provider()

    if effective == LLMProviderEnum.GEMINI:
        return GeminiProvider(api_key=settings.gemini_api_key)
    elif effective == LLMProviderEnum.GROQ:
        return GroqProvider(api_key=settings.groq_api_key)
    else:
        return TemplateProvider()


def explain_changes(
    change_report: ChangeReport,
    settings: Optional[Settings] = None,
    provider: Optional[LLMProvider] = None,
) -> list[Explanation]:
    """Generate explanations for all non-unchanged changes.

    Uses a fallback chain: primary provider → alternative → template.

    Args:
        change_report: The detected changes.
        settings: App settings (used if provider is not given).
        provider: Override provider instance (for testing).

    Returns:
        List of Explanation objects.
    """
    if provider is None:
        if settings is None:
            from .config import get_settings
            settings = get_settings()
        provider = get_provider(settings)

    template = TemplateProvider()

    # Collect all records that need explanation
    records_to_explain: list[ChangeRecord] = (
        change_report.new + change_report.changed + change_report.deleted
    )

    explanations: list[Explanation] = []

    for record in records_to_explain:
        explanation = _explain_with_fallback(record, provider, template)
        explanations.append(explanation)

    return explanations


def _explain_with_fallback(
    record: ChangeRecord,
    primary: LLMProvider,
    fallback: LLMProvider,
) -> Explanation:
    """Try primary provider, fall back to template on failure."""
    # If primary IS the template, no fallback needed
    if primary.name == "template":
        return primary.explain_change(record)

    try:
        return primary.explain_change(record)
    except Exception as e:
        logger.warning(
            "Provider '%s' failed for key %s: %s. Falling back to template.",
            primary.name,
            record.business_key_values,
            e,
        )
        return fallback.explain_change(record)
