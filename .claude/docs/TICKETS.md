# Development Tickets - Form Filler

This document contains detailed tickets for multi-developer workflow. Each ticket is designed to be independently assignable with clear acceptance criteria and dependencies.

## Ticket Status Legend
- 🟢 **Ready**: No blockers, can be started immediately
- 🟡 **Blocked**: Waiting on dependencies
- 🔵 **In Progress**: Currently being worked on
- ✅ **Done**: Completed and merged

---

## Phase 1: Domain Layer

### 🟢 Ticket #1: Domain Models
**Priority**: P0 (Critical)
**Effort**: 3 days
**Assignee**: TBD
**Dependencies**: None

**Description**:
Implement core domain models representing the business entities with no external dependencies.

**Tasks**:
- [ ] Create `src/form_filler/domain/models.py`
- [ ] Implement `FormField` class with properties: name, field_type, required, category, default_value
- [ ] Implement `UserData` class as a container for user information with validation
- [ ] Implement `PDFForm` class with field collection and metadata
- [ ] Implement `FieldMapping` class to represent user-data-to-form-field mappings
- [ ] Add comprehensive docstrings with examples
- [ ] Add `__repr__` and `__eq__` methods for all classes

**Acceptance Criteria**:
- [ ] All domain models are dataclasses or Pydantic models
- [ ] No external library dependencies (pure Python)
- [ ] 100% type coverage with mypy
- [ ] All classes have comprehensive docstrings
- [ ] Unit tests cover all model creation and validation scenarios
- [ ] Test coverage ≥95%

**Files to Create**:
- `src/form_filler/domain/__init__.py`
- `src/form_filler/domain/models.py`
- `tests/unit/domain/test_models.py`

**Example**:
```python
@dataclass(frozen=True)
class FormField:
    name: str
    field_type: FieldType
    required: bool = False
    category: Optional[FieldCategory] = None
    default_value: Optional[str] = None
```

---

### 🟢 Ticket #2: Value Objects
**Priority**: P0 (Critical)
**Effort**: 2 days
**Assignee**: TBD
**Dependencies**: None

**Description**:
Implement value objects for domain concepts that should be immutable and validated.

**Tasks**:
- [ ] Create `src/form_filler/domain/value_objects.py`
- [ ] Implement `FieldType` enum (TEXT, BOOLEAN, DATE, NUMBER, CHECKBOX, RADIO, DROPDOWN)
- [ ] Implement `FieldCategory` enum (PERSONAL, ADDRESS, CONTACT, FINANCIAL, EMPLOYMENT, OTHER)
- [ ] Implement `FilePath` value object with validation
- [ ] Implement `FieldValue` value object with type-safe conversions
- [ ] Add validation logic for each value object

**Acceptance Criteria**:
- [ ] All value objects are immutable (frozen dataclasses or enums)
- [ ] Validation raises appropriate exceptions for invalid values
- [ ] Value objects implement equality comparison
- [ ] Type hints are complete and verified
- [ ] Unit tests cover all valid and invalid cases
- [ ] Test coverage ≥95%

**Files to Create**:
- `src/form_filler/domain/value_objects.py`
- `tests/unit/domain/test_value_objects.py`

---

### 🟢 Ticket #3: Domain Interfaces (Protocols)
**Priority**: P0 (Critical)
**Effort**: 2 days
**Assignee**: TBD
**Dependencies**: Ticket #1 (Domain Models)

**Description**:
Define abstract interfaces (protocols) for infrastructure dependencies using Python's Protocol typing.

**Tasks**:
- [ ] Create `src/form_filler/domain/interfaces.py`
- [ ] Define `PDFProcessor` protocol with methods: extract_fields, fill_form, validate_form
- [ ] Define `DataRepository` protocol with methods: load, save, exists, list_profiles
- [ ] Define `LLMProvider` protocol with methods: generate_text, extract_structured_data
- [ ] Define `FieldMatcher` protocol with methods: match_fields, fuzzy_match, confidence_score
- [ ] Add comprehensive type hints and docstrings

**Acceptance Criteria**:
- [ ] All interfaces use Python's `Protocol` from typing
- [ ] Methods have complete type annotations
- [ ] Docstrings explain contract expectations
- [ ] No implementation details, only contracts
- [ ] Protocols are runtime-checkable where appropriate
- [ ] Examples provided in docstrings

**Files to Create**:
- `src/form_filler/domain/interfaces.py`
- `tests/unit/domain/test_interfaces.py` (structural tests)

**Example**:
```python
class PDFProcessor(Protocol):
    """Protocol for PDF processing operations."""

    def extract_fields(self, pdf_path: Path) -> list[FormField]:
        """Extract form fields from a PDF."""
        ...
```

---

### 🟢 Ticket #4: Domain Exceptions & Validators
**Priority**: P0 (Critical)
**Effort**: 2 days
**Assignee**: TBD
**Dependencies**: Ticket #1, #2

**Description**:
Implement domain-specific exceptions and business rule validators.

