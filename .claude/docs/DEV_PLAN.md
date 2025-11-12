# Development Plan - Form Filler

## Project Overview

A Python-based utility for semi-automatically filling PDF forms, specifically designed for the 2025 Swiss Tax Questionnaire (Departure). The project provides command-line tools with LLM assistance for extracting form fields, managing user information, and populating PDFs with user data.

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

## Architecture

### Phase 1: Core Infrastructure (Current Priority)

#### 1.1 Project Structure
```
form_filler/
├── .github/
│   └── workflows/
│       ├── ci.yml          # CI/CD pipeline
│       └── release.yml     # Release automation
├── src/
│   └── form_filler/
│       ├── __init__.py
│       ├── cli.py          # CLI entry points
│       ├── core/
│       │   ├── __init__.py
│       │   ├── form_inspector.py    # PDF schema extraction
│       │   ├── user_data_manager.py # User info CRUD
│       │   ├── field_matcher.py     # Field mapping logic
│       │   └── form_filler.py       # PDF filling
│       ├── llm/
│       │   ├── __init__.py
│       │   ├── assistant.py         # LLM integration
│       │   └── models.py            # Model management
│       └── utils/
│           ├── __init__.py
│           ├── file_io.py           # JSON/YAML handling
│           └── validators.py        # Data validation
├── tests/
│   ├── conftest.py
│   ├── test_form_inspector.py
│   ├── test_user_data_manager.py
│   ├── test_form_filler.py
│   └── test_llm_assistant.py
├── resources/
│   ├── examples/
│   └── output/
├── pyproject.toml
├── requirements.txt
├── .gitignore
├── .pre-commit-config.yaml
└── README.md
```

#### 1.2 Module Dependencies
```
cli.py
  ↓
core/ modules (form_inspector, user_data_manager, field_matcher, form_filler)
  ↓
llm/ modules (assistant, models) [optional]
  ↓
utils/ modules (file_io, validators)
```

### Phase 2: Core Modules Implementation

#### 2.1 Form Inspector (`form_inspector.py`)
**Purpose:** Extract and analyze PDF AcroForm schema

**Key Functions:**
- `extract_schema(pdf_path: Path) -> Dict[str, FieldInfo]`
- `categorize_fields(schema: Dict) -> Dict[str, List[str]]`
- `get_required_fields(schema: Dict) -> List[str]`

**Dependencies:**
- PyPDFForm (wrapper.schema)

**Status:** TODO - Build on existing `generate_stub.py`

#### 2.2 User Data Manager (`user_data_manager.py`)
**Purpose:** CRUD operations on persistent user information

**Key Functions:**
- `load_user_data(file_path: Path) -> Dict[str, Any]`
- `save_user_data(data: Dict, file_path: Path) -> None`
- `merge_fields(existing: Dict, new_fields: List[str]) -> Dict`
- `interactive_review(data: Dict) -> Dict`

**Dependencies:**
- PyYAML (optional)
- json (stdlib)

**Status:** TODO - New implementation

#### 2.3 Field Matcher (`field_matcher.py`)
**Purpose:** Map user data fields to form fields

**Key Functions:**
- `match_fields(user_data: Dict, form_fields: Dict) -> Dict[str, str]`
- `fuzzy_match(field_name: str, candidates: List[str]) -> Optional[str]`
- `validate_mapping(mapping: Dict) -> bool`

**Dependencies:**
- difflib (stdlib) for fuzzy matching

**Status:** TODO - New implementation (future enhancement)

#### 2.4 Form Filler (`form_filler.py`)
**Purpose:** Populate PDF forms with user data

**Key Functions:**
- `fill_pdf(pdf_path: Path, data: Dict, output_path: Path) -> None`
- `generate_output_name(input_path: Path) -> Path`

**Dependencies:**
- PyPDFForm (PdfWrapper)

**Status:** TODO - Build on existing `fill_form.py`

### Phase 3: LLM Integration

#### 3.1 LLM Assistant (`llm/assistant.py`)
**Purpose:** LLM-assisted form filling and data extraction

**Key Functions:**
- `extract_structured_data(text: str, schema: Dict) -> Dict`
- `suggest_field_values(field_name: str, context: Dict) -> List[str]`
- `map_natural_language(user_input: str, fields: List[str]) -> Dict`

**Dependencies:**
- transformers (Hugging Face)
- torch
- accelerate

**Status:** TODO - New implementation

#### 3.2 Model Manager (`llm/models.py`)
**Purpose:** Manage local LLM models

**Key Functions:**
- `load_model(model_name: str) -> Model`
- `list_available_models() -> List[str]`
- `download_model(model_name: str) -> None`

**Dependencies:**
- transformers
- torch

**Status:** TODO - New implementation

### Phase 4: CLI Implementation

#### 4.1 Entry Point 1: `extract-required-info`
```bash
extract-required-info form.pdf [--output info.json]
```

**Implementation:**
```python
def extract_required_info():
    """Extract required field information from PDF form."""
    # 1. Parse CLI arguments
    # 2. Call form_inspector.extract_schema()
    # 3. Call form_inspector.categorize_fields()
    # 4. Display or save results
```

