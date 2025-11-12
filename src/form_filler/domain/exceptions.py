"""Domain-specific exceptions.

This module defines a comprehensive exception hierarchy for the form filler domain.
All exceptions inherit from FormFillerException and provide detailed error messages
to facilitate debugging and error handling.
"""


class FormFillerException(Exception):
    """Base exception for all form filler errors.

    All domain-specific exceptions inherit from this base class, allowing
    for broad exception handling when needed.

    Attributes:
        message: Human-readable error description
        context: Optional dictionary with additional error context
    """

    def __init__(self, message: str, context: dict | None = None) -> None:
        """Initialize the exception with a message and optional context.

        Args:
            message: Human-readable description of the error
            context: Optional dictionary containing additional error details
        """
        self.message = message
        self.context = context or {}
        super().__init__(self.message)

    def __str__(self) -> str:
        """Return string representation of the exception."""
        if self.context:
            context_str = ", ".join(f"{k}={v}" for k, v in self.context.items())
            return f"{self.message} (context: {context_str})"
        return self.message


class PDFNotFoundError(FormFillerException):
    """Raised when a PDF file cannot be found.

    This exception is raised when attempting to access a PDF file that
    doesn't exist at the specified path.
    """

    def __init__(self, path: str) -> None:
        """Initialize with the missing PDF path.

        Args:
            path: The file path that was not found
        """
        super().__init__(f"PDF file not found: {path}", {"path": path})


class PDFProcessingError(FormFillerException):
    """Raised when PDF processing fails.

    This exception covers various PDF processing errors such as:
    - Corrupt or invalid PDF files
    - Failed field extraction
    - PDF generation errors
    - PDF writing/saving errors
    """

    def __init__(self, message: str, pdf_path: str | None = None) -> None:
        """Initialize with error message and optional PDF path.

        Args:
            message: Description of what went wrong during PDF processing
            pdf_path: Optional path to the PDF file that caused the error
        """
        context = {"pdf_path": pdf_path} if pdf_path else {}
        super().__init__(f"PDF processing failed: {message}", context)


class DataRepositoryError(FormFillerException):
    """Raised when data repository operations fail.

    This exception is raised when there are errors in reading from or
    writing to the user data repository (database, file system, etc.).
    """

    def __init__(self, message: str, operation: str | None = None) -> None:
        """Initialize with error message and optional operation name.

        Args:
            message: Description of the repository error
            operation: Optional name of the operation that failed (e.g., 'read', 'write')
        """
        context = {"operation": operation} if operation else {}
        super().__init__(f"Data repository error: {message}", context)


class FieldCategorizationError(FormFillerException):
    """Raised when field categorization fails.

    This exception is raised when the system cannot properly categorize
    a form field (e.g., cannot determine if it's personal info, address, etc.).
    """

    def __init__(self, field_name: str, reason: str) -> None:
        """Initialize with field name and reason for categorization failure.

        Args:
            field_name: Name of the field that could not be categorized
            reason: Explanation of why categorization failed
        """
        super().__init__(
            f"Cannot categorize field '{field_name}': {reason}",
            {"field_name": field_name, "reason": reason},
        )


class ValidationError(FormFillerException):
    """Raised when data validation fails.

    This is a general validation error used throughout the domain layer
    for various validation failures in value objects and entities.
    """

    def __init__(self, message: str, field_name: str | None = None) -> None:
        """Initialize with error message and optional field name.

        Args:
            message: Description of the validation failure
            field_name: Optional name of the field that failed validation
        """
        context = {"field_name": field_name} if field_name else {}
        super().__init__(f"Validation error: {message}", context)


class DataValidationError(FormFillerException):
    """Raised when user data validation fails.

    This exception is raised specifically for validation errors in user data,
    such as missing required fields, invalid data types, or constraint violations.
    """

    def __init__(
        self,
        message: str,
        field_name: str | None = None,
        expected_type: str | None = None,
        actual_value: object = None,
    ) -> None:
        """Initialize with validation details.

        Args:
            message: Description of the validation failure
            field_name: Optional name of the field that failed validation
            expected_type: Optional description of expected data type
            actual_value: Optional actual value that failed validation
        """
        context = {}
        if field_name:
            context["field_name"] = field_name
        if expected_type:
            context["expected_type"] = expected_type
        if actual_value is not None:
            context["actual_value"] = str(actual_value)

        super().__init__(f"Data validation failed: {message}", context)


class FieldMappingError(FormFillerException):
    """Raised when field mapping between user data and form fields fails.

    This exception is raised when the system cannot properly map user data fields
    to form fields, such as:
    - Ambiguous field matches
    - No matching fields found
    - Conflicting mappings
    """

    def __init__(
        self,
        message: str,
        user_field: str | None = None,
        form_field: str | None = None,
    ) -> None:
        """Initialize with mapping error details.

        Args:
            message: Description of the mapping error
            user_field: Optional name of the user data field
            form_field: Optional name of the form field
        """
        context = {}
        if user_field:
            context["user_field"] = user_field
        if form_field:
            context["form_field"] = form_field

        super().__init__(f"Field mapping error: {message}", context)
