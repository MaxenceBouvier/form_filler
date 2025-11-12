# Refactoring Example: From Legacy to Clean Architecture

This document demonstrates how to refactor the existing `generate_stub.py` script into the recommended clean architecture.

## Original Code Analysis

The current `generate_stub.py` has several architectural issues:
- Direct dependency on PyPDFForm
- Mixed responsibilities (extraction, formatting, file I/O)
- No abstraction layers
- Procedural rather than object-oriented

## Refactored Implementation

### Step 1: Define Domain Models

```python
# src/form_filler/domain/models.py
from dataclasses import dataclass
from enum import Enum
from typing import Any, Optional

class FieldType(Enum):
    TEXT = "text"
    BOOLEAN = "boolean"
    NUMBER = "number"
    DATE = "date"
    CHOICE = "choice"
    UNKNOWN = "unknown"

class FieldCategory(Enum):
    PERSONAL = "personal"
    ADDRESS = "address"
    FINANCIAL = "financial"
    EMPLOYMENT = "employment"
    LEGAL = "legal"
    OTHER = "other"

@dataclass
class FormField:
    """Domain model for a form field."""
    name: str
    field_type: FieldType
    default_value: Any
    required: bool = False
    category: Optional[FieldCategory] = None
    options: Optional[list[str]] = None

    def to_dict(self) -> dict:
        """Convert to dictionary representation."""
        return {
            'name': self.name,
            'type': self.field_type.value,
            'default_value': self.default_value,
            'required': self.required,
            'category': self.category.value if self.category else None,
            'options': self.options
        }

@dataclass
class PDFForm:
    """Domain model for a PDF form."""
    path: str
    fields: list[FormField]
    metadata: dict[str, Any]

    @property
    def field_count(self) -> int:
        return len(self.fields)

    def get_fields_by_category(self, category: FieldCategory) -> list[FormField]:
        """Get all fields of a specific category."""
        return [f for f in self.fields if f.category == category]

    def to_stub_dict(self) -> dict[str, Any]:
        """Generate a stub dictionary with field names and default values."""
        return {field.name: field.default_value for field in self.fields}
```

### Step 2: Define Interfaces

```python
# src/form_filler/domain/interfaces.py
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Protocol

class PDFProcessor(Protocol):
    """Interface for PDF processing implementations."""

    def extract_schema(self, pdf_path: Path) -> dict:
        """Extract form schema from PDF."""
        ...

    def extract_fields(self, pdf_path: Path) -> list[FormField]:
        """Extract form fields from PDF."""
        ...

class DataRepository(Protocol):
    """Interface for data persistence."""

    def save(self, data: dict, path: Path) -> None:
        """Save data to storage."""
        ...

    def load(self, path: Path) -> dict:
        """Load data from storage."""
        ...

class FieldCategorizer(ABC):
    """Abstract base class for field categorization."""

    @abstractmethod
    def categorize(self, field: FormField) -> FieldCategory:
        """Categorize a form field."""
        pass
```

### Step 3: Implement Infrastructure Adapters

```python
# src/form_filler/infrastructure/pdf/pypdfform_adapter.py
from pathlib import Path
from typing import Any

from PyPDFForm import PdfWrapper

from form_filler.domain.models import FormField, FieldType
from form_filler.domain.interfaces import PDFProcessor

class PyPDFFormAdapter(PDFProcessor):
    """Adapter for PyPDFForm library."""

    def __init__(self, adobe_mode: bool = True):
        self.adobe_mode = adobe_mode

    def extract_schema(self, pdf_path: Path) -> dict:
        """Extract raw schema from PDF."""
        if not pdf_path.exists():
            raise FileNotFoundError(f"PDF not found: {pdf_path}")

        wrapper = PdfWrapper(str(pdf_path), adobe_mode=self.adobe_mode)
        return wrapper.schema

    def extract_fields(self, pdf_path: Path) -> list[FormField]:
        """Extract and convert fields to domain models."""
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
                required=meta.get("required", False)
            )
            fields.append(field)

        return fields

    def _determine_field_type(self, meta: dict[str, Any]) -> FieldType:
        """Determine field type from metadata."""
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
            return FieldType.UNKNOWN

    def _get_default_value(self, field_type: FieldType) -> Any:
        """Get default value based on field type."""
        if field_type == FieldType.BOOLEAN:
            return False
        elif field_type == FieldType.NUMBER:
            return 0
        else:
            return ""
```

### Step 4: Implement Repository Adapters

