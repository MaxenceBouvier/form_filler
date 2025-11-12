# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Python-based utility for semi-automatically filling PDF forms, specifically designed for the 2025 Swiss Tax Questionnaire (Departure). The project provides command-line tools to extract form fields, manage user information, and populate PDFs with user data.

## Installation

This project is designed to be installed via `uv` and includes a `pyproject.toml` that enables quick and easy installation as a package:

```bash
uv pip install -e .
```

Once installed, the utilities are available as command-line entry points.

## Dependencies

- Python 3.8+
- PyPDFForm (required) - provides high-level interface for inspecting and filling PDF AcroForms
- PyYAML (optional) - enables YAML input/output support; JSON is used if unavailable

Dependencies are managed via `pyproject.toml` and installed automatically with the package.

## Architecture

### Current State

The codebase currently has two foundational scripts:
- `generate_stub.py`: Introspects PDF AcroForm schema via PyPDFForm's `wrapper.schema`, generating a dict mapping field names to default values (booleans → `False`, others → empty string)
- `fill_form.py`: Reads JSON/YAML data, instantiates `PdfWrapper` with `adobe_mode=True`, fills fields, and writes output with optional flattening

### Target Architecture

The project is being refactored into three CLI entry points:

#### 1. `extract-required-info`
Analyzes a PDF form and extracts metadata about required fields.

**Usage:**
```bash
extract-required-info form.pdf
```

**Output:** List/report of field names, types, and possibly categories (personal info, address, financial, etc.)

**Purpose:** Understanding what information a form needs before filling

#### 2. `update-user-info`
Manages a persistent user information store (JSON/YAML file containing reusable personal data).

**Usage:**
```bash
update-user-info --only-new    # default: adds only fields not in user info file
update-user-info --review      # interactive mode to review/update existing values
```

**Input:** Form schema/requirements + existing user info file

**Output:** Updated user info file

**Purpose:** Maintaining a single source of truth for user data across multiple forms

#### 3. `fill-in-pdf`
Populates PDF form fields with user data.

**Usage:**
```bash
fill-in-pdf --input form.pdf --user my_info.json
```

**Flags:**
- `--input` (required): Path to source PDF form
- `--user` (required): Path to user info file

**Output:** Automatically named as `{original_pdf_name}_autofilled.pdf`

**Purpose:** Final step - generating the completed form

### Workflow

```
1. extract-required-info form.pdf
   → Shows what fields the form needs

2. update-user-info --only-new
   → Adds missing fields to user's persistent data store
   (or use --review to interactively update existing values)

3. fill-in-pdf --input form.pdf --user my_info.json
   → Generates form_autofilled.pdf
```

### Data Flow

```
PDF Form → extract-required-info → Required Fields List
                                         ↓
User Info File ← update-user-info ← Required Fields
                                         ↓
User Info File → fill-in-pdf ← PDF Form → Filled PDF
```

### Core Components

The architecture requires these modules:

1. **Form Inspector**: Extracts schema from PDF (builds on `generate_stub.py`)
2. **User Data Manager**: CRUD operations on persistent user info file
3. **Field Matcher**: Maps user data fields to form fields (may need fuzzy matching)
4. **Form Filler**: Populates PDF (builds on `fill_form.py`)

## Key Implementation Details

- **Field Type Detection**: In `build_stub()` (generate_stub.py:33), field types are extracted from the schema. If a field has multiple types (list), the first is selected. Boolean fields get `False`, all others get empty string.

- **Adobe Compatibility**: Use `adobe_mode=True` when instantiating `PdfWrapper` (fill_form.py:84) to ensure proper appearance regeneration in Adobe readers.

- **Format Detection**: Auto-detect JSON vs YAML from file extension (.yaml/.yml vs .json) rather than requiring explicit format flags.

- **Error Handling**: Validate file existence before processing and provide clear error messages for missing dependencies.

- **Output Naming Convention**: Filled PDFs are automatically named as `{original_name}_autofilled.pdf` to prevent accidental overwrites.

## LLM Integration

The project supports LLM-assisted form filling:
1. Extract required fields from PDF
2. Update user info (manually or via LLM assistance)
3. LLM can help map user's natural language information to structured fields
4. User reviews generated data
5. Fill form with verified data

Field names in the user data must match form field names for successful filling (field matcher may provide fuzzy matching in the future).
