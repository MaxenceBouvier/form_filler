"""Unit tests for the ExtractFieldsUseCase."""

from pathlib import Path
from unittest.mock import MagicMock, Mock

import pytest

from form_filler.application.extract_fields import ExtractFieldsUseCase
from form_filler.domain.models import FieldCategory, FieldType, FormField, PDFForm


class TestExtractFieldsUseCase:
    """Test the ExtractFieldsUseCase."""

    @pytest.fixture
    def mock_pdf_processor(self):
        """Create a mock PDF processor."""
        processor = Mock()
        processor.extract_fields.return_value = [
            FormField(
                name="full_name",
                field_type=FieldType.TEXT,
                default_value="",
                required=True,
            ),
            FormField(
                name="is_resident",
                field_type=FieldType.BOOLEAN,
                default_value=False,
                required=False,
            ),
        ]
        return processor

    @pytest.fixture
    def mock_repository(self):
        """Create a mock repository."""
        repo = Mock()
        repo.save = MagicMock()
        return repo

    def test_extract_fields_without_output(self, mock_pdf_processor):
        """Test extracting fields without saving output."""
        use_case = ExtractFieldsUseCase(pdf_processor=mock_pdf_processor)

        pdf_path = Path("test.pdf")
        result = use_case.execute(pdf_path)

        assert isinstance(result, PDFForm)
        assert result.field_count == 2
        assert len(result.fields) == 2
        mock_pdf_processor.extract_fields.assert_called_once_with(pdf_path)

    def test_extract_fields_with_json_output(self, mock_pdf_processor, mock_repository):
        """Test extracting fields and saving to JSON."""
        use_case = ExtractFieldsUseCase(
            pdf_processor=mock_pdf_processor, repository=mock_repository
        )

        pdf_path = Path("test.pdf")
        output_path = Path("output.json")
        result = use_case.execute(pdf_path, output_path)

        assert result.field_count == 2
        mock_repository.save.assert_called_once()
        saved_data = mock_repository.save.call_args[0][0]
        assert "full_name" in saved_data
        assert "is_resident" in saved_data

    def test_extract_with_categorization(self, mock_pdf_processor):
        """Test field extraction with categorization."""
        mock_categorizer = Mock()
        mock_categorizer.categorize = Mock(side_effect=lambda f: FieldCategory.PERSONAL)

        use_case = ExtractFieldsUseCase(
            pdf_processor=mock_pdf_processor, categorizer=mock_categorizer
        )

        pdf_path = Path("test.pdf")
        result = use_case.execute(pdf_path)

        assert all(field.category == FieldCategory.PERSONAL for field in result.fields)
        assert mock_categorizer.categorize.call_count == 2
