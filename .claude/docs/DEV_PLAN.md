# Development Plan - Form Filler (Modular Architecture)

## Project Overview

A Python-based utility for semi-automatically filling PDF forms with LLM assistance, designed with a clean hexagonal architecture for maintainability, testability, and parallel development.

## Architecture Philosophy

This project follows **Hexagonal Architecture** (Ports & Adapters) with clear separation of concerns:
- **Domain**: Pure business logic with no external dependencies
- **Application**: Use case orchestration
- **Infrastructure**: External library adapters (PDF, storage, LLM)
- **Presentation**: User interfaces (CLI, future web)

See [ARCHITECTURAL_REVIEW.md](../../ARCHITECTURAL_REVIEW.md) for detailed analysis.

## Development Environment

### Prerequisites
- Python >= 3.13
- uv (Python package installer)
- Git
- Pre-commit hooks

### Setup
```bash
# Install in development mode
uv pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install

# Run tests
pytest
```

## Modular Project Structure

```
form_filler/
├── src/form_filler/
│   ├── __init__.py
│   │
│   ├── domain/                      # Domain Layer (Pure Python)
│   │   ├── __init__.py
│   │   ├── models.py                # Domain models (FormField, UserData, PDFForm)
│   │   ├── interfaces.py            # Abstract protocols/interfaces
│   │   ├── value_objects.py         # Value objects (FieldType, Category)
│   │   ├── exceptions.py            # Domain exceptions
│   │   └── validators.py            # Business rule validators
│   │
│   ├── application/                 # Application Layer (Use Cases)
│   │   ├── __init__.py
│   │   ├── use_cases/
│   │   │   ├── __init__.py
│   │   │   ├── extract_fields.py   # ExtractFieldsUseCase
│   │   │   ├── update_user_data.py # UpdateUserDataUseCase
│   │   │   ├── fill_form.py        # FillFormUseCase
│   │   │   └── validate_data.py    # ValidateDataUseCase
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── field_categorizer.py    # Field categorization service
│   │   │   ├── field_matcher.py        # Field matching service
│   │   │   └── data_transformer.py     # Data transformation service
│   │   └── dto.py                   # Data Transfer Objects
│   │
│   ├── infrastructure/              # Infrastructure Layer (Adapters)
│   │   ├── __init__.py
│   │   ├── pdf/
│   │   │   ├── __init__.py
│   │   │   ├── interface.py        # PDFProcessor protocol
│   │   │   ├── pypdfform_adapter.py # PyPDFForm implementation
│   │   │   └── factory.py          # PDF processor factory
│   │   ├── persistence/
│   │   │   ├── __init__.py
│   │   │   ├── interface.py        # Repository protocol
│   │   │   ├── json_repository.py  # JSON storage
│   │   │   ├── yaml_repository.py  # YAML storage
│   │   │   └── factory.py          # Repository factory
│   │   └── llm/
│   │       ├── __init__.py
│   │       ├── interface.py        # LLMProvider protocol
│   │       ├── huggingface_adapter.py  # HuggingFace implementation
│   │       ├── model_manager.py    # Model loading/management
│   │       └── factory.py          # LLM provider factory
│   │
│   ├── presentation/                # Presentation Layer
│   │   ├── __init__.py
│   │   ├── cli/
│   │   │   ├── __init__.py
│   │   │   ├── commands.py         # CLI command implementations
│   │   │   ├── formatters.py       # Output formatting
│   │   │   └── prompts.py          # Interactive prompts
│   │   └── web/                    # Future: Web interface
│   │       └── __init__.py
│   │
│   ├── shared/                      # Shared Kernel
│   │   ├── __init__.py
│   │   ├── logging_config.py       # Logging setup
│   │   └── config.py               # Configuration management
│   │
│   └── container.py                 # Dependency injection container
│
├── tests/
│   ├── unit/                        # Unit tests (isolated)
│   │   ├── domain/
│   │   ├── application/
│   │   └── infrastructure/
│   ├── integration/                 # Integration tests
│   │   ├── test_extract_workflow.py
│   │   ├── test_update_workflow.py
│   │   └── test_fill_workflow.py
│   ├── e2e/                         # End-to-end tests
│   │   └── test_complete_flow.py
│   ├── fixtures/                    # Test data
│   │   ├── sample_forms/
│   │   └── sample_data/
│   └── conftest.py
│
├── resources/                       # Data directory
│   ├── user_info/                  # User database (NEVER committed)
│   ├── examples/                   # Sample configs (committed)
│   └── output/                     # Generated PDFs (not committed)
│
├── .claude/docs/
│   ├── DEV_PLAN.md                 # This file
│   └── TICKETS.md                  # Development tickets
│
├── ARCHITECTURAL_REVIEW.md
├── ARCHITECTURE_DIAGRAM.md
├── REFACTORING_EXAMPLE.md
└── pyproject.toml
```

