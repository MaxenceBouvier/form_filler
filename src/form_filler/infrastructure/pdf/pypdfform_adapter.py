"""Adapter for PyPDFForm library.

This module provides an implementation of the PDFProcessor protocol using PyPDFForm.
PyPDFForm is used for extracting form schemas, filling forms, and validating PDFs.
"""

from pathlib import Path
from typing import Any

from PyPDFForm import PdfWrapper

from form_filler.domain.exceptions import (
    PDFNotFoundError,
    PDFProcessingError,
    ValidationError,
)
from form_filler.domain.models import FieldType, FormField


class PyPDFFormAdapter:
    """Adapter for PyPDFForm library implementing PDFProcessor protocol.

    This class provides a concrete implementation of PDF processing operations
    using the PyPDFForm library. It handles form field extraction, form filling,
    and validation of PDF forms.

    Attributes:
        adobe_mode: Whether to enable Adobe compatibility mode for appearance regeneration.

    Examples:
        >>> from pathlib import Path
        >>> adapter = PyPDFFormAdapter(adobe_mode=True)
        >>> fields = adapter.extract_fields(Path("form.pdf"))
        >>> adapter.fill_form(
        ...     Path("form.pdf"),
        ...     {"name": "John Doe"},
        ...     Path("filled.pdf")
        ... )
    """

    def __init__(self, adobe_mode: bool = True):
        """Initialize the adapter.

        Args:
            adobe_mode: Enable Adobe compatibility mode for appearance regeneration.
                       Recommended for better compatibility with Adobe Reader.
        """
        self.adobe_mode = adobe_mode

    def extract_schema(self, pdf_path: Path) -> dict[str, Any]:
        """Extract raw schema from PDF.

        Args:
            pdf_path: Path to the PDF file.

        Returns:
            Dictionary containing the form schema with field metadata.

        Raises:
            PDFNotFoundError: If the PDF file doesn't exist.
            PDFProcessingError: If schema extraction fails.

        Examples:
            >>> adapter = PyPDFFormAdapter()
            >>> schema = adapter.extract_schema(Path("form.pdf"))
            >>> "properties" in schema
            True
        """
        if not pdf_path.exists():
            raise PDFNotFoundError(f"PDF not found: {pdf_path}")

        try:
            wrapper = PdfWrapper(str(pdf_path), adobe_mode=self.adobe_mode)
            schema: dict[str, Any] = wrapper.schema
            return schema
        except Exception as e:
            raise PDFProcessingError(f"Failed to extract schema from {pdf_path}: {e}") from e

    def extract_fields(self, pdf_path: Path) -> list[FormField]:
        """Extract and convert fields to domain models.

        Args:
            pdf_path: Path to the PDF file.

        Returns:
            List of FormField domain models.

        Raises:
            PDFNotFoundError: If the PDF file doesn't exist.
            PDFProcessingError: If field extraction fails.

        Examples:
            >>> adapter = PyPDFFormAdapter()
            >>> fields = adapter.extract_fields(Path("form.pdf"))
            >>> all(isinstance(f, FormField) for f in fields)
            True
        """
        schema = self.extract_schema(pdf_path)
        fields = []

        properties = schema.get("properties", {})
        for field_name, meta in properties.items():
            field_type = self._determine_field_type(meta)
            default_value = self._get_default_value(field_type)

            field = FormField(
                name=field_name,
                field_type=field_type,
                default_value=default_value,
                required=meta.get("required", False),
            )
            fields.append(field)

        return fields

    def fill_form(self, pdf_path: Path, data: dict[str, Any], output_path: Path) -> None:
        """Fill a PDF form with provided data and save to output path.

        Args:
            pdf_path: Path to the source PDF form.
            data: Dictionary mapping field names to values.
            output_path: Path where the filled PDF should be saved.

        Raises:
            PDFNotFoundError: If the PDF file doesn't exist.
            PDFProcessingError: If form filling fails.
            ValidationError: If data format is invalid.

        Examples:
            >>> adapter = PyPDFFormAdapter()
            >>> data = {"first_name": "John", "last_name": "Doe"}
            >>> adapter.fill_form(
            ...     Path("form.pdf"),
            ...     data,
            ...     Path("filled.pdf")
            ... )
        """
        if not pdf_path.exists():
            raise PDFNotFoundError(f"PDF not found: {pdf_path}")

        if not isinstance(data, dict):
            raise ValidationError("Data must be a dictionary")

        try:
            # Create output directory if it doesn't exist
            output_path.parent.mkdir(parents=True, exist_ok=True)

            # Fill the form
            wrapper = PdfWrapper(str(pdf_path), adobe_mode=self.adobe_mode)
            wrapper.fill(data)

            # Save to output path
            with output_path.open("wb") as f:
                f.write(wrapper.read())

        except Exception as e:
            raise PDFProcessingError(
                f"Failed to fill form {pdf_path} and save to {output_path}: {e}"
            ) from e

    def validate_form(self, pdf_path: Path) -> bool:
        """Validate that the PDF contains a valid fillable form.

        Args:
            pdf_path: Path to the PDF file to validate.

        Returns:
            True if the PDF contains a valid fillable form, False otherwise.

        Raises:
            PDFNotFoundError: If the PDF file doesn't exist.

        Examples:
            >>> adapter = PyPDFFormAdapter()
            >>> is_valid = adapter.validate_form(Path("form.pdf"))
            >>> isinstance(is_valid, bool)
            True
        """
        if not pdf_path.exists():
            raise PDFNotFoundError(f"PDF not found: {pdf_path}")

        try:
            # Try to extract schema - if successful, it's a valid form
            schema = self.extract_schema(pdf_path)

            # Check if schema has properties (fields)
            properties = schema.get("properties", {})

            # Valid if there's at least one field
            return len(properties) > 0

        except PDFProcessingError:
            # If we can't extract schema, it's not a valid fillable form
            return False

    def _determine_field_type(self, meta: dict[str, Any]) -> FieldType:
        """Determine field type from metadata.

        Args:
            meta: Field metadata dictionary.

        Returns:
            The determined FieldType.

        Examples:
            >>> adapter = PyPDFFormAdapter()
            >>> field_type = adapter._determine_field_type({"type": "boolean"})
            >>> field_type == FieldType.BOOLEAN
            True
        """
        field_type = meta.get("type")

        if isinstance(field_type, list):
            field_type = field_type[0] if field_type else None

        if field_type == "boolean":
            return FieldType.BOOLEAN
        elif field_type == "number":
            return FieldType.NUMBER
        elif field_type == "string":
            return FieldType.TEXT
        else:
            # Default to TEXT for unknown types
            return FieldType.TEXT

    def _get_default_value(self, field_type: FieldType) -> Any:
        """Get default value based on field type.

        Args:
            field_type: The type of the field.

        Returns:
            Appropriate default value for the field type.

        Examples:
            >>> adapter = PyPDFFormAdapter()
            >>> adapter._get_default_value(FieldType.BOOLEAN)
            False
            >>> adapter._get_default_value(FieldType.TEXT)
            ''
        """
        if field_type in (FieldType.BOOLEAN, FieldType.CHECKBOX):
            return False
        elif field_type == FieldType.NUMBER:
            return 0
        else:
            # TEXT, DATE, CHOICE, RADIO, DROPDOWN, UNKNOWN all default to empty string
            return ""
