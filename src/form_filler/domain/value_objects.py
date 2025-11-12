"""Value objects for domain concepts - immutable and validated."""

from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Any

from form_filler.domain.exceptions import ValidationError


class FieldType(Enum):
    """Types of form fields.

    Represents the various data types that can appear in PDF forms.
    This is an immutable enum that ensures type safety across the domain.
    """

    TEXT = "text"
    BOOLEAN = "boolean"
    DATE = "date"
    NUMBER = "number"
    CHOICE = "choice"
    CHECKBOX = "checkbox"
    RADIO = "radio"
    DROPDOWN = "dropdown"
    UNKNOWN = "unknown"

    def __str__(self) -> str:
        """Return string representation."""
        return self.value


class FieldCategory(Enum):
    """Categories for organizing form fields.

    Used to group related fields for better organization and processing.
    This is an immutable enum that ensures consistent categorization.
    """

    PERSONAL = "personal"
    ADDRESS = "address"
    CONTACT = "contact"
    LEGAL = "legal"
    FINANCIAL = "financial"
    EMPLOYMENT = "employment"
    OTHER = "other"

    def __str__(self) -> str:
        """Return string representation."""
        return self.value


@dataclass(frozen=True)
class FilePath:
    """Immutable value object representing a file path with validation.

    Ensures that file paths are valid and meet specific requirements.
    Being frozen makes it immutable and safe to use as dict keys or in sets.
    """

    path: str

    def __post_init__(self) -> None:
        """Validate the file path after initialization."""
        if not self.path:
            raise ValidationError("File path cannot be empty")

        if not isinstance(self.path, str):
            raise ValidationError(f"File path must be a string, got {type(self.path).__name__}")

        # Check for null bytes which are invalid in file paths
        if "\x00" in self.path:
            raise ValidationError("File path cannot contain null bytes")

    def as_path(self) -> Path:
        """Convert to pathlib.Path for file operations."""
        return Path(self.path)

    def exists(self) -> bool:
        """Check if the file exists."""
        return self.as_path().exists()

    def is_pdf(self) -> bool:
        """Check if the file has a PDF extension."""
        return self.path.lower().endswith(".pdf")

    def __str__(self) -> str:
        """Return string representation."""
        return self.path


@dataclass(frozen=True)
class FieldValue:
    """Immutable value object representing a form field value with type-safe conversions.

    Provides type-safe value conversions and validation based on field type.
    Being frozen ensures immutability and safe sharing across the domain.
    """

    value: Any
    field_type: FieldType

    def __post_init__(self) -> None:
        """Validate the field value after initialization."""
        # Validate that field_type is actually a FieldType
        if not isinstance(self.field_type, FieldType):
            raise ValidationError(
                f"field_type must be a FieldType enum, got {type(self.field_type).__name__}"
            )

    def as_str(self) -> str:
        """Convert value to string representation."""
        if self.value is None:
            return ""
        return str(self.value)

    def as_bool(self) -> bool:
        """Convert value to boolean.

        Raises:
            ValidationError: If conversion is not possible or field type is incompatible.
        """
        if self.field_type not in (FieldType.BOOLEAN, FieldType.CHECKBOX):
            raise ValidationError(f"Cannot convert {self.field_type} field to boolean")

        if isinstance(self.value, bool):
            return self.value

        if isinstance(self.value, str):
            # Handle common boolean string representations
            lower_val = self.value.lower().strip()
            if lower_val in ("true", "yes", "1", "on"):
                return True
            elif lower_val in ("false", "no", "0", "off", ""):
                return False
            else:
                raise ValidationError(f"Cannot convert string '{self.value}' to boolean")

        if isinstance(self.value, (int, float)):
            return bool(self.value)

        raise ValidationError(f"Cannot convert {type(self.value).__name__} to boolean")

    def as_int(self) -> int:
        """Convert value to integer.

        Raises:
            ValidationError: If conversion is not possible or field type is incompatible.
        """
        if self.field_type != FieldType.NUMBER:
            raise ValidationError(f"Cannot convert {self.field_type} field to integer")

        if isinstance(self.value, int):
            return self.value

        if isinstance(self.value, float):
            return int(self.value)

        if isinstance(self.value, str):
            try:
                # Try to convert, removing common formatting
                cleaned = self.value.strip().replace(",", "").replace(" ", "")
                return int(float(cleaned))  # Use float as intermediate to handle "123.0"
            except (ValueError, AttributeError) as e:
                raise ValidationError(
                    f"Cannot convert string '{self.value}' to integer: {e}"
                ) from e

        raise ValidationError(f"Cannot convert {type(self.value).__name__} to integer")

    def as_float(self) -> float:
        """Convert value to float.

        Raises:
            ValidationError: If conversion is not possible or field type is incompatible.
        """
        if self.field_type != FieldType.NUMBER:
            raise ValidationError(f"Cannot convert {self.field_type} field to float")

        if isinstance(self.value, (int, float)):
            return float(self.value)

        if isinstance(self.value, str):
            try:
                # Try to convert, removing common formatting
                cleaned = self.value.strip().replace(",", "").replace(" ", "")
                return float(cleaned)
            except (ValueError, AttributeError) as e:
                raise ValidationError(f"Cannot convert string '{self.value}' to float: {e}") from e

        raise ValidationError(f"Cannot convert {type(self.value).__name__} to float")

    def is_empty(self) -> bool:
        """Check if the value is empty or None."""
        if self.value is None:
            return True
        if isinstance(self.value, str):
            return self.value.strip() == ""
        if isinstance(self.value, (list, dict, tuple)):
            return len(self.value) == 0
        return False

    def __str__(self) -> str:
        """Return string representation."""
        return self.as_str()

    def __eq__(self, other: object) -> bool:
        """Check equality with another FieldValue."""
        if not isinstance(other, FieldValue):
            return NotImplemented
        return self.value == other.value and self.field_type == other.field_type

    def __hash__(self) -> int:
        """Return hash for use in sets and as dict keys."""
        # Only hash immutable components
        return hash((str(self.value), self.field_type))