## Development Phases

### Phase 0: Foundation Setup ✅
**Status**: COMPLETE

- ✅ Project structure
- ✅ CI/CD pipeline
- ✅ Testing framework
- ✅ Pre-commit hooks
- ✅ Architectural review

### Phase 1: Domain Layer (Week 1)
**Goal**: Establish core domain models with no external dependencies

**Modules**:
1. **Domain Models** (`domain/models.py`)
   - `FormField`: Represents a PDF form field
   - `UserData`: Container for user information
   - `PDFForm`: Represents a complete PDF form
   - `FieldMapping`: Maps user data to form fields

2. **Value Objects** (`domain/value_objects.py`)
   - `FieldType`: Enum for field types (text, boolean, date, etc.)
   - `FieldCategory`: Enum for categories (personal, address, financial)
   - `FilePath`: Value object for validated file paths

3. **Domain Interfaces** (`domain/interfaces.py`)
   - `PDFProcessor`: Protocol for PDF operations
   - `DataRepository`: Protocol for data persistence
   - `LLMProvider`: Protocol for LLM services
   - `FieldMatcher`: Protocol for field matching

4. **Domain Exceptions** (`domain/exceptions.py`)
   - `FormFillerException`: Base exception
   - `PDFProcessingError`: PDF-related errors
   - `DataValidationError`: Data validation failures
   - `FieldMappingError`: Field mapping issues

**Dependencies**: None (pure Python)

**Tests**: Unit tests for all domain models and validators

**Ticket Reference**: See TICKETS.md #1-4

---

### Phase 2: Infrastructure Adapters (Week 2)
**Goal**: Implement adapters for external dependencies

**Track A: PDF Processing** (Independent)
1. **PDF Interface** (`infrastructure/pdf/interface.py`)
2. **PyPDFForm Adapter** (`infrastructure/pdf/pypdfform_adapter.py`)
3. **PDF Factory** (`infrastructure/pdf/factory.py`)

**Track B: Data Persistence** (Independent)
1. **Repository Interface** (`infrastructure/persistence/interface.py`)
2. **JSON Repository** (`infrastructure/persistence/json_repository.py`)
3. **YAML Repository** (`infrastructure/persistence/yaml_repository.py`)
4. **Repository Factory** (`infrastructure/persistence/factory.py`)

**Track C: LLM Integration** (Independent, Optional)
1. **LLM Interface** (`infrastructure/llm/interface.py`)
2. **HuggingFace Adapter** (`infrastructure/llm/huggingface_adapter.py`)
3. **Model Manager** (`infrastructure/llm/model_manager.py`)
4. **LLM Factory** (`infrastructure/llm/factory.py`)

**Dependencies**:
- Track A: PyPDFForm
- Track B: PyYAML
- Track C: transformers, torch (optional)

**Tests**: Integration tests with mocked domain layer

**Ticket Reference**: See TICKETS.md #5-13

**Parallel Development**: All three tracks can be developed simultaneously by different developers

---

### Phase 3: Application Layer (Week 3)
**Goal**: Implement use cases and application services

**Track A: Use Cases** (Depends on Infrastructure)
1. **Extract Fields Use Case** (`application/use_cases/extract_fields.py`)
   - Dependencies: PDFProcessor

2. **Update User Data Use Case** (`application/use_cases/update_user_data.py`)
   - Dependencies: DataRepository

3. **Fill Form Use Case** (`application/use_cases/fill_form.py`)
   - Dependencies: PDFProcessor, DataRepository, FieldMatcher

4. **Validate Data Use Case** (`application/use_cases/validate_data.py`)
   - Dependencies: Domain validators

**Track B: Services** (Independent)
1. **Field Categorizer** (`application/services/field_categorizer.py`)
   - Rule-based field categorization

2. **Field Matcher** (`application/services/field_matcher.py`)
   - Chain of responsibility pattern for field matching
   - Strategies: exact match, fuzzy match, LLM-assisted

3. **Data Transformer** (`application/services/data_transformer.py`)
   - Transform between formats and representations

**Dependencies**: Domain layer, Infrastructure adapters

**Tests**: Unit tests with mocked infrastructure

**Ticket Reference**: See TICKETS.md #14-20

---

### Phase 4: Presentation Layer (Week 4)
**Goal**: Implement CLI commands

1. **CLI Commands** (`presentation/cli/commands.py`)
   - `extract_required_info`: Calls ExtractFieldsUseCase
   - `update_user_info`: Calls UpdateUserDataUseCase
   - `fill_in_pdf`: Calls FillFormUseCase

