"""Domain-specific exceptions."""


class FormFillerException(Exception):
    """Base exception for all form filler errors."""

    pass


class PDFNotFoundError(FormFillerException):
    """Raised when a PDF file cannot be found."""

    pass


class PDFProcessingError(FormFillerException):
    """Raised when PDF processing fails."""

    pass


class DataRepositoryError(FormFillerException):
    """Raised when data repository operations fail."""

    pass


class FieldCategorizationError(FormFillerException):
    """Raised when field categorization fails."""

    pass


class ValidationError(FormFillerException):
    """Raised when data validation fails."""

    pass