**Tasks**:
- [ ] Create `src/form_filler/domain/exceptions.py`
- [ ] Implement `FormFillerException` as base exception
- [ ] Implement specific exceptions: `PDFProcessingError`, `DataValidationError`, `FieldMappingError`, `FileNotFoundError`
- [ ] Create `src/form_filler/domain/validators.py`
- [ ] Implement validators: `validate_field_value`, `validate_user_data`, `validate_field_mapping`
- [ ] Add validation rules for required fields, data types, value ranges

**Acceptance Criteria**:
- [ ] Exception hierarchy is clear and meaningful
- [ ] All exceptions include helpful error messages
- [ ] Validators raise appropriate domain exceptions
- [ ] Validators are pure functions (no side effects)
- [ ] Unit tests cover all validation scenarios
- [ ] Test coverage ≥95%

**Files to Create**:
- `src/form_filler/domain/exceptions.py`
- `src/form_filler/domain/validators.py`
- `tests/unit/domain/test_exceptions.py`
- `tests/unit/domain/test_validators.py`

---

## Phase 2: Infrastructure Adapters

### Track A: PDF Processing

### 🟡 Ticket #5: PDF Infrastructure Setup
**Priority**: P0 (Critical)
**Effort**: 1 day
**Assignee**: TBD
**Dependencies**: Ticket #3 (Domain Interfaces)

**Description**:
Set up infrastructure for PDF processing with clear interface definition.

**Tasks**:
- [ ] Create directory structure: `src/form_filler/infrastructure/pdf/`
- [ ] Create `interface.py` re-exporting domain `PDFProcessor` protocol
- [ ] Add adapter-specific types if needed
- [ ] Set up integration test fixtures with sample PDFs

**Acceptance Criteria**:
- [ ] Directory structure matches plan
- [ ] Interface clearly documented
- [ ] Test fixtures include valid and invalid PDFs
- [ ] README in directory explains adapter purpose

**Files to Create**:
- `src/form_filler/infrastructure/__init__.py`
- `src/form_filler/infrastructure/pdf/__init__.py`
- `src/form_filler/infrastructure/pdf/interface.py`
- `tests/integration/infrastructure/pdf/fixtures/` (directory)

---

### 🟡 Ticket #6: PyPDFForm Adapter Implementation
**Priority**: P0 (Critical)
**Effort**: 4 days
**Assignee**: TBD
**Dependencies**: Ticket #5

**Description**:
Implement PDF processor adapter using PyPDFForm library.

**Tasks**:
- [ ] Create `pypdfform_adapter.py`
- [ ] Implement `PyPDFFormAdapter` class implementing `PDFProcessor`
- [ ] Implement `extract_fields` method using PyPDFForm's schema API
- [ ] Implement `fill_form` method with adobe_mode=True
- [ ] Implement `validate_form` method checking field compatibility
- [ ] Add error handling and conversion to domain exceptions
- [ ] Map PyPDFForm types to domain `FieldType`

**Acceptance Criteria**:
- [ ] Adapter implements complete `PDFProcessor` protocol
- [ ] All PyPDFForm exceptions converted to domain exceptions
- [ ] Adobe compatibility mode enabled by default
- [ ] Integration tests with real PDFs pass
- [ ] Test coverage ≥90%
- [ ] No direct PyPDFForm dependencies outside this adapter

**Files to Create**:
- `src/form_filler/infrastructure/pdf/pypdfform_adapter.py`
- `tests/integration/infrastructure/pdf/test_pypdfform_adapter.py`

---

### 🟡 Ticket #7: PDF Factory
**Priority**: P1 (High)
**Effort**: 1 day
**Assignee**: TBD
**Dependencies**: Ticket #6

**Description**:
Implement factory for creating PDF processor instances.

**Tasks**:
- [ ] Create `factory.py`
- [ ] Implement `PDFProcessorFactory` class
- [ ] Support creating processors by name: "pypdfform", "default"
- [ ] Add configuration support for processor options
- [ ] Future-proof for multiple PDF library support

**Acceptance Criteria**:
- [ ] Factory returns correct adapter instances
- [ ] Unknown processor names raise clear errors
- [ ] Configuration can be passed to adapters
- [ ] Unit tests cover all factory scenarios
- [ ] Test coverage ≥95%

**Files to Create**:
- `src/form_filler/infrastructure/pdf/factory.py`
- `tests/unit/infrastructure/pdf/test_factory.py`

---

### Track B: Data Persistence

### 🟡 Ticket #8: Persistence Infrastructure Setup
**Priority**: P0 (Critical)
**Effort**: 1 day
**Assignee**: TBD
**Dependencies**: Ticket #3 (Domain Interfaces)

**Description**:
Set up infrastructure for data persistence with repository pattern.

**Tasks**:
- [ ] Create directory structure: `src/form_filler/infrastructure/persistence/`
- [ ] Create `interface.py` with `DataRepository` protocol
- [ ] Define repository operations: load, save, exists, delete, list
- [ ] Set up test fixtures with sample JSON/YAML files

**Acceptance Criteria**:
- [ ] Directory structure matches plan
- [ ] Interface supports both JSON and YAML
- [ ] Test fixtures include valid and invalid data files
- [ ] README explains repository pattern usage

**Files to Create**:
- `src/form_filler/infrastructure/persistence/__init__.py`
- `src/form_filler/infrastructure/persistence/interface.py`
- `tests/integration/infrastructure/persistence/fixtures/` (directory)