```python
# src/form_filler/infrastructure/persistence/json_repository.py
import json
from pathlib import Path
from typing import Any

from form_filler.domain.interfaces import DataRepository

class JSONRepository(DataRepository):
    """JSON file repository implementation."""

    def __init__(self, ensure_ascii: bool = False, indent: int = 2):
        self.ensure_ascii = ensure_ascii
        self.indent = indent

    def save(self, data: dict[str, Any], path: Path) -> None:
        """Save data to JSON file."""
        path.parent.mkdir(parents=True, exist_ok=True)

        with path.open("w", encoding="utf-8") as f:
            json.dump(
                data,
                f,
                ensure_ascii=self.ensure_ascii,
                indent=self.indent
            )

    def load(self, path: Path) -> dict[str, Any]:
        """Load data from JSON file."""
        if not path.exists():
            raise FileNotFoundError(f"File not found: {path}")

        with path.open("r", encoding="utf-8") as f:
            return json.load(f)
```

```python
# src/form_filler/infrastructure/persistence/yaml_repository.py
from pathlib import Path
from typing import Any, Optional

from form_filler.domain.interfaces import DataRepository

class YAMLRepository(DataRepository):
    """YAML file repository implementation."""

    def __init__(self):
        self._yaml: Optional[Any] = None
        self._ensure_yaml_available()

    def _ensure_yaml_available(self):
        """Ensure PyYAML is available."""
        try:
            import yaml
            self._yaml = yaml
        except ImportError:
            raise RuntimeError(
                "PyYAML is not installed. "
                "Install it with 'pip install pyyaml' to enable YAML support."
            )

    def save(self, data: dict[str, Any], path: Path) -> None:
        """Save data to YAML file."""
        path.parent.mkdir(parents=True, exist_ok=True)

        with path.open("w", encoding="utf-8") as f:
            self._yaml.safe_dump(
                data,
                f,
                sort_keys=False,
                allow_unicode=True
            )

    def load(self, path: Path) -> dict[str, Any]:
        """Load data from YAML file."""
        if not path.exists():
            raise FileNotFoundError(f"File not found: {path}")

        with path.open("r", encoding="utf-8") as f:
            return self._yaml.safe_load(f)
```

### Step 5: Implement Application Use Cases

```python
# src/form_filler/application/extract_fields.py
from pathlib import Path
from typing import Optional

from form_filler.domain.models import PDFForm, FormField
from form_filler.domain.interfaces import PDFProcessor, DataRepository, FieldCategorizer

class ExtractFieldsUseCase:
    """Use case for extracting fields from a PDF form."""

    def __init__(
        self,
        pdf_processor: PDFProcessor,
        repository: Optional[DataRepository] = None,
        categorizer: Optional[FieldCategorizer] = None
    ):
        self.pdf_processor = pdf_processor
        self.repository = repository
        self.categorizer = categorizer

    def execute(self, pdf_path: Path, output_path: Optional[Path] = None) -> PDFForm:
        """Extract fields from PDF and optionally save to file."""
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
                'field_count': len(fields),
                'extraction_timestamp': self._get_timestamp()
            }
        )

        # Save stub if output path and repository are provided
        if output_path and self.repository:
            stub_data = pdf_form.to_stub_dict()
            self.repository.save(stub_data, output_path)

        return pdf_form

    def _get_timestamp(self) -> str:
        """Get current timestamp."""
        from datetime import datetime
        return datetime.now().isoformat()
```

### Step 6: Implement Field Categorization

