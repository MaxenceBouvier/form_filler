"""Integration tests for PDF extraction."""

import tempfile
from pathlib import Path

import pytest

from form_filler.application.extract_fields import ExtractFieldsUseCase
from form_filler.container import container, setup_container
from form_filler.domain.interfaces import FieldCategorizer, PDFProcessor


class TestPDFExtractionIntegration:
    """Integration tests for PDF extraction."""

    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup test environment."""
        setup_container()

    @pytest.fixture
    def sample_pdf(self, tmp_path):
        """Create or provide a sample PDF for testing.

        Note: This is a placeholder. In a real implementation,
        you would need an actual PDF file for testing.
        """
        # For demonstration, we'll skip this test if no sample PDF exists
        sample_pdf_path = Path("form_to_fill/sample.pdf")
        if not sample_pdf_path.exists():
            pytest.skip("Sample PDF not available for testing")
        return sample_pdf_path

    def test_end_to_end_extraction(self, sample_pdf):
        """Test complete extraction workflow."""
        # Resolve real dependencies from container
        pdf_processor = container.resolve(PDFProcessor)

        # Create use case with real dependencies
        use_case = ExtractFieldsUseCase(pdf_processor=pdf_processor)

        # Execute extraction
        result = use_case.execute(sample_pdf)

        # Verify results
        assert result is not None
        assert result.field_count > 0
        assert len(result.fields) > 0

    def test_extraction_with_json_output(self, sample_pdf):
        """Test extraction with JSON output."""
        with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as tmp:
            output_path = Path(tmp.name)

        try:
            pdf_processor = container.resolve(PDFProcessor)
            repo = container.resolve("json_repository")

            use_case = ExtractFieldsUseCase(pdf_processor=pdf_processor, repository=repo)

            result = use_case.execute(sample_pdf, output_path)

            assert output_path.exists()
            assert result.field_count > 0
        finally:
            # Cleanup
            if output_path.exists():
                output_path.unlink()

    def test_extraction_with_categorization(self, sample_pdf):
        """Test extraction with field categorization."""
        pdf_processor = container.resolve(PDFProcessor)
        categorizer = container.resolve(FieldCategorizer)

        use_case = ExtractFieldsUseCase(pdf_processor=pdf_processor, categorizer=categorizer)

        result = use_case.execute(sample_pdf)

        # Verify that fields have categories assigned
        assert result.field_count > 0
        # At least some fields should have categories (not all will be OTHER)
        categorized_fields = [f for f in result.fields if f.category is not None]
        assert len(categorized_fields) > 0