---

### 🟡 Ticket #9: JSON Repository Implementation
**Priority**: P0 (Critical)
**Effort**: 2 days
**Assignee**: TBD
**Dependencies**: Ticket #8

**Description**:
Implement repository for JSON-based user data storage.

**Tasks**:
- [ ] Create `json_repository.py`
- [ ] Implement `JSONRepository` class implementing `DataRepository`
- [ ] Implement all CRUD operations (load, save, exists, delete, list)
- [ ] Add atomic file writes (write to temp, then move)
- [ ] Add file locking to prevent concurrent modification
- [ ] Convert file system errors to domain exceptions
- [ ] Validate JSON structure against schema

**Acceptance Criteria**:
- [ ] Repository implements complete `DataRepository` protocol
- [ ] File operations are atomic and safe
- [ ] Proper error handling with domain exceptions
- [ ] Integration tests with real files pass
- [ ] Test coverage ≥90%
- [ ] Concurrent access is handled gracefully

**Files to Create**:
- `src/form_filler/infrastructure/persistence/json_repository.py`
- `tests/integration/infrastructure/persistence/test_json_repository.py`

---

### 🟡 Ticket #10: YAML Repository Implementation
**Priority**: P1 (High)
**Effort**: 2 days
**Assignee**: TBD
**Dependencies**: Ticket #8, Ticket #9 (can reuse patterns)

**Description**:
Implement repository for YAML-based user data storage.

**Tasks**:
- [ ] Create `yaml_repository.py`
- [ ] Implement `YAMLRepository` class implementing `DataRepository`
- [ ] Implement all CRUD operations
- [ ] Reuse atomic write and locking patterns from JSON repository
- [ ] Add YAML-specific validation
- [ ] Handle PyYAML optional dependency gracefully

**Acceptance Criteria**:
- [ ] Repository implements complete `DataRepository` protocol
- [ ] Graceful handling when PyYAML not installed
- [ ] File operations match JSON repository safety
- [ ] Integration tests pass
- [ ] Test coverage ≥90%

**Files to Create**:
- `src/form_filler/infrastructure/persistence/yaml_repository.py`
- `tests/integration/infrastructure/persistence/test_yaml_repository.py`

---

### 🟡 Ticket #11: Repository Factory
**Priority**: P1 (High)
**Effort**: 1 day
**Assignee**: TBD
**Dependencies**: Ticket #9, #10

**Description**:
Implement factory for creating repository instances based on file format.

**Tasks**:
- [ ] Create `factory.py`
- [ ] Implement `RepositoryFactory` class
- [ ] Auto-detect format from file extension (.json, .yaml, .yml)
- [ ] Support explicit format specification
- [ ] Return appropriate repository instance

**Acceptance Criteria**:
- [ ] Factory returns correct repository for each format
- [ ] Auto-detection works for all supported formats
- [ ] Clear error messages for unsupported formats
- [ ] Unit tests cover all scenarios
- [ ] Test coverage ≥95%

**Files to Create**:
- `src/form_filler/infrastructure/persistence/factory.py`
- `tests/unit/infrastructure/persistence/test_factory.py`

---

### Track C: LLM Integration (Optional)

### 🟡 Ticket #12: LLM Infrastructure Setup
**Priority**: P2 (Medium, Optional)
**Effort**: 1 day
**Assignee**: TBD
**Dependencies**: Ticket #3 (Domain Interfaces)

**Description**:
Set up infrastructure for optional LLM integration.

**Tasks**:
- [ ] Create directory structure: `src/form_filler/infrastructure/llm/`
- [ ] Create `interface.py` with `LLMProvider` protocol
- [ ] Define LLM operations: generate_text, extract_structured_data, suggest_values
- [ ] Set up optional dependency handling
- [ ] Add configuration for model selection

**Acceptance Criteria**:
- [ ] Directory structure matches plan
- [ ] Interface is provider-agnostic
- [ ] Graceful handling when LLM dependencies not installed
- [ ] README explains optional nature of LLM features

**Files to Create**:
- `src/form_filler/infrastructure/llm/__init__.py`
- `src/form_filler/infrastructure/llm/interface.py`

---

### 🟡 Ticket #13: HuggingFace Adapter Implementation
**Priority**: P2 (Medium, Optional)
**Effort**: 5 days
**Assignee**: TBD
**Dependencies**: Ticket #12

**Description**:
Implement LLM provider adapter using Hugging Face Transformers.

**Tasks**:
- [ ] Create `huggingface_adapter.py`
- [ ] Implement `HuggingFaceAdapter` class implementing `LLMProvider`
- [ ] Implement model loading with caching
- [ ] Implement text generation with parameters
- [ ] Implement structured data extraction using prompts
- [ ] Add safety: sanitize outputs, validate against schema
- [ ] Create `model_manager.py` for model downloading and versioning
- [ ] Add `factory.py` for LLM provider creation

**Acceptance Criteria**:
- [ ] Adapter implements complete `LLMProvider` protocol
- [ ] Model loading is lazy and cached
- [ ] Outputs are sanitized and validated
- [ ] Graceful degradation when models unavailable
- [ ] Integration tests with small test model
- [ ] Test coverage ≥85% (lower due to external dependency)
- [ ] Memory usage is reasonable (model unloading)

