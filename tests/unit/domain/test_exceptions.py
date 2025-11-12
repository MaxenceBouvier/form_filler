"""Unit tests for domain exceptions."""

import pytest

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


class TestFormFillerException:
    """Test the base FormFillerException class."""

    def test_exception_with_message_only(self):
        """Test exception creation with just a message."""
        exc = FormFillerException("Something went wrong")
        assert exc.message == "Something went wrong"
        assert exc.context == {}
        assert str(exc) == "Something went wrong"

    def test_exception_with_context(self):
        """Test exception creation with message and context."""
        exc = FormFillerException("Error occurred", {"field": "name", "value": "test"})
        assert exc.message == "Error occurred"
        assert exc.context == {"field": "name", "value": "test"}
        assert "field=name" in str(exc)
        assert "value=test" in str(exc)

    def test_exception_with_empty_context(self):
        """Test exception with explicitly empty context."""
        exc = FormFillerException("Error", {})
        assert exc.context == {}
        assert str(exc) == "Error"

    def test_exception_with_none_context(self):
        """Test exception with None context (should default to empty dict)."""
        exc = FormFillerException("Error", None)
        assert exc.context == {}

    def test_exception_inheritance(self):
        """Test that FormFillerException inherits from Exception."""
        exc = FormFillerException("Error")
        assert isinstance(exc, Exception)

    def test_exception_can_be_raised(self):
        """Test that exception can be raised and caught."""
        with pytest.raises(FormFillerException) as exc_info:
            raise FormFillerException("Test error")
        assert "Test error" in str(exc_info.value)


class TestPDFNotFoundError:
    """Test the PDFNotFoundError exception."""

    def test_pdf_not_found_with_path(self):
        """Test PDFNotFoundError with file path."""
        exc = PDFNotFoundError("/path/to/missing.pdf")
        assert "PDF file not found" in exc.message
        assert "/path/to/missing.pdf" in exc.message
        assert exc.context["path"] == "/path/to/missing.pdf"

    def test_pdf_not_found_inheritance(self):
        """Test that PDFNotFoundError inherits from FormFillerException."""
        exc = PDFNotFoundError("/test.pdf")
        assert isinstance(exc, FormFillerException)

    def test_pdf_not_found_can_be_raised(self):
        """Test that PDFNotFoundError can be raised and caught."""
        with pytest.raises(PDFNotFoundError) as exc_info:
            raise PDFNotFoundError("/missing.pdf")
        assert "/missing.pdf" in str(exc_info.value)


class TestPDFProcessingError:
    """Test the PDFProcessingError exception."""

    def test_pdf_processing_error_with_message_only(self):
        """Test PDFProcessingError with just a message."""
        exc = PDFProcessingError("Corrupt file")
        assert "PDF processing failed" in exc.message
        assert "Corrupt file" in exc.message
        assert exc.context == {}

    def test_pdf_processing_error_with_path(self):
        """Test PDFProcessingError with message and path."""
        exc = PDFProcessingError("Cannot extract fields", pdf_path="/test.pdf")
        assert "PDF processing failed" in exc.message
        assert "Cannot extract fields" in exc.message
        assert exc.context["pdf_path"] == "/test.pdf"

    def test_pdf_processing_error_inheritance(self):
        """Test that PDFProcessingError inherits from FormFillerException."""
        exc = PDFProcessingError("Error")
        assert isinstance(exc, FormFillerException)


class TestDataRepositoryError:
    """Test the DataRepositoryError exception."""

    def test_data_repository_error_with_message_only(self):
        """Test DataRepositoryError with just a message."""
        exc = DataRepositoryError("Cannot read file")
        assert "Data repository error" in exc.message
        assert "Cannot read file" in exc.message
        assert exc.context == {}

    def test_data_repository_error_with_operation(self):
        """Test DataRepositoryError with message and operation."""
        exc = DataRepositoryError("Database connection failed", operation="read")
        assert "Data repository error" in exc.message
        assert "Database connection failed" in exc.message
        assert exc.context["operation"] == "read"

    def test_data_repository_error_inheritance(self):
        """Test that DataRepositoryError inherits from FormFillerException."""
        exc = DataRepositoryError("Error")
        assert isinstance(exc, FormFillerException)


class TestFieldCategorizationError:
    """Test the FieldCategorizationError exception."""

    def test_field_categorization_error(self):
        """Test FieldCategorizationError with field name and reason."""
        exc = FieldCategorizationError("unknown_field", "Field name doesn't match any category")
        assert "Cannot categorize field" in exc.message
        assert "unknown_field" in exc.message
        assert "Field name doesn't match any category" in exc.message
        assert exc.context["field_name"] == "unknown_field"
        assert "Field name doesn't match any category" in exc.context["reason"]

    def test_field_categorization_error_inheritance(self):
        """Test that FieldCategorizationError inherits from FormFillerException."""
        exc = FieldCategorizationError("field", "reason")
        assert isinstance(exc, FormFillerException)


