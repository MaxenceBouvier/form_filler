"""Use case for extracting fields from a PDF form."""

from datetime import datetime
from pathlib import Path

from form_filler.domain.interfaces import FieldCategorizer, PDFProcessor
from form_filler.domain.models import PDFForm


class ExtractFieldsUseCase:
    """Use case for extracting fields from a PDF form."""

    def __init__(
        self,
        pdf_processor: PDFProcessor,
        repository=None,
        categorizer: FieldCategorizer | None = None,
    ):
        """Initialize the use case.

        Args:
            pdf_processor: Implementation of PDF processor interface.
            repository: Optional repository for saving output.
            categorizer: Optional field categorizer.
        """
        self.pdf_processor = pdf_processor
        self.repository = repository
        self.categorizer = categorizer

    def execute(self, pdf_path: Path, output_path: Path | None = None) -> PDFForm:
        """Extract fields from PDF and optionally save to file.

        Args:
            pdf_path: Path to the PDF file.
            output_path: Optional path to save the stub data.

        Returns:
            PDFForm domain model with extracted fields.
        """
        # Extract fields using the PDF processor
        fields = self.pdf_processor.extract_fields(pdf_path)

        # Categorize fields if categorizer is available
        if self.categorizer:
            for field in fields:
                field.category = self.categorizer.categorize(field)

        # Create PDFForm domain model
        pdf_form = PDFForm(
            path=str(pdf_path),
            fields=fields,
            metadata={
                "field_count": len(fields),
                "extraction_timestamp": self._get_timestamp(),
            },
        )

        # Save stub if output path and repository are provided
        if output_path and self.repository:
            stub_data = pdf_form.to_stub_dict()
            self.repository.save(stub_data, output_path)

        return pdf_form

    def _get_timestamp(self) -> str:
        """Get current timestamp.

        Returns:
            ISO format timestamp string.
        """
        return datetime.now().isoformat()