**Files to Create**:
- `src/form_filler/infrastructure/llm/huggingface_adapter.py`
- `src/form_filler/infrastructure/llm/model_manager.py`
- `src/form_filler/infrastructure/llm/factory.py`
- `tests/integration/infrastructure/llm/test_huggingface_adapter.py`

---

## Phase 3: Application Layer

### Track A: Use Cases

### 🟡 Ticket #14: Extract Fields Use Case
**Priority**: P0 (Critical)
**Effort**: 3 days
**Assignee**: TBD
**Dependencies**: Ticket #1-4 (Domain), Ticket #6 (PDF Adapter)

**Description**:
Implement use case for extracting and categorizing fields from PDF forms.

**Tasks**:
- [ ] Create `src/form_filler/application/use_cases/extract_fields.py`
- [ ] Implement `ExtractFieldsUseCase` class
- [ ] Dependency inject `PDFProcessor` protocol
- [ ] Extract fields from PDF
- [ ] Categorize fields using domain logic
- [ ] Return structured DTO with categorized fields
- [ ] Create `application/dto.py` for data transfer objects

**Acceptance Criteria**:
- [ ] Use case depends only on domain interfaces (not implementations)
- [ ] Clear separation of orchestration vs business logic
- [ ] Returns DTOs, not domain models
- [ ] Unit tests with mocked PDF processor
- [ ] Integration tests with real PDF processor
- [ ] Test coverage ≥90%

**Files to Create**:
- `src/form_filler/application/__init__.py`
- `src/form_filler/application/use_cases/__init__.py`
- `src/form_filler/application/use_cases/extract_fields.py`
- `src/form_filler/application/dto.py`
- `tests/unit/application/use_cases/test_extract_fields.py`
- `tests/integration/application/test_extract_fields_integration.py`

---

### 🟡 Ticket #15: Update User Data Use Case
**Priority**: P0 (Critical)
**Effort**: 3 days
**Assignee**: TBD
**Dependencies**: Ticket #1-4 (Domain), Ticket #9-10 (Repositories)

**Description**:
Implement use case for updating user information store.

**Tasks**:
- [ ] Create `update_user_data.py`
- [ ] Implement `UpdateUserDataUseCase` class
- [ ] Dependency inject `DataRepository` protocol
- [ ] Load existing user data
- [ ] Merge new fields (only-new mode)
- [ ] Interactive review mode (future: use prompts)
- [ ] Validate before saving
- [ ] Save updated data atomically

**Acceptance Criteria**:
- [ ] Use case depends only on domain interfaces
- [ ] Supports both "only-new" and "review" modes
- [ ] Data validation before saving
- [ ] Unit tests with mocked repository
- [ ] Integration tests with real repository
- [ ] Test coverage ≥90%

**Files to Create**:
- `src/form_filler/application/use_cases/update_user_data.py`
- `tests/unit/application/use_cases/test_update_user_data.py`
- `tests/integration/application/test_update_user_data_integration.py`

---

### 🟡 Ticket #16: Fill Form Use Case
**Priority**: P0 (Critical)
**Effort**: 4 days
**Assignee**: TBD
**Dependencies**: Ticket #1-4 (Domain), Ticket #6 (PDF), Ticket #9-10 (Repositories), Ticket #18 (Field Matcher)

**Description**:
Implement use case for filling PDF forms with user data.

**Tasks**:
- [ ] Create `fill_form.py`
- [ ] Implement `FillFormUseCase` class
- [ ] Dependency inject `PDFProcessor`, `DataRepository`, `FieldMatcher` protocols
- [ ] Load user data from repository
- [ ] Extract form schema from PDF
- [ ] Match user data fields to form fields
- [ ] Fill form with matched data
- [ ] Generate output filename (naming convention)
- [ ] Save filled PDF

**Acceptance Criteria**:
- [ ] Use case orchestrates multiple dependencies
- [ ] Field matching is delegated to FieldMatcher service
- [ ] Proper error handling for missing fields
- [ ] Output naming follows convention: `{input}_autofilled.pdf`
- [ ] Unit tests with mocked dependencies
- [ ] Integration tests with real components
- [ ] Test coverage ≥90%

**Files to Create**:
- `src/form_filler/application/use_cases/fill_form.py`
- `tests/unit/application/use_cases/test_fill_form.py`
- `tests/integration/application/test_fill_form_integration.py`

---

### 🟡 Ticket #17: Validate Data Use Case
**Priority**: P1 (High)
**Effort**: 2 days
**Assignee**: TBD
**Dependencies**: Ticket #1-4 (Domain)

**Description**:
Implement use case for validating user data against form requirements.

**Tasks**:
- [ ] Create `validate_data.py`
- [ ] Implement `ValidateDataUseCase` class
- [ ] Validate required fields are present
- [ ] Validate field types match
- [ ] Validate value constraints (ranges, formats)
- [ ] Return validation report with issues

**Acceptance Criteria**:
- [ ] Comprehensive validation coverage
- [ ] Clear validation error messages
- [ ] Returns structured validation report
- [ ] Unit tests cover all validation rules
- [ ] Test coverage ≥95%

