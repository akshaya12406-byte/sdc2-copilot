"""Abstract base for LLM explanation providers."""

from __future__ import annotations

from abc import ABC, abstractmethod

from ..models import ChangeRecord, Explanation


class LLMProvider(ABC):
    """Protocol for LLM explanation providers.

    Every provider must implement ``explain_change`` which takes a
    ChangeRecord and returns a human-readable Explanation.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """Short identifier for this provider (e.g., 'gemini', 'groq', 'template')."""
        ...

    @abstractmethod
    def explain_change(self, record: ChangeRecord) -> Explanation:
        """Generate a human-readable explanation for a single change.

        Args:
            record: The detected change record.

        Returns:
            An Explanation with the human-readable text.
        """
        ...
