"""Domain interfaces defining contracts for infrastructure implementations.

This module defines Protocol-based interfaces for the form filler domain layer.
These protocols establish contracts that infrastructure implementations must satisfy,
enabling dependency inversion and testability.

Protocols vs Abstract Base Classes:
    - Protocols use structural subtyping (duck typing with type checking)
    - No explicit inheritance required (unlike ABC)
    - More flexible and Pythonic
    - Runtime checking available with @runtime_checkable

Examples:
    >>> from pathlib import Path
    >>> from form_filler.domain.interfaces import PDFProcessor
    >>> from form_filler.infrastructure.pdf.pypdfform_adapter import PyPDFFormAdapter
    >>>
    >>> # PyPDFFormAdapter satisfies PDFProcessor protocol without inheritance
    >>> processor: PDFProcessor = PyPDFFormAdapter()
    >>> fields = processor.extract_fields(Path("form.pdf"))
"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Protocol, runtime_checkable

from form_filler.domain.models import FieldCategory, FieldMapping, FormField


@runtime_checkable
class PDFProcessor(Protocol):
    """Protocol for PDF processing operations.

    Defines the contract for extracting information from PDF forms.
    Implementations should handle PDF parsing, field extraction, and
    form filling operations.

    Methods:
        extract_schema: Extract raw form schema from PDF
        extract_fields: Extract and convert fields to domain models
        fill_form: Populate PDF form with provided data
        validate_form: Validate that all required fields are present

    Examples:
        >>> from pathlib import Path
        >>> from form_filler.infrastructure.pdf.pypdfform_adapter import PyPDFFormAdapter
        >>>
        >>> processor = PyPDFFormAdapter(adobe_mode=True)
        >>> fields = processor.extract_fields(Path("tax_form.pdf"))
        >>> schema = processor.extract_schema(Path("tax_form.pdf"))
    """

    def extract_schema(self, pdf_path: Path) -> dict[str, Any]:
        """Extract raw form schema from a PDF file.

        Args:
            pdf_path: Path to the PDF file to analyze

        Returns:
            Dictionary containing the raw form schema with field metadata.
            Structure depends on the underlying PDF library.

        Raises:
            PDFNotFoundError: If the PDF file doesn't exist
            PDFProcessingError: If schema extraction fails

        Examples:
            >>> schema = processor.extract_schema(Path("form.pdf"))
            >>> "properties" in schema
            True
        """
        ...

    def extract_fields(self, pdf_path: Path) -> list[FormField]:
        """Extract form fields from a PDF and convert to domain models.

        Args:
            pdf_path: Path to the PDF file to analyze

        Returns:
            List of FormField domain models representing the form structure.

        Raises:
            PDFNotFoundError: If the PDF file doesn't exist
            PDFProcessingError: If field extraction fails

        Examples:
            >>> fields = processor.extract_fields(Path("form.pdf"))
            >>> len(fields) > 0
            True
            >>> all(isinstance(f, FormField) for f in fields)
            True
        """
        ...

    def fill_form(self, pdf_path: Path, data: dict[str, Any], output_path: Path) -> None:
        """Fill a PDF form with provided data and save to output path.

        Args:
            pdf_path: Path to the source PDF form
            data: Dictionary mapping field names to values
            output_path: Path where the filled PDF should be saved

        Raises:
            PDFNotFoundError: If the PDF file doesn't exist
            PDFProcessingError: If form filling fails
            ValidationError: If data format is invalid

        Examples:
            >>> data = {"first_name": "John", "last_name": "Doe"}
            >>> processor.fill_form(
            ...     Path("form.pdf"),
            ...     data,
            ...     Path("form_filled.pdf")
            ... )
        """
        ...

    def validate_form(self, pdf_path: Path) -> bool:
        """Validate that the PDF contains a valid fillable form.

        Args:
            pdf_path: Path to the PDF file to validate

        Returns:
            True if the PDF contains a valid fillable form, False otherwise.

        Raises:
            PDFNotFoundError: If the PDF file doesn't exist

        Examples:
            >>> is_valid = processor.validate_form(Path("form.pdf"))
            >>> isinstance(is_valid, bool)
            True
        """
        ...


@runtime_checkable
class DataRepository(Protocol):
    """Protocol for data persistence operations.

    Defines the contract for saving and loading structured data.
    Implementations can support different formats (JSON, YAML, etc.)
    and storage backends.

    Methods:
        save: Persist data to storage
        load: Retrieve data from storage
        exists: Check if data exists at path
        list_profiles: List available user profiles

    Examples:
        >>> from pathlib import Path
        >>> from form_filler.infrastructure.persistence.json_repository import JSONRepository
        >>>
        >>> repo = JSONRepository()
        >>> data = {"name": "John Doe", "age": 30}
        >>> repo.save(data, Path("user.json"))
        >>> loaded = repo.load(Path("user.json"))
        >>> loaded["name"]
        'John Doe'
    """

    def save(self, data: dict[str, Any], path: Path) -> None:
        """Save data to persistent storage.

        Args:
            data: Dictionary to persist
            path: Target path for storage

        Raises:
            DataRepositoryError: If save operation fails

        Examples:
            >>> repo.save({"key": "value"}, Path("data.json"))
        """
        ...

    def load(self, path: Path) -> dict[str, Any]:
        """Load data from persistent storage.

        Args:
            path: Source path to load from

        Returns:
            Dictionary loaded from storage.

        Raises:
            DataRepositoryError: If load operation fails
            FileNotFoundError: If path doesn't exist

        Examples:
            >>> data = repo.load(Path("user.json"))
            >>> isinstance(data, dict)
            True
        """
        ...

    def exists(self, path: Path) -> bool:
        """Check if data exists at the specified path.

        Args:
            path: Path to check

        Returns:
            True if data exists at path, False otherwise.

        Examples:
            >>> repo.exists(Path("user.json"))
            True
            >>> repo.exists(Path("nonexistent.json"))
            False
        """
        ...

    def list_profiles(self, directory: Path) -> list[Path]:
        """List all available user profile files in a directory.

        Args:
            directory: Directory to search for profiles

        Returns:
            List of paths to profile files, sorted by modification time.

        Raises:
            DataRepositoryError: If directory access fails

        Examples:
            >>> profiles = repo.list_profiles(Path("resources/user_info"))
            >>> all(p.exists() for p in profiles)
            True
        """
        ...


@runtime_checkable
class LLMProvider(Protocol):
    """Protocol for Large Language Model operations.

    Defines the contract for LLM-based text generation and data extraction.
    Implementations can use different models (OpenAI, Anthropic, local models).

    Methods:
        generate_text: Generate natural language text
        extract_structured_data: Extract structured data from text

    Examples:
        >>> provider = HuggingFaceLLM(model_name="meta-llama/Llama-2-7b-chat-hf")
        >>> text = provider.generate_text("Explain form filling")
        >>> data = provider.extract_structured_data(
        ...     "John Doe lives at 123 Main St",
        ...     schema={"name": str, "address": str}
        ... )
    """

    def generate_text(
        self,
        prompt: str,
        max_length: int = 512,
        temperature: float = 0.7,
        **kwargs: Any,
    ) -> str:
        """Generate text using the language model.

        Args:
            prompt: Input prompt for text generation
            max_length: Maximum length of generated text in tokens
            temperature: Sampling temperature (0.0 = deterministic, 1.0 = creative)
            **kwargs: Additional model-specific parameters

        Returns:
            Generated text string.

        Raises:
            LLMError: If text generation fails

        Examples:
            >>> text = provider.generate_text(
            ...     "Complete this form field description:",
            ...     max_length=100,
            ...     temperature=0.5
            ... )
            >>> isinstance(text, str)
            True
        """
        ...

    def extract_structured_data(
        self, text: str, schema: dict[str, type], **kwargs: Any
    ) -> dict[str, Any]:
        """Extract structured data from natural language text.

        Uses the LLM to parse unstructured text and extract data according
        to the provided schema.

        Args:
            text: Natural language text to parse
            schema: Dictionary mapping field names to expected types
            **kwargs: Additional extraction parameters

        Returns:
            Dictionary with extracted data matching the schema.

        Raises:
            LLMError: If extraction fails
            ValidationError: If extracted data doesn't match schema

        Examples:
            >>> text = "John Doe, born 1990, lives at 123 Main Street"
            >>> schema = {"name": str, "birth_year": int, "address": str}
            >>> data = provider.extract_structured_data(text, schema)
            >>> data["name"]
            'John Doe'
            >>> data["birth_year"]
            1990
        """
        ...


@runtime_checkable
class FieldMatcher(Protocol):
    """Protocol for matching and mapping form fields.

    Defines the contract for mapping user data fields to PDF form fields.
    Implementations can use exact matching, fuzzy matching, or ML-based matching.

    Methods:
        match_fields: Create field mappings between user data and form
        fuzzy_match: Find best matches using fuzzy string matching
        confidence_score: Calculate confidence for a field mapping

    Examples:
        >>> matcher = SimpleFieldMatcher()
        >>> user_fields = ["first_name", "last_name"]
        >>> form_fields = ["firstName", "lastName"]
        >>> mappings = matcher.match_fields(user_fields, form_fields)
        >>> len(mappings) == 2
        True
    """

    def match_fields(
        self,
        user_fields: list[str],
        form_fields: list[FormField],
        min_confidence: float = 0.7,
    ) -> list[FieldMapping]:
        """Create field mappings between user data and form fields.

        Args:
            user_fields: List of field names from user data
            form_fields: List of FormField objects from the PDF
            min_confidence: Minimum confidence threshold for matches (0.0 to 1.0)

        Returns:
            List of FieldMapping objects representing the matches.

        Raises:
            ValidationError: If inputs are invalid

        Examples:
            >>> user_fields = ["email", "phone"]
            >>> form_fields = [
            ...     FormField(name="email_address", ...),
            ...     FormField(name="phone_number", ...)
            ... ]
            >>> mappings = matcher.match_fields(user_fields, form_fields)
            >>> all(m.confidence >= 0.7 for m in mappings)
            True
        """
        ...

    def fuzzy_match(
        self, field_name: str, candidates: list[str], threshold: float = 0.6
    ) -> list[tuple[str, float]]:
        """Find best matches for a field name using fuzzy matching.

        Args:
            field_name: Field name to match
            candidates: List of candidate field names
            threshold: Minimum similarity threshold (0.0 to 1.0)

        Returns:
            List of (candidate, score) tuples sorted by descending score.

        Examples:
            >>> matches = matcher.fuzzy_match(
            ...     "email",
            ...     ["email_address", "e_mail", "phone"],
            ...     threshold=0.5
            ... )
            >>> matches[0][0]  # Best match
            'email_address'
            >>> matches[0][1] > 0.8  # High confidence
            True
        """
        ...

    def confidence_score(
        self, user_field: str, form_field: str, context: dict[str, Any] | None = None
    ) -> float:
        """Calculate confidence score for a field mapping.

        Args:
            user_field: User data field name
            form_field: PDF form field name
            context: Optional context information (field types, categories, etc.)

        Returns:
            Confidence score between 0.0 (no match) and 1.0 (perfect match).

        Examples:
            >>> score = matcher.confidence_score("first_name", "firstName")
            >>> 0.0 <= score <= 1.0
            True
            >>> exact_score = matcher.confidence_score("email", "email")
            >>> exact_score
            1.0
        """
        ...


class FieldCategorizer(ABC):
    """Abstract base class for field categorization.

    NOTE: This uses ABC instead of Protocol for backward compatibility.
    Consider migrating to Protocol in future versions.

    Categorizes form fields into logical groups (personal, address, financial, etc.)
    based on field names, types, and patterns.

    Methods:
        categorize: Assign a category to a form field

    Examples:
        >>> from form_filler.application.field_categorizer import RuleBasedCategorizer
        >>>
        >>> categorizer = RuleBasedCategorizer()
        >>> field = FormField(name="first_name", field_type=FieldType.TEXT, ...)
        >>> category = categorizer.categorize(field)
        >>> category == FieldCategory.PERSONAL
        True
    """

    @abstractmethod
    def categorize(self, field: FormField) -> FieldCategory:
        """Categorize a form field based on its properties.

        Args:
            field: FormField to categorize

        Returns:
            FieldCategory enum value representing the field's category.

        Examples:
            >>> field = FormField(name="street_address", ...)
            >>> categorizer.categorize(field)
            <FieldCategory.ADDRESS: 'address'>
        """
        pass
