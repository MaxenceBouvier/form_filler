 Claude Code Documentation

> **Document Structure**: This file contains both universal AI assistant guidelines (applicable to any repository) and project-specific information. Universal sections are marked with 🌍. Copy Part I to your project's CLAUDE.md file and customize Part II with your project details.

---

## ⚠️ OPTIONAL: Package Manager Configuration

> **Note**: This section is for Python projects using `uv`. If your project doesn't use `uv`, you can remove this section entirely or adapt it for your package manager (npm, yarn, poetry, etc.).

**MANDATORY RULE (if using uv)**: This project uses `uv` (not `pip`) for ALL Python package operations.

**ALWAYS use:**
- ✅ `uv pip install <package>`
- ✅ `uv pip freeze`
- ✅ `uv pip list`
- ✅ `uv venv .venv`

**NEVER use:**
- ❌ `pip install <package>`
- ❌ `pip freeze`
- ❌ `pip list`
- ❌ `python -m venv .venv`

**Why `uv`?**
- 10-100x faster than pip
- Better dependency resolution
- Project standard across all repos
- Consistent with CI/CD pipeline

**If you catch yourself about to use `pip`, STOP and use `uv pip` instead.**

---

## 🌍 Part I: Universal AI Assistant Guidelines
(Applicable to ANY repository)

### Core Principles

1. **Security First**: Never expose secrets, validate inputs, follow least privilege
2. **Correctness Over Speed**: Working code over fast code
3. **Best Practices**: Industry standards over personal preferences
4. **Ask When Uncertain**: Clarify ambiguities rather than guess
5. **Document Decisions**: Explain rationale for significant choices
6. **Use Project Tools**: Use the project's configured package manager and tools (see above if applicable)

### Error Handling and Safety

#### When Operations Fail

1. **Authentication Failures**
   - ⛔ DO NOT retry authentication multiple times
   - ✅ Inform user immediately with clear error message
   - ✅ Provide exact manual steps to resolve
   - ✅ Save work to draft files if operations blocked
   - ✅ Wait for explicit user confirmation before retrying

2. **File Operation Failures**
   - ✅ Check file/directory existence BEFORE operations
   - ✅ Validate permissions and paths
   - ✅ Provide alternative approaches when primary fails
   - ⛔ DO NOT continue with operations that depend on failed steps

3. **Test Failures**
   - ✅ Always run tests AFTER code changes
   - ✅ Report failures with exact error messages
   - ✅ Suggest fixes based on error analysis
   - ⛔ DO NOT commit code with failing tests

4. **Build/Compilation Failures**
   - ✅ Check build status before proceeding
   - ✅ Report dependency issues clearly
   - ✅ Suggest dependency installation commands

### Testing Standards

#### Test Creation Requirements

1. **When to Write Tests**
   - ✅ ALWAYS write tests for new functions/classes
   - ✅ ALWAYS write tests for bug fixes (regression prevention)
   - ✅ ALWAYS update tests when changing behavior
   - ⛔ DO NOT skip tests for "simple" code

2. **Test Organization**
   - ✅ Module-specific tests → `src/<module>/tests/` directory
   - ✅ End-to-end tests → top-level `tests/` directory
   - ✅ Mirror module structure: `src/module/foo.py` → `src/module/tests/test_foo.py`
   - ✅ Use descriptive test names: `test_<function>_<scenario>_<expected>`
   - ✅ Group related tests in classes

3. **Test Quality**
   - ✅ Test edge cases, not just happy paths
   - ✅ Use assertions with clear failure messages
   - ✅ Make tests deterministic (no random failures)
   - ✅ Keep tests fast (mock expensive operations)

#### TDD & Testing Trophy Policy

- **Practice TDD**: write a failing test first, implement, then refactor with tests green.
- **Testing Trophy mix**: prefer **static + integration tests** as the bulk; keep **unit tests** focused and **E2E** minimal for critical flows. This aligns with the Testing Trophy guidance popularized by Kent C. Dodds.
- **Reproducibility**: Make tests deterministic by seeding random number generators and persisting test fixtures under `src/<module>/tests/data/` (module tests) or `tests/data/` (E2E tests).

