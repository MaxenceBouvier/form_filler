"""Domain interfaces defining contracts for infrastructure implementations."""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Protocol

from form_filler.domain.models import FieldCategory, FormField


class PDFProcessor(Protocol):
    """Interface for PDF processing implementations."""

    def extract_schema(self, pdf_path: Path) -> dict:
        """Extract form schema from PDF."""
        ...

    def extract_fields(self, pdf_path: Path) -> list[FormField]:
        """Extract form fields from PDF."""
        ...


class DataRepository(Protocol):
    """Interface for data persistence."""

    def save(self, data: dict, path: Path) -> None:
        """Save data to storage."""
        ...

    def load(self, path: Path) -> dict:
        """Load data from storage."""
        ...


class FieldCategorizer(ABC):
    """Abstract base class for field categorization."""

    @abstractmethod
    def categorize(self, field: FormField) -> FieldCategory:
        """Categorize a form field."""
        pass
