"""Adapter for PyPDFForm library."""

from pathlib import Path
from typing import Any

from PyPDFForm import PdfWrapper

from form_filler.domain.exceptions import PDFNotFoundError, PDFProcessingError
from form_filler.domain.models import FieldType, FormField


class PyPDFFormAdapter:
    """Adapter for PyPDFForm library."""

    def __init__(self, adobe_mode: bool = True):
        """Initialize the adapter.

        Args:
            adobe_mode: Enable Adobe compatibility mode for appearance regeneration.
        """
        self.adobe_mode = adobe_mode

    def extract_schema(self, pdf_path: Path) -> dict:
        """Extract raw schema from PDF.

        Args:
            pdf_path: Path to the PDF file.

        Returns:
            Dictionary containing the form schema.

        Raises:
            PDFNotFoundError: If the PDF file doesn't exist.
            PDFProcessingError: If schema extraction fails.
        """
        if not pdf_path.exists():
            raise PDFNotFoundError(f"PDF not found: {pdf_path}")

        try:
            wrapper = PdfWrapper(str(pdf_path), adobe_mode=self.adobe_mode)
            schema: dict = wrapper.schema
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

    def _determine_field_type(self, meta: dict[str, Any]) -> FieldType:
        """Determine field type from metadata.

        Args:
            meta: Field metadata dictionary.

        Returns:
            The determined FieldType.
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
        """
        if field_type in (FieldType.BOOLEAN, FieldType.CHECKBOX):
            return False
        elif field_type == FieldType.NUMBER:
            return 0
        else:
            # TEXT, DATE, CHOICE, RADIO, DROPDOWN, UNKNOWN all default to empty string
            return ""