**Files to Create**:
- `src/form_filler/application/use_cases/validate_data.py`
- `tests/unit/application/use_cases/test_validate_data.py`

---

### Track B: Services

### 🟢 Ticket #18: Field Matcher Service
**Priority**: P0 (Critical)
**Effort**: 4 days
**Assignee**: TBD
**Dependencies**: Ticket #1-4 (Domain)

**Description**:
Implement field matching service using Chain of Responsibility pattern.

**Tasks**:
- [ ] Create `field_matcher.py`
- [ ] Implement base `FieldMatcher` abstract class
- [ ] Implement `ExactFieldMatcher` (exact string match)
- [ ] Implement `CaseInsensitiveFieldMatcher`
- [ ] Implement `FuzzyFieldMatcher` (using difflib)
- [ ] Implement `ChainFieldMatcher` to compose matchers
- [ ] Add confidence scoring for fuzzy matches
- [ ] Support custom matching strategies

**Acceptance Criteria**:
- [ ] Chain of Responsibility pattern correctly implemented
- [ ] Each matcher is independently testable
- [ ] Matchers can be composed flexibly
- [ ] Fuzzy matching has configurable threshold
- [ ] Unit tests for each matcher strategy
- [ ] Test coverage ≥95%

**Files to Create**:
- `src/form_filler/application/services/__init__.py`
- `src/form_filler/application/services/field_matcher.py`
- `tests/unit/application/services/test_field_matcher.py`

**Example**:
```python
matcher = ChainFieldMatcher([
    ExactFieldMatcher(),
    CaseInsensitiveFieldMatcher(),
    FuzzyFieldMatcher(threshold=0.8)
])
result = matcher.match("firstName", ["first_name", "FirstName", "fname"])
```

---

### 🟢 Ticket #19: Field Categorizer Service
**Priority**: P1 (High)
**Effort**: 3 days
**Assignee**: TBD
**Dependencies**: Ticket #1-4 (Domain)

**Description**:
Implement service for categorizing form fields into logical groups.

**Tasks**:
- [ ] Create `field_categorizer.py`
- [ ] Implement `FieldCategorizationService` class
- [ ] Create rule-based categorization using field name patterns
- [ ] Support categories: PERSONAL, ADDRESS, CONTACT, FINANCIAL, EMPLOYMENT, OTHER
- [ ] Use keyword matching and regex patterns
- [ ] Make categories extensible

**Acceptance Criteria**:
- [ ] Categorization rules are data-driven (not hard-coded)
- [ ] High accuracy on common field names
- [ ] Extensible for new categories
- [ ] Unit tests with diverse field names
- [ ] Test coverage ≥90%

**Files to Create**:
- `src/form_filler/application/services/field_categorizer.py`
- `tests/unit/application/services/test_field_categorizer.py`

---

### 🟢 Ticket #20: Data Transformer Service
**Priority**: P1 (High)
**Effort**: 2 days
**Assignee**: TBD
**Dependencies**: Ticket #1-4 (Domain)

**Description**:
Implement service for transforming data between representations.

**Tasks**:
- [ ] Create `data_transformer.py`
- [ ] Implement `DataTransformerService` class
- [ ] Transform domain models to DTOs
- [ ] Transform DTOs to domain models
- [ ] Transform between data formats (date formats, boolean representations)
- [ ] Support custom transformations via strategy pattern

**Acceptance Criteria**:
- [ ] Bidirectional transformations work correctly
- [ ] No data loss in round-trip transformations
- [ ] Type-safe transformations
- [ ] Unit tests for all transformations
- [ ] Test coverage ≥95%

**Files to Create**:
- `src/form_filler/application/services/data_transformer.py`
- `tests/unit/application/services/test_data_transformer.py`

---

## Phase 4: Presentation Layer

### 🟡 Ticket #21: CLI Commands Implementation
**Priority**: P0 (Critical)
**Effort**: 5 days
**Assignee**: TBD
**Dependencies**: Ticket #14-16 (Use Cases)

**Description**:
Implement CLI command handlers for all three entry points.

**Tasks**:
- [ ] Create `src/form_filler/presentation/cli/commands.py`
- [ ] Implement `extract_required_info` command
- [ ] Implement `update_user_info` command
- [ ] Implement `fill_in_pdf` command
- [ ] Use argparse or click for argument parsing
- [ ] Integrate with dependency injection container
- [ ] Add --help documentation for all commands
- [ ] Support --verbose flag for debugging

**Acceptance Criteria**:
- [ ] All three CLI commands work end-to-end
- [ ] Clear, helpful error messages
- [ ] Proper exit codes (0 for success, 1+ for errors)
- [ ] Progress indicators for long operations
- [ ] CLI integration tests pass
- [ ] Commands work with both JSON and YAML

**Files to Create**:
- `src/form_filler/presentation/__init__.py`
- `src/form_filler/presentation/cli/__init__.py`
- `src/form_filler/presentation/cli/commands.py`
- `tests/integration/presentation/test_cli_commands.py`

---

### 🟡 Ticket #22: Output Formatters
**Priority**: P1 (High)
**Effort**: 2 days
**Assignee**: TBD
**Dependencies**: Ticket #21

**Description**:
Implement output formatters for CLI command results.