2. **Output Formatters** (`presentation/cli/formatters.py`)
   - JSON formatter
   - Table formatter
   - Human-readable formatter

3. **Interactive Prompts** (`presentation/cli/prompts.py`)
   - Field value input
   - Confirmation prompts
   - Review mode

**Dependencies**: Application layer

**Tests**: CLI integration tests

**Ticket Reference**: See TICKETS.md #21-23

---

### Phase 5: Integration & Configuration (Week 5)
**Goal**: Wire everything together with dependency injection

1. **Dependency Container** (`container.py`)
   - Service registration
   - Lifecycle management
   - Configuration-based wiring

2. **Configuration Management** (`shared/config.py`)
   - Environment-based configuration
   - Default settings
   - Validation

3. **Logging Setup** (`shared/logging_config.py`)
   - Structured logging
   - Log levels
   - Output formatting

**Ticket Reference**: See TICKETS.md #24-26

---

### Phase 6: Testing & Quality (Week 6)
**Goal**: Comprehensive test coverage and quality assurance

1. **Integration Tests** (`tests/integration/`)
   - Workflow tests
   - Cross-layer tests

2. **End-to-End Tests** (`tests/e2e/`)
   - Complete user workflows
   - Real PDF files

3. **Performance Tests**
   - Large form handling
   - Multiple file processing

4. **Security Audit**
   - Dependency scanning
   - Data protection verification

**Ticket Reference**: See TICKETS.md #27-30

---

### Phase 7: Documentation & Polish (Week 7)
**Goal**: Complete documentation and user experience

1. **API Documentation**
   - Docstring completion
   - Type hint verification
   - Example code

2. **User Guide**
   - Installation instructions
   - Usage examples
   - Troubleshooting

3. **Developer Guide**
   - Architecture overview
   - Contributing guidelines
   - Extension points

**Ticket Reference**: See TICKETS.md #31-33

---

## Key Design Patterns

### 1. Hexagonal Architecture (Ports & Adapters)
- Domain at center, infrastructure at edges
- Dependency inversion at layer boundaries

### 2. Dependency Injection
- Constructor injection for dependencies
- Container-based service resolution

### 3. Repository Pattern
- Abstraction over data persistence
- Supports multiple storage formats

### 4. Strategy Pattern
- Swappable PDF processors
- Multiple field matching strategies

### 5. Chain of Responsibility
- Field matching with fallback options
- Data transformation pipeline

### 6. Factory Pattern
- Infrastructure adapter creation
- Service instantiation

### 7. Plugin Architecture
- Optional LLM features
- Extensible field matchers

## Module Dependency Rules

### Allowed Dependencies
```
Domain → None (pure Python)
Application → Domain
Infrastructure → Domain, Application (implements interfaces)
Presentation → Application, Domain (not Infrastructure)
Shared → None
```

### Forbidden Dependencies
```
Domain → Application ❌
Domain → Infrastructure ❌
Domain → Presentation ❌
Application → Infrastructure ❌ (only via interfaces)
Infrastructure → Presentation ❌
```

## Parallel Development Strategy

### Independent Tracks

**Track 1: PDF Processing**
- Developer A
- Modules: `infrastructure/pdf/*`
- Interface: `PDFProcessor`
- No blockers

**Track 2: Data Persistence**
- Developer B
- Modules: `infrastructure/persistence/*`
- Interface: `DataRepository`
- No blockers

**Track 3: LLM Integration**
- Developer C
- Modules: `infrastructure/llm/*`
- Interface: `LLMProvider`
- No blockers (optional feature)

**Track 4: Application Services**
- Developer D
- Modules: `application/services/*`
- Depends on: Domain models
- Can mock infrastructure

**Track 5: CLI Layer**
- Developer E
- Modules: `presentation/cli/*`
- Depends on: Application use cases
- Can mock infrastructure

### Integration Points

**Weekly Integration**:
1. Domain interfaces reviewed and finalized
2. Infrastructure adapters integrated via dependency injection
3. Use cases wired to adapters
4. CLI commands connected to use cases
5. Integration tests verify connections

## Testing Strategy

### Test Pyramid

```
        /\
       /e2e\         <- End-to-end (few, slow)
      /------\
     /integ.  \      <- Integration (some, medium)
    /----------\
   /   unit     \    <- Unit (many, fast)
  /--------------\
```

### Coverage Goals
- **Unit Tests**: 90%+ coverage
- **Integration Tests**: All cross-layer interactions
- **E2E Tests**: All CLI commands with real files

### Test Doubles
- **Mocks**: For external services (LLM, file system)
- **Stubs**: For infrastructure adapters during unit tests
- **Fakes**: In-memory repositories for integration tests