### Security and Secrets Management

#### Secrets Detection and Prevention

1. **Before Committing**
   - ✅ ALWAYS scan for secrets in changed files
   - ✅ Check for: API keys, passwords, tokens, private keys, connection strings
   - ⛔ NEVER commit files containing secrets
   - ✅ Use environment variables or secret management tools

2. **Secret Patterns to Watch**
   - API keys: `api_key=`, `apikey:`, `API_TOKEN`
   - Passwords: `password=`, `passwd:`, `PWD`
   - Private keys: `-----BEGIN PRIVATE` + ` KEY-----` (PEM format headers)
   - Connection strings: `mongodb://`, `postgres://username:password@`
   - Tokens: `token=`, `bearer`, `jwt`

3. **When Secrets Are Detected**
   - ⛔ DO NOT proceed with commit
   - ✅ Warn user immediately with specific file and line number
   - ✅ Suggest `.gitignore` entry or environment variable alternative
   - ✅ Recommend secret rotation if already exposed

### Performance Considerations

1. **Algorithm Complexity**
   - ✅ Consider time and space complexity for operations on large datasets
   - ✅ Prefer O(n log n) over O(n²) when working with >1000 items
   - ✅ Use appropriate data structures (set for membership, dict for lookups)

2. **I/O Operations**
   - ✅ Batch file operations when processing multiple files
   - ✅ Use generators for large datasets instead of loading into memory
   - ✅ Consider async I/O for network or disk-heavy operations

### 🌍 Git/Version Control Workflow (Universal)

#### Development Workflow for New Features

**MANDATORY: When asked to build something, ALWAYS follow this workflow:**

```
┌─────────────────────────────────────────────────────────────┐
│  REQUIRED WORKFLOW FOR ALL CODE CHANGES                     │
├─────────────────────────────────────────────────────────────┤
│  1. Check existing branches → git fetch origin              │
│  2. Create issue/ticket in issue tracker                    │
│  3. Create feature/fix branch from main                     │
│  4. Implement changes following project patterns            │
│  5. Run tests and linting                                   │
│  6. Commit with conventional format                         │
│  7. Push branch and create pull/merge request               │
│                                                              │
│  ⛔ DO NOT make changes directly on main/master             │
│  ⛔ DO NOT skip creating an issue first                     │
│  ✅ ALWAYS use feature branches                             │
└─────────────────────────────────────────────────────────────┘
```

#### Parallel Development with Git Worktrees

When running multiple Claude instances or working on multiple features:

```bash
# Create worktree for parallel development
git worktree add -b feature/issue-123 ../project-feature-123 main

# Each instance works in its own worktree
# Benefits:
# - ✅ No branch switching conflicts
# - ✅ Shared .git repository
# - ✅ Each instance works independently

# Cleanup after merge:
git worktree remove ../project-feature-123
git branch -d feature/issue-123
```

#### File Operations in Worktrees

**CRITICAL: When working in a worktree, ALL file operations MUST stay within that worktree**

This is the #1 rule to prevent accidentally modifying files in the wrong location.

```bash
# ✅ CORRECT: Check your current working directory
# The <env> section tells you: Working directory: /workspace/<project-name>-feature-12
# ALL file operations must use paths relative to THIS directory

# ✅ CORRECT: Use relative paths from current directory
Read("src/module/file.py")
Edit("src/another_module/config.py", ...)
Write("tests/test_new_feature.py", ...)

# ❌ WRONG: Using absolute paths to main repository
Read("/workspace/<project-name>/src/module/file.py")  # WRONG!
Edit("/workspace/<project-name>/src/another_module/config.py", ...) # WRONG!

# ❌ WRONG: cd'ing out of the worktree
cd ../<project-name>  # WRONG! Leaves the worktree
cd /workspace/<project-name>  # WRONG! Leaves the worktree
```