**Tasks**:
- [ ] Create `formatters.py`
- [ ] Implement `JSONFormatter` for machine-readable output
- [ ] Implement `TableFormatter` for human-readable tables
- [ ] Implement `HumanFormatter` for natural language output
- [ ] Support --format flag in CLI commands
- [ ] Support colored output (optional, with fallback)

**Acceptance Criteria**:
- [ ] All formatters produce valid output
- [ ] JSON output is valid JSON
- [ ] Table formatting is aligned and readable
- [ ] Colors work when terminal supports them, gracefully degrade otherwise
- [ ] Unit tests for all formatters
- [ ] Test coverage ≥90%

**Files to Create**:
- `src/form_filler/presentation/cli/formatters.py`
- `tests/unit/presentation/cli/test_formatters.py`

---

### 🟡 Ticket #23: Interactive Prompts
**Priority**: P2 (Medium)
**Effort**: 3 days
**Assignee**: TBD
**Dependencies**: Ticket #21

**Description**:
Implement interactive prompts for the --review mode.

**Tasks**:
- [ ] Create `prompts.py`
- [ ] Implement field value input with validation
- [ ] Implement confirmation prompts (yes/no)
- [ ] Implement review mode: show current values, allow editing
- [ ] Support multi-line input for long fields
- [ ] Add input history (up/down arrows)
- [ ] Start with simple input(), consider rich/prompt_toolkit later

**Acceptance Criteria**:
- [ ] Prompts are clear and user-friendly
- [ ] Input validation provides helpful feedback
- [ ] Review mode is intuitive
- [ ] Supports both interactive and non-interactive modes
- [ ] Integration tests with simulated input
- [ ] Test coverage ≥85%

**Files to Create**:
- `src/form_filler/presentation/cli/prompts.py`
- `tests/integration/presentation/cli/test_prompts.py`

---

## Phase 5: Integration & Configuration