```python
# src/form_filler/application/field_categorizer.py
import re
from typing import Dict, List

from form_filler.domain.models import FormField, FieldCategory
from form_filler.domain.interfaces import FieldCategorizer

class RuleBasedFieldCategorizer(FieldCategorizer):
    """Rule-based field categorizer using keyword matching."""

    def __init__(self):
        self.rules = self._build_rules()

    def _build_rules(self) -> Dict[FieldCategory, List[re.Pattern]]:
        """Build categorization rules."""
        return {
            FieldCategory.PERSONAL: [
                re.compile(r'.*name.*', re.IGNORECASE),
                re.compile(r'.*birth.*', re.IGNORECASE),
                re.compile(r'.*ssn.*', re.IGNORECASE),
                re.compile(r'.*social.*security.*', re.IGNORECASE),
            ],
            FieldCategory.ADDRESS: [
                re.compile(r'.*address.*', re.IGNORECASE),
                re.compile(r'.*street.*', re.IGNORECASE),
                re.compile(r'.*city.*', re.IGNORECASE),
                re.compile(r'.*state.*', re.IGNORECASE),
                re.compile(r'.*zip.*', re.IGNORECASE),
                re.compile(r'.*postal.*', re.IGNORECASE),
            ],
            FieldCategory.FINANCIAL: [
                re.compile(r'.*income.*', re.IGNORECASE),
                re.compile(r'.*salary.*', re.IGNORECASE),
                re.compile(r'.*bank.*', re.IGNORECASE),
                re.compile(r'.*account.*', re.IGNORECASE),
                re.compile(r'.*tax.*', re.IGNORECASE),
            ],
            FieldCategory.EMPLOYMENT: [
                re.compile(r'.*employer.*', re.IGNORECASE),
                re.compile(r'.*occupation.*', re.IGNORECASE),
                re.compile(r'.*job.*', re.IGNORECASE),
                re.compile(r'.*work.*', re.IGNORECASE),
            ],
        }

    def categorize(self, field: FormField) -> FieldCategory:
        """Categorize a field based on its name."""
        for category, patterns in self.rules.items():
            for pattern in patterns:
                if pattern.match(field.name):
                    return category
        return FieldCategory.OTHER
```

### Step 7: Implement Dependency Injection

```python
# src/form_filler/container.py
from typing import Dict, Type, Any, Optional

class ServiceContainer:
    """Simple dependency injection container."""

    def __init__(self):
        self._services: Dict[Type, Any] = {}
        self._factories: Dict[Type, callable] = {}

    def register(self, interface: Type, implementation: Any) -> None:
        """Register a service implementation."""
        self._services[interface] = implementation

    def register_factory(self, interface: Type, factory: callable) -> None:
        """Register a factory function for lazy initialization."""
        self._factories[interface] = factory

    def resolve(self, interface: Type) -> Any:
        """Resolve a service by interface."""
        # Check if service is already instantiated
        if interface in self._services:
            return self._services[interface]

        # Check if factory exists
        if interface in self._factories:
            service = self._factories[interface]()
            self._services[interface] = service
            return service

        raise ValueError(f"No service registered for {interface}")

    def has(self, interface: Type) -> bool:
        """Check if a service is registered."""
        return interface in self._services or interface in self._factories

# Global container instance
container = ServiceContainer()

def setup_container():
    """Setup the dependency injection container."""
    from form_filler.infrastructure.pdf.pypdfform_adapter import PyPDFFormAdapter
    from form_filler.infrastructure.persistence.json_repository import JSONRepository
    from form_filler.infrastructure.persistence.yaml_repository import YAMLRepository
    from form_filler.application.field_categorizer import RuleBasedFieldCategorizer
    from form_filler.domain.interfaces import PDFProcessor, DataRepository, FieldCategorizer

    # Register services
    container.register(PDFProcessor, PyPDFFormAdapter())
    container.register_factory(FieldCategorizer, RuleBasedFieldCategorizer)

    # Register repositories based on availability
    try:
        container.register('json_repository', JSONRepository())
    except Exception:
        pass

    try:
        container.register('yaml_repository', YAMLRepository())
    except Exception:
        pass
```

### Step 8: Implement CLI Command

```python
# src/form_filler/presentation/cli/commands.py
import argparse
from pathlib import Path
from typing import Optional

from form_filler.container import container, setup_container
from form_filler.application.extract_fields import ExtractFieldsUseCase
from form_filler.domain.interfaces import PDFProcessor, DataRepository

def extract_required_info():
    """CLI command to extract required fields from a PDF."""
    parser = argparse.ArgumentParser(
        description="Extract required field information from a PDF form"
    )
    parser.add_argument(
        "pdf",
        type=Path,
        help="Path to the PDF form"
    )
    parser.add_argument(
        "--json",
        type=Path,
        help="Output JSON file path"
    )
    parser.add_argument(
        "--yaml",
        type=Path,
        help="Output YAML file path"
    )
    parser.add_argument(
        "--categorize",
        action="store_true",
        help="Categorize fields by type (personal, address, etc.)"
    )

    args = parser.parse_args()

    # Setup dependency container
    setup_container()

    # Resolve dependencies
    pdf_processor = container.resolve(PDFProcessor)
    categorizer = None
    if args.categorize and container.has(FieldCategorizer):
        categorizer = container.resolve(FieldCategorizer)

    # Create use case
    use_case = ExtractFieldsUseCase(
        pdf_processor=pdf_processor,
        categorizer=categorizer
    )

    # Execute extraction
    pdf_form = use_case.execute(args.pdf)

    # Display results
    print(f"Extracted {pdf_form.field_count} fields from {args.pdf}")

    if args.categorize:
        print("\nFields by category:")
        categories = {}
        for field in pdf_form.fields:
            cat = field.category.value if field.category else "uncategorized"
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(field.name)

        for category, fields in sorted(categories.items()):
            print(f"  {category}: {len(fields)} fields")
            for field in fields[:3]:  # Show first 3 as examples
                print(f"    - {field}")
            if len(fields) > 3:
                print(f"    ... and {len(fields) - 3} more")

    # Save outputs if requested
    if args.json:
        if container.has('json_repository'):
            repo = container.resolve('json_repository')
            stub_data = pdf_form.to_stub_dict()
            repo.save(stub_data, args.json)
            print(f"\nSaved JSON stub to {args.json}")

    if args.yaml:
        if container.has('yaml_repository'):
            repo = container.resolve('yaml_repository')
            stub_data = pdf_form.to_stub_dict()
            repo.save(stub_data, args.yaml)
            print(f"Saved YAML stub to {args.yaml}")
```

