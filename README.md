# Form Filler

A Python-based utility for semi-automatically filling PDF forms with LLM assistance.

[![CI](https://github.com/mbouvier/form_filler/actions/workflows/ci.yml/badge.svg)](https://github.com/mbouvier/form_filler/actions/workflows/ci.yml)
[![Python 3.13+](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/downloads/)
[![Code style: ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Features

- Extract required field information from PDF AcroForms
- Manage persistent user information across multiple forms
- LLM-assisted form filling with local Hugging Face models
- Automatic field mapping and validation
- Adobe-compatible PDF output
- Cross-platform support (Linux, macOS, Windows)

## Quick Start

### 1. Extract Required Information

First, analyze the PDF form to see what fields are required:

```bash
extract-required-info "<pdf>>.pdf"
```

This displays all form fields, their types, and categories (personal info, address, financial, etc.).

### 2. Update User Information

Create or update your persistent user information file:

```bash
# Add only new fields not already in your user info
update-user-info --only-new

# Or interactively review and update existing values
update-user-info --review
```

This creates/updates a file in `resources/user_info/` containing your reusable personal data.

### 3. Fill the PDF Form

Generate the completed form:

```bash
fill-in-pdf --input "<pdf>.pdf" --user resources/user_info/my_profile.json
```

Output is automatically saved to `resources/output/` with the naming convention: `{original_name}_autofilled.pdf`.

## Workflow

```
┌─────────────────────────────────────────────────┐
│  PDF Form                                       │
└─────────────────┬───────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────┐
│  extract-required-info                          │
│  → Shows required fields and categories         │
└─────────────────┬───────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────┐
│  update-user-info                               │
│  → Updates persistent user data store           │
└─────────────────┬───────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────┐
│  [Optional] LLM assistance                      │
│  → Natural language to structured data          │
└─────────────────┬───────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────┐
│  fill-in-pdf                                    │
│  → Generates completed PDF                      │
└─────────────────────────────────────────────────┘
```

## LLM Integration

Form Filler supports local LLM assistance via Hugging Face transformers:

1. **Extract fields** from the PDF form
2. **Provide information** in natural language
3. **LLM maps** your input to structured field data
4. **Review** the generated data
5. **Fill form** with verified information

The tool uses local models to ensure privacy - your sensitive information never leaves your machine.

## Command Reference

### `extract-required-info`

Extract and display form field requirements.

```bash
extract-required-info <pdf_file> [--output <output_file>]
```

**Arguments:**
- `<pdf_file>`: Path to the PDF form
- `--output`: Optional JSON/YAML output file

### `update-user-info`

Manage your persistent user information.

```bash
update-user-info [--only-new] [--review] [--file <user_info_file>]
```

**Flags:**
- `--only-new`: Add only fields not already in user info (default)
- `--review`: Interactive mode to review/update all values
- `--file`: Specify custom user info file path (default: stored in `resources/user_info/`)

### `fill-in-pdf`

Fill a PDF form with user data.

```bash
fill-in-pdf --input <pdf_file> --user <user_info_file> [--output <output_file>]
```

**Arguments:**
- `--input`: Path to source PDF form (required)
- `--user`: Path to user info file (required)
- `--output`: Custom output name (optional, defaults to `resources/output/{input}_autofilled.pdf`)

## How It Works

Form Filler is built on:

- **[PyPDFForm](https://github.com/chinapandaman/PyPDFForm)**: High-level PDF AcroForm manipulation
- **[Transformers](https://huggingface.co/transformers)**: Local LLM inference via Hugging Face
- **[PyTorch](https://pytorch.org/)**: Machine learning backend

The tool extracts PDF schema using `PyPDFForm.wrapper.schema`, maintains user data in JSON/YAML format, and fills forms with `adobe_mode=True` for proper compatibility.

## Project Structure

The project uses a `resources/` directory to organize different types of data:

```
resources/
├── user_info/          # User database (NEVER committed)
│   ├── profile1.json   # Individual user profiles
│   ├── profile2.yaml   # Supports both JSON and YAML
│   └── ...
├── output/             # Generated PDFs (not committed)
│   └── *_autofilled.pdf
└── examples/           # Example configurations (committed)
    └── sample_data.json

form_to_fill/           # Source PDF forms
├── blank_form.pdf      # Forms to be filled (not committed)
└── README.md           # Documentation (committed)
```

### Resources Folder Details

#### `resources/user_info/`
**Purpose:** Your personal data database

- Stores all user information profiles (personal details, addresses, financial info, etc.)
- Can contain multiple profiles for different users or scenarios
- Supports both JSON and YAML formats
- **SECURITY:** This directory is excluded from git and protected by CI/CD validation
- **Privacy:** Your sensitive information never leaves your machine

#### `resources/output/`
**Purpose:** Storage for generated PDF forms

- All auto-filled PDFs are saved here by default
- Files follow the naming convention: `{original_name}_autofilled.pdf`
- Not tracked by git to avoid bloating the repository

#### `resources/examples/`
**Purpose:** Sample configurations and templates

- Contains example user data structures (with fake/anonymized data)
- Useful for understanding the expected data format
- Safe to commit as they contain no real user information

#### `form_to_fill/`
**Purpose:** Source forms to be filled

- Place your blank PDF forms here
- PDFs are not committed to git (except READMEs)
- Can also contain filled forms to extract data from

## Installation

### Prerequisites
- Python >= 3.13
- [uv](https://github.com/astral-sh/uv) (recommended) or pip

### Quick Install

```bash
# Create virtual environment with uv (recommended)
uv venv .venv --python 3.13
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install the package
uv pip install -e .

# Or using standard pip
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

### Development Install

```bash
# Create virtual environment with uv
uv venv .venv --python 3.13
source .venv/bin/activate

# Install with development dependencies
uv pip install -e ".[dev]"

# Set up pre-commit hooks
pre-commit install
```

## Development

### Project Code Structure

```
form_filler/
├── src/form_filler/     # Main package
│   ├── cli.py           # CLI entry points
│   ├── core/            # Core functionality
│   └── llm/             # LLM integration
├── tests/               # Test suite
├── .github/workflows/   # CI/CD
├── pyproject.toml       # Project configuration
└── requirements.txt     # Dependencies
```

### Running Tests

```bash
# Run all tests with coverage
pytest

# Run specific test file
pytest tests/test_form_inspector.py

# Run with verbose output
pytest -v
```

### Code Quality

```bash
# Format code
ruff format .

# Lint code
ruff check .

# Type check
mypy src/
```

Pre-commit hooks will automatically run these checks before each commit.

## Dependencies

### Core
- PyPDFForm >= 1.4.0
- PyYAML >= 6.0

### LLM (Optional)
- transformers >= 4.30.0
- torch >= 2.0.0
- accelerate >= 0.20.0
- sentencepiece >= 0.1.99
- tokenizers >= 0.13.0

### Development
- pytest >= 7.0.0
- pytest-cov >= 4.0.0
- ruff >= 0.1.0
- mypy >= 1.0.0
- pre-commit >= 3.0.0

## Legacy Scripts

The original utility scripts are still available:

- `generate_stub.py`: Inspect PDF and emit stub JSON/YAML
- `fill_form.py`: Fill PDF from JSON/YAML data

These will be deprecated in favor of the new CLI tools.

## Disclaimer

This project is provided for educational purposes. It's your responsibility to ensure all answers are correct and complete before submitting any official documents. Always review LLM-generated data for accuracy.

## License

MIT License - see LICENSE file for details.

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass and code quality checks succeed
5. Submit a pull request

See [DEV_PLAN.md](.claude/docs/DEV_PLAN.md) for the development roadmap.
