"""Domain layer - pure business logic with no external dependencies."""

from form_filler.domain.exceptions import (
    DataRepositoryError,
    DataValidationError,
    FieldCategorizationError,
    FieldMappingError,
    FormFillerException,
    PDFNotFoundError,
    PDFProcessingError,
    ValidationError,
)
from form_filler.domain.models import FieldMapping, FormField, PDFForm, UserData
from form_filler.domain.validators import (
    validate_field_mapping,
    validate_field_value,
    validate_user_data,
)
from form_filler.domain.value_objects import (
    FieldCategory,
    FieldType,
    FieldValue,
    FilePath,
)

__all__ = [
    # Value Objects
    "FieldType",
    "FieldCategory",
    "FieldValue",
    "FilePath",
    # Domain Models
    "FormField",
    "PDFForm",
    "UserData",
    "FieldMapping",
    # Exceptions
    "FormFillerException",
    "PDFNotFoundError",
    "PDFProcessingError",
    "DataRepositoryError",
    "FieldCategorizationError",
    "ValidationError",
    "DataValidationError",
    "FieldMappingError",
    # Validators
    "validate_field_value",
    "validate_user_data",
    "validate_field_mapping",
]