**Status:** TODO

#### 4.2 Entry Point 2: `update-user-info`
```bash
update-user-info [--only-new] [--review] [--file user_info.json]
```

**Implementation:**
```python
def update_user_info():
    """Manage user information store."""
    # 1. Parse CLI arguments
    # 2. Load existing user data
    # 3. If --only-new: merge new fields from latest form
    # 4. If --review: interactive_review()
    # 5. Save updated data
```

**Status:** TODO

#### 4.3 Entry Point 3: `fill-in-pdf`
```bash
fill-in-pdf --input form.pdf --user my_info.json [--output custom_name.pdf]
```

**Implementation:**
```python
def fill_in_pdf():
    """Fill PDF form with user data."""
    # 1. Parse CLI arguments
    # 2. Load user data
    # 3. Load form schema
    # 4. Match fields (field_matcher)
    # 5. Fill PDF (form_filler)
    # 6. Save output with naming convention
```

**Status:** TODO

### Phase 5: Testing & Quality Assurance

#### 5.1 Test Coverage Goals
- Unit tests: 80%+ coverage
- Integration tests for CLI
- End-to-end tests with sample PDFs

#### 5.2 Test Data
- Sample PDF forms (anonymized)
- Sample user data (fixtures)
- Expected outputs

#### 5.3 CI/CD Pipeline
- ✅ Automated testing on push/PR
- ✅ Code quality checks (black, ruff, mypy)
- ✅ Security scanning (bandit)
- ✅ Multi-OS testing (Ubuntu, Windows, macOS)

### Phase 6: Documentation

#### 6.1 User Documentation
- README with quick start guide
- Usage examples
- Troubleshooting guide

#### 6.2 Developer Documentation
- API documentation (docstrings)
- Architecture diagrams
- Contributing guidelines

## Development Workflow

### Typical User Workflow
```
1. extract-required-info form.pdf
   → Displays required fields and categories

2. update-user-info --only-new
   → Adds missing fields to user info file
   → Optionally use --review for interactive update

3. [Optional] LLM assistance for natural language input
   → User provides information in natural language
   → LLM maps to structured fields

4. fill-in-pdf --input form.pdf --user my_info.json
   → Generates form_autofilled.pdf
```

### Developer Workflow
```
1. Create feature branch
2. Implement changes with tests
3. Run pre-commit hooks (automatic)
4. Run full test suite: pytest
5. Create PR → CI runs automatically
6. Merge after approval
7. Tag release → Automated PyPI publish
```

## Technology Stack

### Core Dependencies
- **PyPDFForm** (>=1.4.0): PDF AcroForm manipulation
- **PyYAML** (>=6.0): YAML support
- **Python** (>=3.13): Language runtime

### LLM Dependencies
- **transformers** (>=4.30.0): Hugging Face models
- **torch** (>=2.0.0): PyTorch backend
- **accelerate** (>=0.20.0): Optimized model loading
- **sentencepiece** (>=0.1.99): Tokenization
- **tokenizers** (>=0.13.0): Fast tokenization

### Development Dependencies
- **pytest** (>=7.0.0): Testing framework
- **pytest-cov** (>=4.0.0): Coverage reporting
- **black** (>=23.0.0): Code formatting
- **ruff** (>=0.1.0): Fast linting
- **mypy** (>=1.0.0): Type checking
- **pre-commit** (>=3.0.0): Git hooks
- **bandit**: Security scanning

## Milestones

### Milestone 1: Foundation (Week 1-2)
- ✅ Project structure setup
- ✅ CI/CD pipeline
- ✅ Testing framework
- ✅ Development environment

### Milestone 2: Core Modules (Week 3-4)
- [ ] Form Inspector implementation
- [ ] User Data Manager implementation
- [ ] Form Filler implementation
- [ ] Basic CLI interfaces

### Milestone 3: LLM Integration (Week 5-6)
- [ ] LLM Assistant implementation
- [ ] Model Manager implementation
- [ ] Natural language processing
- [ ] Integration with core modules

### Milestone 4: Polish & Release (Week 7-8)
- [ ] Comprehensive testing
- [ ] Documentation completion
- [ ] Bug fixes and optimization
- [ ] First stable release (v1.0.0)

## Open Questions & Decisions

1. **LLM Model Selection**: Which local model to recommend?
   - Options: Llama 2, Mistral, Phi-2
   - Criteria: Size, performance, license

2. **Field Matching Strategy**: Exact match vs fuzzy matching?
   - Start with exact match
   - Add fuzzy matching as enhancement

3. **User Data Storage**: JSON vs YAML default?
   - Support both
   - Default to JSON for simplicity

4. **Interactive Mode**: Terminal UI library?
   - Options: rich, prompt_toolkit
   - Decision: Start with simple input(), enhance later

## Notes

- Maintain backward compatibility with existing `generate_stub.py` and `fill_form.py`
- Consider migration path for existing users
- Keep LLM dependencies optional for basic functionality
- Prioritize Adobe compatibility (adobe_mode=True)
- Follow semantic versioning for releases