## Security Considerations

### Data Protection
- **Encryption**: User data at rest (future enhancement)
- **Audit Log**: Data access tracking
- **Validation**: Strict input validation
- **Sanitization**: LLM output sanitization

### Git Protection
- `.gitignore`: Exclude `resources/user_info/`
- CI validation: Check for sensitive data commits
- Pre-commit hooks: Prevent accidental commits

## Migration from Legacy Scripts

### Phase-wise Migration

**Phase 1**: Keep legacy scripts alongside new implementation
- `generate_stub.py` → Use new `extract-required-info`
- `fill_form.py` → Use new `fill-in-pdf`

**Phase 2**: Deprecation warnings in legacy scripts

**Phase 3**: Remove legacy scripts after stable release

## Technology Stack

### Core Dependencies
- **PyPDFForm** (>=1.4.0): PDF AcroForm manipulation
- **PyYAML** (>=6.0): YAML support
- **Python** (>=3.13): Language runtime

### Optional Dependencies
- **transformers** (>=4.30.0): LLM support
- **torch** (>=2.0.0): PyTorch backend
- **accelerate** (>=0.20.0): Model optimization

### Development Dependencies
- **pytest** (>=7.0.0): Testing
- **pytest-cov** (>=4.0.0): Coverage
- **ruff** (>=0.1.0): Linting and formatting
- **mypy** (>=1.0.0): Type checking
- **pre-commit** (>=3.0.0): Git hooks
- **bandit**: Security scanning

## Milestones & Timeline

### Milestone 1: Domain Foundation (Week 1)
- ✅ Architectural review complete
- [ ] Domain models implemented
- [ ] Interfaces defined
- [ ] Value objects created
- [ ] Unit tests passing

### Milestone 2: Infrastructure Adapters (Week 2)
- [ ] PDF adapter implemented
- [ ] Data repositories implemented
- [ ] LLM adapter implemented (optional)
- [ ] Factory patterns in place
- [ ] Integration tests passing

### Milestone 3: Application Layer (Week 3)
- [ ] All use cases implemented
- [ ] Services implemented
- [ ] Unit tests passing
- [ ] Mock-based testing complete

### Milestone 4: Presentation Layer (Week 4)
- [ ] CLI commands implemented
- [ ] Output formatting complete
- [ ] Interactive prompts working
- [ ] CLI integration tests passing

### Milestone 5: Integration (Week 5)
- [ ] Dependency injection working
- [ ] Configuration management complete
- [ ] All layers integrated
- [ ] End-to-end tests passing

### Milestone 6: Quality Assurance (Week 6)
- [ ] 90%+ test coverage achieved
- [ ] Security audit complete
- [ ] Performance testing done
- [ ] Bug fixes complete

### Milestone 7: Documentation & Release (Week 7)
- [ ] API documentation complete
- [ ] User guide written
- [ ] Developer guide written
- [ ] v1.0.0 release ready

## Success Metrics

### Code Quality
- Test coverage: ≥90%
- Type coverage: 100%
- Linting violations: 0
- Security issues: 0

### Architecture
- Circular dependencies: 0
- Layer violations: 0
- Interface segregation: All infrastructure behind protocols
- Dependency direction: Consistently inward

### Development Velocity
- Parallel development: 3+ developers working simultaneously
- Integration conflicts: Minimal
- Test execution time: <2 minutes
- Build time: <30 seconds

## Open Questions & Decisions

### Resolved
- ✅ Architecture pattern: Hexagonal Architecture
- ✅ Dependency injection: Custom lightweight container
- ✅ Testing strategy: Test pyramid with mocks/stubs/fakes

### Open
- [ ] **LLM Model Selection**: Which local model to recommend?
  - Options: Llama 2, Mistral, Phi-2
  - Criteria: Size, performance, license

- [ ] **Encryption Library**: What to use for user data encryption?
  - Options: cryptography, nacl
  - Requirement: Easy key management

- [ ] **Interactive UI Library**: For --review mode?
  - Options: rich, prompt_toolkit, simple input()
  - Decision: Start simple, enhance later

## References

- [ARCHITECTURAL_REVIEW.md](../../ARCHITECTURAL_REVIEW.md): Detailed architectural analysis
- [ARCHITECTURE_DIAGRAM.md](../../ARCHITECTURE_DIAGRAM.md): Visual diagrams
- [REFACTORING_EXAMPLE.md](../../REFACTORING_EXAMPLE.md): Code examples
- [TICKETS.md](TICKETS.md): Development tickets for multi-dev workflow
- [CLAUDE.md](../../CLAUDE.md): Project context for AI assistants
