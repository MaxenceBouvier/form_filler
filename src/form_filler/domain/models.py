"""Domain models for the form filler application."""

from dataclasses import dataclass
from enum import Enum
from typing import Any


class FieldType(Enum):
    """Types of form fields."""

    TEXT = "text"
    BOOLEAN = "boolean"
    NUMBER = "number"
    DATE = "date"
    CHOICE = "choice"
    UNKNOWN = "unknown"


class FieldCategory(Enum):
    """Categories for organizing form fields."""

    PERSONAL = "personal"
    ADDRESS = "address"
    FINANCIAL = "financial"
    EMPLOYMENT = "employment"
    LEGAL = "legal"
    OTHER = "other"


@dataclass
class FormField:
    """Domain model for a form field."""

    name: str
    field_type: FieldType
    default_value: Any
    required: bool = False
    category: FieldCategory | None = None
    options: list[str] | None = None

    def to_dict(self) -> dict:
        """Convert to dictionary representation."""
        return {
            "name": self.name,
            "type": self.field_type.value,
            "default_value": self.default_value,
            "required": self.required,
            "category": self.category.value if self.category else None,
            "options": self.options,
        }


@dataclass
class PDFForm:
    """Domain model for a PDF form."""

    path: str
    fields: list[FormField]
    metadata: dict[str, Any]

    @property
    def field_count(self) -> int:
        """Return the number of fields in the form."""
        return len(self.fields)

    def get_fields_by_category(self, category: FieldCategory) -> list[FormField]:
        """Get all fields of a specific category."""
        return [f for f in self.fields if f.category == category]

    def to_stub_dict(self) -> dict[str, Any]:
        """Generate a stub dictionary with field names and default values."""
        return {field.name: field.default_value for field in self.fields}