### Step 9: Add Unit Tests

```python
# tests/unit/test_extract_fields_use_case.py
import pytest
from pathlib import Path
from unittest.mock import Mock, MagicMock

from form_filler.domain.models import FormField, FieldType, PDFForm
from form_filler.application.extract_fields import ExtractFieldsUseCase

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
                required=True
            ),
            FormField(
                name="is_resident",
                field_type=FieldType.BOOLEAN,
                default_value=False,
                required=False
            )
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

    def test_extract_fields_with_json_output(
        self, mock_pdf_processor, mock_repository
    ):
        """Test extracting fields and saving to JSON."""
        use_case = ExtractFieldsUseCase(
            pdf_processor=mock_pdf_processor,
            repository=mock_repository
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
        mock_categorizer.categorize = Mock(
            side_effect=lambda f: FieldCategory.PERSONAL
        )

        use_case = ExtractFieldsUseCase(
            pdf_processor=mock_pdf_processor,
            categorizer=mock_categorizer
        )

        pdf_path = Path("test.pdf")
        result = use_case.execute(pdf_path)

        assert all(
            field.category == FieldCategory.PERSONAL
            for field in result.fields
        )
        assert mock_categorizer.categorize.call_count == 2
```

### Step 10: Integration Test

```python
# tests/integration/test_pdf_extraction_integration.py
import pytest
from pathlib import Path
import tempfile

from form_filler.container import setup_container, container
from form_filler.application.extract_fields import ExtractFieldsUseCase
from form_filler.domain.interfaces import PDFProcessor

class TestPDFExtractionIntegration:
    """Integration tests for PDF extraction."""

    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup test environment."""
        setup_container()

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
        with tempfile.NamedTemporaryFile(
            suffix='.json', delete=False
        ) as tmp:
            output_path = Path(tmp.name)

        pdf_processor = container.resolve(PDFProcessor)
        repo = container.resolve('json_repository')

        use_case = ExtractFieldsUseCase(
            pdf_processor=pdf_processor,
            repository=repo
        )

        result = use_case.execute(sample_pdf, output_path)

        assert output_path.exists()
        assert result.field_count > 0

        # Cleanup
        output_path.unlink()
```

## Benefits of This Refactoring

### 1. **Testability**
- Each component can be tested in isolation
- Mock dependencies easily injected
- Clear separation between unit and integration tests

### 2. **Maintainability**
- Single responsibility for each class
- Changes to PDF library don't affect business logic
- Easy to add new output formats or categorization rules

### 3. **Extensibility**
- New PDF processors can be added without changing core logic
- New repository types (database, cloud) easily added
- Categorization strategies can be swapped

### 4. **Team Collaboration**
- Clear interfaces allow parallel development
- Each developer can work on their module independently
- Integration points are well-defined

### 5. **Error Handling**
- Each layer can handle errors appropriately
- Domain exceptions provide clear error semantics
- Infrastructure errors are translated to domain errors

## Migration Path

1. **Phase 1**: Create new structure alongside legacy code
2. **Phase 2**: Implement core domain models and interfaces
3. **Phase 3**: Build infrastructure adapters
4. **Phase 4**: Implement use cases
5. **Phase 5**: Create CLI commands that use new architecture
6. **Phase 6**: Deprecate legacy scripts
7. **Phase 7**: Remove legacy code

This approach allows gradual migration without breaking existing functionality.