class TestValidationError:
    """Test the ValidationError exception."""

    def test_validation_error_with_message_only(self):
        """Test ValidationError with just a message."""
        exc = ValidationError("Invalid input")
        assert "Validation error" in exc.message
        assert "Invalid input" in exc.message
        assert exc.context == {}

    def test_validation_error_with_field_name(self):
        """Test ValidationError with message and field name."""
        exc = ValidationError("Value too long", field_name="description")
        assert "Validation error" in exc.message
        assert "Value too long" in exc.message
        assert exc.context["field_name"] == "description"

    def test_validation_error_inheritance(self):
        """Test that ValidationError inherits from FormFillerException."""
        exc = ValidationError("Error")
        assert isinstance(exc, FormFillerException)


class TestDataValidationError:
    """Test the DataValidationError exception."""

    def test_data_validation_error_with_message_only(self):
        """Test DataValidationError with just a message."""
        exc = DataValidationError("Invalid data format")
        assert "Data validation failed" in exc.message
        assert "Invalid data format" in exc.message
        assert exc.context == {}

    def test_data_validation_error_with_field_name(self):
        """Test DataValidationError with message and field name."""
        exc = DataValidationError("Value is required", field_name="email")
        assert "Data validation failed" in exc.message
        assert "Value is required" in exc.message
        assert exc.context["field_name"] == "email"

    def test_data_validation_error_with_expected_type(self):
        """Test DataValidationError with expected type."""
        exc = DataValidationError(
            "Type mismatch",
            field_name="age",
            expected_type="number",
        )
        assert exc.context["field_name"] == "age"
        assert exc.context["expected_type"] == "number"

    def test_data_validation_error_with_actual_value(self):
        """Test DataValidationError with actual value."""
        exc = DataValidationError(
            "Invalid value",
            field_name="status",
            expected_type="string",
            actual_value=123,
        )
        assert exc.context["field_name"] == "status"
        assert exc.context["expected_type"] == "string"
        assert exc.context["actual_value"] == "123"

    def test_data_validation_error_with_all_fields(self):
        """Test DataValidationError with all optional fields."""
        exc = DataValidationError(
            "Complete validation failure",
            field_name="score",
            expected_type="number",
            actual_value="invalid",
        )
        assert exc.context["field_name"] == "score"
        assert exc.context["expected_type"] == "number"
        assert exc.context["actual_value"] == "invalid"

    def test_data_validation_error_inheritance(self):
        """Test that DataValidationError inherits from FormFillerException."""
        exc = DataValidationError("Error")
        assert isinstance(exc, FormFillerException)


class TestFieldMappingError:
    """Test the FieldMappingError exception."""

    def test_field_mapping_error_with_message_only(self):
        """Test FieldMappingError with just a message."""
        exc = FieldMappingError("Cannot map field")
        assert "Field mapping error" in exc.message
        assert "Cannot map field" in exc.message
        assert exc.context == {}

    def test_field_mapping_error_with_user_field(self):
        """Test FieldMappingError with user field."""
        exc = FieldMappingError("Field not found", user_field="first_name")
        assert "Field mapping error" in exc.message
        assert "Field not found" in exc.message
        assert exc.context["user_field"] == "first_name"

    def test_field_mapping_error_with_form_field(self):
        """Test FieldMappingError with form field."""
        exc = FieldMappingError("Field not found", form_field="firstName")
        assert "Field mapping error" in exc.message
        assert exc.context["form_field"] == "firstName"

    def test_field_mapping_error_with_both_fields(self):
        """Test FieldMappingError with both user and form fields."""
        exc = FieldMappingError(
            "Ambiguous mapping",
            user_field="name",
            form_field="full_name",
        )
        assert "Field mapping error" in exc.message
        assert "Ambiguous mapping" in exc.message
        assert exc.context["user_field"] == "name"
        assert exc.context["form_field"] == "full_name"

    def test_field_mapping_error_inheritance(self):
        """Test that FieldMappingError inherits from FormFillerException."""
        exc = FieldMappingError("Error")
        assert isinstance(exc, FormFillerException)


class TestExceptionHierarchy:
    """Test the overall exception hierarchy."""

    def test_all_exceptions_inherit_from_base(self):
        """Test that all exceptions inherit from FormFillerException."""
        exceptions = [
            PDFNotFoundError("/test.pdf"),
            PDFProcessingError("Error"),
            DataRepositoryError("Error"),
            FieldCategorizationError("field", "reason"),
            ValidationError("Error"),
            DataValidationError("Error"),
            FieldMappingError("Error"),
        ]

        for exc in exceptions:
            assert isinstance(exc, FormFillerException)
            assert isinstance(exc, Exception)

    def test_catch_base_exception(self):
        """Test that base exception can catch all domain exceptions."""
        with pytest.raises(FormFillerException):
            raise PDFNotFoundError("/test.pdf")

        with pytest.raises(FormFillerException):
            raise DataValidationError("Invalid data")

        with pytest.raises(FormFillerException):
            raise FieldMappingError("Cannot map")

    def test_catch_specific_exception(self):
        """Test that specific exceptions can be caught individually."""
        with pytest.raises(PDFNotFoundError):
            raise PDFNotFoundError("/test.pdf")

        with pytest.raises(DataValidationError):
            raise DataValidationError("Invalid")

        with pytest.raises(FieldMappingError):
            raise FieldMappingError("Error")