**Rule for AI Assistants:**
1. **ALWAYS** check `<env>` for the current working directory at the start of a session
2. **ALWAYS** use paths relative to the current working directory
3. **NEVER** use absolute paths that point to the main repository directory
4. **NEVER** use `cd` to navigate outside the current worktree
5. **IF** you need to reference the main repo, ask the user first

**How to verify you're in the right place:**
```bash
# Check current directory
pwd  # Should show: /workspace/<project-name>-feature-X

# Verify you're on the right branch
git branch --show-current  # Should show: feature/X-description

# If you're unsure, ask the user!
```

#### Environment Setup in Worktrees

> **Note**: This section applies to projects that use virtual environments (Python, Node.js, etc.). Adapt the commands for your project's package manager.

**When working in a git worktree** (e.g., `/workspace/<project-name>-refactor-8`):

**CRITICAL: Each worktree should have its own isolated environment**

```bash
# ✅ CORRECT: Always activate and use the local environment IN WORKTREES
# For Python:
source .venv/bin/activate
python -m pytest tests/

# For Node.js:
npm install  # Creates local node_modules
npm test

# ❌ WRONG: Using global environment in a worktree (causes conflicts with other worktrees)
```

**When working in the main repository** (`/workspace/<project-name>`):

You can use either a global or local environment based on your project preferences:

```bash
# Option 1: Global environment (if your team uses this approach)
# Option 2: Local environment (recommended for consistency)
```

**Setup for new worktree:**

**Automated Setup (Recommended):**
```bash
# If your project has a setup script (see workflow_scripts/ for templates):
cd ../<project-name>-feature-X
./scripts/setup_worktree.sh

# The script should handle:
# - Creating isolated environment (.venv, node_modules, etc.)
# - Installing dependencies
# - Copying/creating environment configuration files
# - Verifying the setup

# Then activate/use the environment as needed
```

**Manual Setup (Alternative - Python Example):**
```bash
# 1. Navigate to worktree
cd ../<project-name>-feature-X

# 2. Create and activate virtual environment
python -m venv .venv  # or: uv venv .venv
source .venv/bin/activate

# 3. Install dependencies
pip install -e .  # or: uv pip install -e .

# 4. Copy environment configuration if needed
cp .env.example .env  # then edit paths for worktree

# 5. Verify correct environment
which python  # Should show: ../<project-name>-feature-X/.venv/bin/python
```

**Manual Setup (Alternative - Node.js Example):**
```bash
# 1. Navigate to worktree
cd ../<project-name>-feature-X

# 2. Install dependencies
npm install  # or: yarn install / pnpm install

# 3. Copy environment configuration if needed
cp .env.example .env

# 4. Verify
npm list --depth=0
```

**Before running ANY commands in a worktree:**
- ✅ Always check you're using the local environment (not global/system)
- ✅ Always activate environment at start of session (if applicable)
- ⛔ Never use global/system packages in worktrees (causes conflicts)

#### Commit Message Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

Types: feat, fix, docs, style, refactor, test, chore
Example: `feat(auth): add OAuth2 support`

#### Branch Naming Conventions

- `feature/<issue-number>-<description>` - New features
- `fix/<issue-number>-<description>` - Bug fixes
- `docs/<issue-number>-<description>` - Documentation
- `refactor/<issue-number>-<description>` - Code improvements

### 🌍 Decision-Making Framework (Universal)

#### When to Make Autonomous Decisions

✅ **DECIDE WITHOUT ASKING** when:
- Following documented project conventions (linting, formatting, structure)
- Applying industry best practices (error handling, logging, security)
- Implementing well-defined requirements with clear acceptance criteria
- Fixing obvious bugs with clear correct behavior
- Following explicit patterns from existing codebase

Examples:
- "This function needs error handling → add try/except with logging" ✅
- "Code fails linting → apply autoformat" ✅
- "Missing docstring → add following project template" ✅

#### When to Ask Questions

❓ **ASK THE USER** when:
- Multiple valid approaches exist with different trade-offs
- Requirements are ambiguous or incomplete
- Decision impacts public API or user-facing behavior
- Breaking changes are necessary
- Security or performance implications are significant
- Deviating from established patterns is beneficial