### 🟡 Ticket #24: Dependency Injection Container
**Priority**: P0 (Critical)
**Effort**: 4 days
**Assignee**: TBD
**Dependencies**: All infrastructure adapters (Ticket #6-13)

**Description**:
Implement lightweight dependency injection container to wire all components.

**Tasks**:
- [ ] Create `src/form_filler/container.py`
- [ ] Implement `Container` class with service registration
- [ ] Support singleton and transient lifetimes
- [ ] Support factory functions for complex creation
- [ ] Register all infrastructure adapters
- [ ] Register all use cases and services
- [ ] Support configuration-based registration
- [ ] Add container initialization from config

**Acceptance Criteria**:
- [ ] All dependencies can be resolved from container
- [ ] Circular dependencies are detected and prevented
- [ ] Singleton lifetime is respected
- [ ] Configuration can override default registrations
- [ ] Unit tests for container functionality
- [ ] Integration tests verify full dependency graph
- [ ] Test coverage ≥90%

**Files to Create**:
- `src/form_filler/container.py`
- `tests/unit/test_container.py`
- `tests/integration/test_container_integration.py`

---

### 🟡 Ticket #25: Configuration Management
**Priority**: P0 (Critical)
**Effort**: 3 days
**Assignee**: TBD
**Dependencies**: None

**Description**:
Implement configuration management for application settings.

**Tasks**:
- [ ] Create `src/form_filler/shared/config.py`
- [ ] Support configuration from environment variables
- [ ] Support configuration from config file (~/.form_filler/config.yaml)
- [ ] Define settings: default paths, PDF processor choice, LLM model, etc.
- [ ] Implement validation for configuration values
- [ ] Support cascading: env vars > config file > defaults

**Acceptance Criteria**:
- [ ] Configuration is loaded in priority order
- [ ] Invalid configuration raises clear errors
- [ ] All settings have sensible defaults
- [ ] Configuration is immutable after load
- [ ] Unit tests for all configuration scenarios
- [ ] Test coverage ≥95%

**Files to Create**:
- `src/form_filler/shared/__init__.py`
- `src/form_filler/shared/config.py`
- `tests/unit/shared/test_config.py`

---

### 🟡 Ticket #26: Logging Setup
**Priority**: P1 (High)
**Effort**: 2 days
**Assignee**: TBD
**Dependencies**: Ticket #25 (Configuration)

**Description**:
Implement structured logging configuration.

**Tasks**:
- [ ] Create `logging_config.py`
- [ ] Configure Python logging with appropriate levels
- [ ] Support log levels from configuration
- [ ] Add contextual logging (include operation, user, etc.)
- [ ] Support log output to file and console
- [ ] Use structured logging format (JSON for production)
- [ ] Sanitize sensitive data in logs

**Acceptance Criteria**:
- [ ] Logging works across all modules
- [ ] Log levels can be configured
- [ ] Sensitive data is never logged
- [ ] Log format is consistent
- [ ] Integration tests verify logging works
- [ ] Test coverage ≥85%

**Files to Create**:
- `src/form_filler/shared/logging_config.py`
- `tests/unit/shared/test_logging_config.py`

---

## Phase 6: Testing & Quality

### 🟡 Ticket #27: Integration Test Suite
**Priority**: P0 (Critical)
**Effort**: 5 days
**Assignee**: TBD
**Dependencies**: All implementation tickets

**Description**:
Create comprehensive integration test suite covering cross-layer interactions.

**Tasks**:
- [ ] Create `tests/integration/test_extract_workflow.py`
- [ ] Create `tests/integration/test_update_workflow.py`
- [ ] Create `tests/integration/test_fill_workflow.py`
- [ ] Test complete workflows with real adapters
- [ ] Use test fixtures with sample PDFs and data
- [ ] Test error scenarios and edge cases
- [ ] Measure and report test coverage

**Acceptance Criteria**:
- [ ] All major workflows have integration tests
- [ ] Tests use real infrastructure components (not mocks)
- [ ] Tests are repeatable and isolated
- [ ] Tests run in CI pipeline
- [ ] Integration test coverage ≥80%

**Files to Create**:
- `tests/integration/test_extract_workflow.py`
- `tests/integration/test_update_workflow.py`
- `tests/integration/test_fill_workflow.py`

---

### 🟡 Ticket #28: End-to-End Test Suite
**Priority**: P0 (Critical)
**Effort**: 3 days
**Assignee**: TBD
**Dependencies**: Ticket #21-23 (CLI), Ticket #27 (Integration Tests)

**Description**:
Create end-to-end test suite simulating real user workflows.

**Tasks**:
- [ ] Create `tests/e2e/test_complete_flow.py`
- [ ] Test complete user journey: extract → update → fill
- [ ] Use real PDF files and data files
- [ ] Test CLI commands via subprocess
- [ ] Verify generated PDFs are valid
- [ ] Test error scenarios (missing files, invalid data)

**Acceptance Criteria**:
- [ ] E2E tests cover all CLI commands
- [ ] Tests run in clean environment
- [ ] Tests verify actual file outputs
- [ ] Tests are documented and maintainable
- [ ] E2E tests pass in CI

**Files to Create**:
- `tests/e2e/__init__.py`
- `tests/e2e/test_complete_flow.py`
- `tests/e2e/test_error_scenarios.py`

---

### 🟡 Ticket #29: Performance Testing
**Priority**: P2 (Medium)
**Effort**: 3 days
**Assignee**: TBD
**Dependencies**: All implementation tickets

**Description**:
Create performance tests to ensure acceptable performance.

**Tasks**:
- [ ] Create `tests/performance/test_large_forms.py`
- [ ] Test with forms containing 100+ fields
- [ ] Test batch processing of multiple forms
- [ ] Measure memory usage during LLM operations
- [ ] Set performance benchmarks (e.g., <5s per form)
- [ ] Profile slow operations

**Acceptance Criteria**:
- [ ] Performance benchmarks are met
- [ ] Memory usage is reasonable (<500MB without LLM)
- [ ] No memory leaks detected
- [ ] Performance tests run in CI (with limits)
- [ ] Performance report generated

**Files to Create**:
- `tests/performance/__init__.py`
- `tests/performance/test_large_forms.py`
- `tests/performance/test_batch_processing.py`

---

### 🟡 Ticket #30: Security Audit
**Priority**: P0 (Critical)
**Effort**: 3 days
**Assignee**: TBD
**Dependencies**: All implementation tickets

**Description**:
Conduct security audit of the codebase and data handling.

**Tasks**:
- [ ] Run bandit security scanner, fix all issues
- [ ] Review all file I/O for path traversal vulnerabilities
- [ ] Verify user data is never logged or leaked
- [ ] Test that resources/user_info/ is never committed
- [ ] Review LLM output sanitization
- [ ] Check for SQL injection (if databases added later)
- [ ] Verify dependencies for known vulnerabilities
- [ ] Document security considerations

**Acceptance Criteria**:
- [ ] Zero bandit security issues
- [ ] No path traversal vulnerabilities
- [ ] Sensitive data protection verified
- [ ] Dependency vulnerabilities addressed
- [ ] Security audit report completed
- [ ] CI includes security scanning

**Files to Create**:
- `.github/workflows/security.yml` (if not exists)
- `docs/SECURITY.md`

---

## Phase 7: Documentation

### 🟡 Ticket #31: API Documentation
**Priority**: P1 (High)
**Effort**: 3 days
**Assignee**: TBD
**Dependencies**: All implementation tickets

**Description**:
Complete API documentation with docstrings and examples.

**Tasks**:
- [ ] Review all public APIs for complete docstrings
- [ ] Add usage examples to all use cases
- [ ] Add type hints verification (mypy --strict)
- [ ] Generate API documentation (Sphinx or mkdocs)
- [ ] Add code examples for common scenarios
- [ ] Document all interfaces and protocols

**Acceptance Criteria**:
- [ ] 100% of public APIs have docstrings
- [ ] All examples are tested and working
- [ ] API documentation is browsable (HTML)
- [ ] Type coverage is 100%
- [ ] Documentation is published (GitHub Pages or ReadTheDocs)

**Files to Create**:
- `docs/api/` (directory)
- `docs/conf.py` (if using Sphinx)

---

### 🟡 Ticket #32: User Guide
**Priority**: P1 (High)
**Effort**: 4 days
**Assignee**: TBD
**Dependencies**: Ticket #21-23 (CLI)

**Description**:
Write comprehensive user guide with examples and tutorials.

**Tasks**:
- [ ] Write installation guide for all platforms
- [ ] Create quick start tutorial
- [ ] Document all CLI commands with examples
- [ ] Add troubleshooting section
- [ ] Add FAQ section
- [ ] Create video tutorial (optional)
- [ ] Add screenshots of CLI output

**Acceptance Criteria**:
- [ ] User guide covers all features
- [ ] Examples are tested and working
- [ ] Troubleshooting covers common issues
- [ ] Guide is accessible (Markdown or HTML)
- [ ] Guide is linked from README

**Files to Create**:
- `docs/user-guide/installation.md`
- `docs/user-guide/quick-start.md`
- `docs/user-guide/commands.md`
- `docs/user-guide/troubleshooting.md`
- `docs/user-guide/faq.md`

---

### 🟡 Ticket #33: Developer Guide
**Priority**: P1 (High)
**Effort**: 3 days
**Assignee**: TBD
**Dependencies**: All implementation tickets

**Description**:
Write developer guide for contributors.

**Tasks**:
- [ ] Document architecture and design patterns
- [ ] Create architecture diagrams (update existing)
- [ ] Write contributing guidelines
- [ ] Document coding standards
- [ ] Explain testing strategy
- [ ] Add guide for adding new adapters/plugins
- [ ] Document release process

**Acceptance Criteria**:
- [ ] Architecture is clearly explained
- [ ] Diagrams are up-to-date
- [ ] Contributing guide is complete
- [ ] Extension points are documented
- [ ] Guide helps new contributors onboard

**Files to Create**:
- `docs/developer-guide/architecture.md`
- `docs/developer-guide/contributing.md`
- `docs/developer-guide/testing.md`
- `docs/developer-guide/extending.md`
- `CONTRIBUTING.md` (root)

---

## Ticket Dependencies Graph

```
Phase 1: Domain Layer
[1] → [3] → [5,8,12]
[2] → [4]
[1,2] → [4]

Phase 2: Infrastructure
[3,5] → [6] → [7]
[3,8] → [9,10] → [11]
[3,12] → [13]

Phase 3: Application
[1-4,6] → [14]
[1-4,9-10] → [15]
[1-4] → [18,19,20]
[1-4,6,9-10,18] → [16]
[1-4] → [17]

Phase 4: Presentation
[14-16] → [21] → [22,23]

Phase 5: Integration
[6-13] → [24]
[] → [25] → [26]

Phase 6: Testing
[All] → [27,28,29,30]

Phase 7: Documentation
[All] → [31,32,33]
```

---

## Development Guidelines

### Ticket Assignment
1. Review ticket dependencies before starting
2. Communicate with team about related tickets
3. Update ticket status when starting work
4. Create draft PR early for feedback
5. Mark ticket done only after PR is merged

### Code Review Checklist
- [ ] Follows architectural guidelines (layer dependencies)
- [ ] Has complete type hints
- [ ] Has comprehensive tests (≥90% coverage)
- [ ] Has clear docstrings
- [ ] Passes all CI checks
- [ ] No security vulnerabilities
- [ ] Follows coding standards (ruff, mypy)

### Testing Requirements
- **Unit Tests**: Fast, isolated, mock external dependencies
- **Integration Tests**: Test cross-layer interactions, use real components
- **E2E Tests**: Test via CLI, verify actual outputs

### Definition of Done
- [ ] Code implemented and follows standards
- [ ] Tests written and passing (≥90% coverage)
- [ ] Documentation updated
- [ ] PR reviewed and approved
- [ ] CI passing (all checks green)
- [ ] Merged to main branch

---

## Quick Reference

### Parallel Development Opportunities

**Week 1** (Can work in parallel):
- Ticket #1: Domain Models
- Ticket #2: Value Objects
- Ticket #3: Domain Interfaces
- Ticket #4: Exceptions & Validators

**Week 2** (Can work in parallel):
- Ticket #5-7: PDF Track
- Ticket #8-11: Persistence Track
- Ticket #12-13: LLM Track (optional)

**Week 3** (Some parallelism):
- Ticket #14-17: Use Cases (sequential dependencies)
- Ticket #18-20: Services (parallel, independent)

### Priority Legend
- **P0 (Critical)**: Must have for v1.0
- **P1 (High)**: Important for v1.0
- **P2 (Medium)**: Nice to have for v1.0
- **P3 (Low)**: Future enhancement

### Effort Estimates
- 1 day: Simple implementation
- 2-3 days: Medium complexity
- 4-5 days: Complex implementation
- 5+ days: Very complex or research needed

---

## Notes for Multi-Developer Teams

1. **Domain First**: All developers should review and agree on domain models (Tickets #1-4) before starting infrastructure work.

2. **Interface Contracts**: Finalize domain interfaces early so infrastructure tracks can proceed independently.

3. **Mock for Testing**: Use mocks/stubs during unit testing so you don't wait for infrastructure implementations.

4. **Weekly Integration**: Plan weekly integration sessions to wire components together.

5. **Communication**: Use ticket references in commits and PRs for traceability.

6. **Incremental**: Aim for vertical slices - get one feature working end-to-end before moving to next.

---

**Last Updated**: 2025-11-12
**Status**: Ready for development