Examples:
- "This could be sync or async. Async is better for I/O but adds complexity. Your preference?" ❓
- "Requirements don't specify error handling for edge case X. Should we: A) fail fast, B) retry, C) fallback?" ❓
- "This refactor would break the API. Should we: A) deprecate old API, B) keep both, C) breaking change?" ❓

#### Priority Hierarchy (When Principles Conflict)

```
1. SECURITY (highest priority)
   ├─ Never expose secrets
   ├─ Validate all inputs
   └─ Security > convenience

2. CORRECTNESS
   ├─ Code must work correctly
   ├─ Edge cases handled
   └─ Correctness > performance

3. BEST PRACTICES
   ├─ Industry standards
   ├─ Established patterns
   └─ Best practices > personal style

4. PROJECT CONVENTIONS
   ├─ Existing codebase patterns
   ├─ Team agreements
   └─ Consistency > personal preference

5. USER PREFERENCES
   ├─ Explicit user requests
   ├─ Project-specific choices
   └─ Preferences > arbitrary choices

6. PERFORMANCE (lowest priority)
   ├─ Optimize hot paths only
   ├─ Profile before optimizing
   └─ Clear code > fast code
```

#### Communication Standards

1. **Be Clear and Concise**
   - ✅ Explain WHAT you're doing
   - ✅ Explain WHY you're doing it
   - ✅ Use absolute file paths in responses
   - ⛔ Avoid overly technical jargon

2. **Error Reporting Template**
   ```
   ❌ **Operation Failed:** [Brief description]

   **Error:** [Exact error message]
   **Cause:** [Analysis]
   **Resolution:** [Steps to fix]
   ```

3. **Asking for Clarification Template**
   ```
   I need clarification on [topic]:

   **Options:**
   1. [Option A]: [Trade-offs]
   2. [Option B]: [Trade-offs]

   **Recommendation:** [Your suggestion and why]
   ```

### 🌍 Code Quality Checklist (Universal)

Before finalizing ANY code changes:

#### Functionality
- [ ] Code implements requirements correctly
- [ ] Edge cases handled
- [ ] Error conditions tested

#### Code Quality
- [ ] Functions are small and single-purpose
- [ ] Clear, descriptive naming
- [ ] No code duplication (DRY)
- [ ] Complex logic documented

#### Testing
- [ ] Unit tests written for new code
- [ ] Tests cover edge cases
- [ ] All tests pass

#### Security
- [ ] No secrets in code
- [ ] Inputs validated
- [ ] Injection attacks prevented

#### Performance
- [ ] No obvious performance issues
- [ ] Appropriate data structures used

### 🌍 Troubleshooting Common Issues (Universal)

#### Authentication Failed (401 Unauthorized)
**Symptoms:** CLI commands fail with `401` error

**Solution:**
1. ⛔ DO NOT retry multiple times
2. ✅ Inform user: "Authentication has expired. Please run these commands: [provide exact commands]"
3. ✅ Save work to draft files
4. ⏸️ Wait for user confirmation before retrying

#### Test Failures After Changes
**Symptoms:** Tests fail after code modifications

**Solution:**
1. ✅ Report exact error message to user
2. ✅ Analyze error and suggest fix
3. ✅ Apply fix and re-run tests
4. ⛔ DO NOT proceed to commit if tests fail

#### File Not Found When Reading
**Symptoms:** Read tool reports file doesn't exist

**Solution:**
1. ✅ Verify path is absolute (not relative)
2. ✅ Check if file was moved/renamed
3. ✅ List directory contents to verify
4. ❓ Ask user if file should exist or be created

#### Unclear Requirements
**Symptoms:** User request is ambiguous

**Solution:**
1. ✅ Identify specific ambiguities
2. ✅ Present options with trade-offs
3. ❓ Ask clarifying questions
4. ⛔ DO NOT guess and proceed

### 🌍 Common Patterns Library (Universal)

#### Adding a New Feature
```
1. Read existing similar features
2. Create feature branch
3. Implement following existing patterns
4. Write tests
5. Update documentation
6. Submit for review
```

#### Fixing a Bug
```
1. Reproduce the bug
2. Write failing test demonstrating bug
3. Fix the bug
4. Verify test now passes
5. Check for similar bugs
6. Document fix in commit message
```

#### Refactoring Code
```
Safe refactoring steps:
1. Ensure tests exist and pass
2. Make small, incremental changes
3. Run tests after EACH change
4. Keep behavior identical
5. Document rationale
```

## Part II: form_filler Project Information

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

- Python >= 3.13 (REQUIRED)
- PyPDFForm >= 1.4.0 (required) - provides high-level interface for inspecting and filling PDF AcroForms
- PyYAML >= 6.0 (required) - enables YAML input/output support
- Hugging Face stack (optional, for LLM features):
  - transformers >= 4.30.0
  - torch >= 2.0.0
  - accelerate >= 0.20.0
  - sentencepiece >= 0.1.99
  - tokenizers >= 0.13.0

Dependencies are managed via `pyproject.toml` and installed automatically with the package.

### Adding New Dependencies

**IMPORTANT: Always add dependencies to the appropriate requirements file**

When you need to add a new package:

1. **Production Dependencies** (needed for the application to run):
   - Add to `requirements.txt`
   - Example: `PyPDFForm>=1.4.0`
   - Install with: `uv pip install -e .`

2. **Development Dependencies** (testing, linting, type checking):
   - Add to `pyproject.toml` under `[project.optional-dependencies].dev`
   - Example: `types-PyYAML>=6.0.0` for type stubs
   - Install with: `uv pip install -e ".[dev]"`

3. **Type Stubs** (always development dependencies):
   - Add all `types-*` packages to dev dependencies
   - Examples: `types-PyYAML`, `types-requests`
   - These are only needed for mypy type checking

**Never just install packages without adding them to requirements!**
- ❌ BAD: `uv pip install some-package` (package not tracked)
- ✅ GOOD: Add to requirements file, then run `uv pip install -e .` or `uv pip install -e ".[dev]"`

## Directory Structure

The project follows a structured organization for data management and security:

```
form_filler/
├── src/form_filler/      # Main package code
├── tests/                # Test suite
├── resources/            # Data directory (mixed commit status)
│   ├── user_info/        # User database - NEVER COMMITTED
│   ├── output/           # Generated PDFs - NOT COMMITTED
│   └── examples/         # Example configs - COMMITTED
├── form_to_fill/         # Source PDF forms
└── ...
```

### Critical: `resources/user_info/`

**Purpose:** User data database containing sensitive personal information

**Storage:**
- Multiple user profiles can be stored as separate files
- Each profile is a JSON or YAML file (e.g., `john_doe.json`, `jane_smith.yaml`)
- Contains structured data matching PDF form field names
- Can be used to extract data from already-filled forms for database population

**Security:**
- **NEVER committed to git** - protected by `.gitignore` and CI/CD validation
- Contains sensitive personal/financial information
- Privacy-first: all data stays local

**Usage by CLI tools:**
- `update-user-info` reads/writes these files
- `fill-in-pdf` reads user data from here
- Can reference by filename: `--user resources/user_info/profile1.json`

### `resources/output/`

**Purpose:** Storage for auto-filled PDF forms

**Behavior:**
- Default output location for `fill-in-pdf` command
- Files named: `{original_name}_autofilled.pdf`
- Not committed to git to avoid repository bloat
- Can be safely deleted/cleaned up without affecting functionality

### `resources/examples/`

**Purpose:** Sample/template data for documentation and testing

**Contents:**
- Example user data structures with anonymized/fake data
- Template configurations
- Safe to commit - contains no real user information
- Useful for users to understand expected data format

### `form_to_fill/`

**Purpose:** Source PDF forms (blank or filled)

**Dual Purpose:**
1. **Input forms:** Place blank PDFs here to be filled
2. **Reference forms:** Place already-filled PDFs here to extract user data

**Git Behavior:**
- PDFs are NOT committed (ignored via `.gitignore`)
- READMEs ARE committed (exception in `.gitignore`)
- Keeps repository clean while allowing documentation

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
