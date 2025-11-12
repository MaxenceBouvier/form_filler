# Git/GitHub Workflow for AI Assistants

This document provides comprehensive Git and GitHub workflow instructions for AI assistants working on the form_filler project.

## Table of Contents
- [Repository Structure](#repository-structure)
- [Branch Strategy](#branch-strategy)
- [Development Workflow](#development-workflow)
- [Commit Guidelines](#commit-guidelines)
- [Issue Management](#issue-management)
- [Pull Request Process](#pull-request-process)
- [CI/CD Considerations](#cicd-considerations)
- [Troubleshooting](#troubleshooting)

## Repository Structure

### Repository Configuration
```
origin → github.com:<username>/form_filler.git
```

### Development
- All development happens on GitHub (`origin`)
- Main branch: `main`

### Remote Commands
```bash
# Fetch from GitHub
git fetch origin

# Push to GitHub
git push origin branch-name
```

## Parallel Development with Git Worktrees

### When to Use Git Worktrees

Git worktrees are ideal for:
- Running multiple Claude Code instances simultaneously on different features
- Working on multiple branches without switching in your main working directory
- Keeping long-running development separate from quick fixes
- Testing changes across different branches concurrently

### Setting Up a Worktree

**Basic Usage:**
```bash
# Create a new worktree for an existing branch
git worktree add ../form_filler-feature feature/my-feature

# Create a new worktree with a new branch
git worktree add -b feature/new-feature ../form_filler-new-feature main

# List all worktrees
git worktree list
```

**Recommended Naming Pattern:**
```bash
# For features
git worktree add ../form_filler-feature-<number> feature/<number>-<description>

# For bug fixes
git worktree add ../form_filler-fix-<number> fix/<number>-<description>

# Examples
git worktree add ../form_filler-feature-5 feature/5-pdf-field-mapping
git worktree add ../form_filler-fix-42 fix/42-yaml-parsing-bug
```

### Working with Worktrees

**Starting Work in a Worktree:**

**Method 1: Automated Setup (Recommended)**
```bash
# 1. Create worktree from main directory
cd /home/mbouvier/proj/form_filler
git worktree add ../form_filler-feature-5 feature/5-pdf-field-mapping

# 2. Navigate to the worktree
cd ../form_filler-feature-5

# 3. Run the automated setup script (if available)
# Note: If scripts/setup_worktree.sh doesn't exist, use Method 2 below
./scripts/setup_worktree.sh

# This script (if present) automatically:
# - Creates .venv with uv
# - Installs all dependencies in sync with main repo
# - Creates any necessary directories
# - Verifies the complete setup

# 4. Activate the environment
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# 5. Verify installation
which python  # Should show: ../form_filler-feature-5/.venv/bin/python
python -c "import form_filler; print('OK')"

# 6. Start Claude Code in the new directory
claude
```

**Method 2: Manual Setup (Alternative)**
```bash
# 1. Create worktree from main directory
cd /home/mbouvier/proj/form_filler
git worktree add ../form_filler-feature-5 feature/5-pdf-field-mapping

# 2. Navigate to the worktree
cd ../form_filler-feature-5

# 3. Set up isolated Python environment for this worktree
uv venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# 4. Install in editable mode with development dependencies
uv pip install -e ".[dev]"

# Alternative: Install core package only
# uv pip install -e .

# 5. Create necessary directories
mkdir -p resources/user_info resources/output resources/examples

# 6. Verify installation
which python  # Should show: ../form_filler-feature-5/.venv/bin/python
python -c "import form_filler; print('OK')"

# 7. Start Claude Code in the new directory
claude
```

**⚠️ CRITICAL: File Operations Must Stay Within the Worktree**

When Claude is running in a worktree, ALL file operations must stay within that worktree:

```bash
# ✅ CORRECT: Check where you are (from <env> in your context)
# Working directory: /home/mbouvier/proj/form_filler-feature-5
# ALL Read, Edit, Write operations use paths relative to THIS directory

# ✅ CORRECT: Use relative paths
Read("src/form_filler/application/extract_fields.py")  # Reads from feature-5 worktree
Edit("src/form_filler/cli.py", ...) # Edits in feature-5 worktree

# ❌ WRONG: Using absolute paths to main repo
Read("/home/mbouvier/proj/form_filler/src/form_filler/application/extract_fields.py")  # WRONG!
Edit("/home/mbouvier/proj/form_filler/src/form_filler/cli.py", ...) # WRONG!

# ❌ WRONG: cd'ing outside the worktree
cd ../form_filler  # WRONG! Modifies wrong files
cd /home/mbouvier/proj/form_filler  # WRONG! Leaves the worktree
```

**Why this matters:**
- Without this rule, Claude may accidentally edit files in the main repo instead of the worktree
- Changes would appear to "not work" because they're being made in the wrong location
- Tests would pass/fail on the wrong code
- Commits would be made to the wrong branch

**Rule for AI Assistants:**
1. **ALWAYS** check `<env>` working directory at session start
2. **ALWAYS** use relative paths from the current directory
3. **NEVER** use absolute paths to `/home/mbouvier/proj/form_filler`
4. **NEVER** cd outside the current worktree
5. **VERIFY** you're in the right place: `pwd` and `git branch --show-current`

**⚠️ CRITICAL: Python Environment Isolation**

Each worktree MUST have its own Python virtual environment. This is essential because:

- **Problem**: If you use the global Python environment, running `uv pip install -e .` in one worktree will overwrite the installation from another worktree
- **Impact**: Tests in worktree A will run against code from worktree B (whichever was installed last), leading to false test results
- **Solution**: Create a dedicated `.venv` directory in each worktree and activate it before running tests
- **Development mode**: Always install with `uv pip install -e ".[dev]"` to include testing tools (pytest, pytest-html, mypy, ruff, etc.)

**Example Issue**:
```bash
# Main repo (may use global Python environment)
cd /home/mbouvier/proj/form_filler
uv pip install -e .  # Installs from main repo to current environment

# Feature branch worktree (WRONG - no isolated env)
cd /home/mbouvier/proj/form_filler-feature-5
pytest tests/  # ❌ Tests run against main repo code, not feature branch!

# Feature branch worktree (CORRECT - isolated env with dev dependencies)
cd /home/mbouvier/proj/form_filler-feature-5
uv venv .venv
source .venv/bin/activate
uv pip install -e ".[dev]"  # Installs from feature branch with dev tools
pytest tests/  # ✅ Tests run against feature branch code!
pytest --html=reports/test_report.html --self-contained-html  # ✅ HTML reports work!
```

**Why Install with `[dev]`?**

When working in a worktree, you need development dependencies:
- **Testing**: `pytest`, `pytest-cov`, `pytest-xdist`, `pytest-html` for running and reporting tests
- **Code quality**: `ruff` for linting, `mypy` for type checking
- **Documentation**: `sphinx` for generating docs
- **Pre-commit**: `pre-commit` hooks for automated quality checks

Without `[dev]`, commands like `pytest --html=...` or `ruff check` will fail.

**Inside Claude Code:**
- Each worktree has its own checked-out branch
- Changes in one worktree don't affect others
- All worktrees share the same .git repository (commits visible everywhere)
- You can push/pull from any worktree

### Cleaning Up Worktrees

**After Merging Your PR:**
```bash
# 1. Return to main directory
cd /home/mbouvier/proj/form_filler

# 2. Deactivate virtual environment if active
deactivate  # Only if you're in the worktree's venv

# 3. Remove the worktree (includes .venv directory)
git worktree remove ../form_filler-feature-5

# 4. Delete the merged branch (optional)
git branch -d feature/5-pdf-field-mapping

# Or use prune to clean up deleted worktrees
git worktree prune
```

**Force Removal (if needed):**
```bash
# If worktree has uncommitted changes
git worktree remove --force ../form_filler-feature-5
```

**Note on .venv Directories:**
- The `.venv` directory in each worktree is automatically ignored by git (see `.gitignore`)
- It will be deleted when you remove the worktree directory
- No need to manually clean up Python environments

### Worktrees vs Repository Clones

| Feature | Git Worktrees | Full Clones |
|---------|---------------|-------------|
| Disk space | Efficient (shared .git) | Duplicate .git history |
| Setup time | Fast | Slower (full clone) |
| Commit visibility | Immediate across all worktrees | Need to push/pull |
| Use case | Parallel short-term work | Long-term separate work |
| Cleanup | Simple removal | Delete entire directory |

**Recommendation**: Use worktrees for parallel Claude instances working on different features.

### For AI Assistants: Creating Worktrees

**Manual worktree creation:**

1. **Create the worktree:**
```bash
git worktree add ../form_filler-<name> <branch-name>
```

2. **Inform the user:**
```
✅ Created worktree at: ../form_filler-<name>
📍 Branch: <branch-name>

To start working in this worktree:
1. Open a new terminal
2. cd ../form_filler-<name>
3. Set up isolated Python environment with dev dependencies:
   uv venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   uv pip install -e ".[dev]"
4. Verify installation:
   which python  # Should show the worktree's .venv path
   pytest --version  # Should work (from dev dependencies)
5. claude

⚠️  CRITICAL: Each worktree needs its own Python environment with dev dependencies:
- Ensures tests run against the correct code (not other worktrees)
- Includes testing tools (pytest, pytest-html, ruff, mypy)
- Install with ".[dev]" not just "." to get all development tools
```

3. **Important limitations:**
   - Claude cannot `cd` to the new worktree and continue in the same session
   - The user must start a new Claude instance in the worktree directory
   - Each worktree must have its own Python virtual environment
   - This workflow prevents conflicts and ensures test isolation

## Branch Strategy

### Naming Conventions

| Type | Pattern | Example | Use Case |
|------|---------|---------|----------|
| Feature | `feature/<description>` | `feature/add-voltage-reference` | New functionality |
| Bug Fix | `fix/<issue-number>-<description>` | `fix/42-netlist-export-error` | Bug fixes |
| Documentation | `docs/<description>` | `docs/update-api-reference` | Documentation only |
| Refactor | `refactor/<description>` | `refactor/optimize-graph-ops` | Code improvements |
| Test | `test/<description>` | `test/add-param-registry-tests` | Test additions |
| Experimental | `exp/<description>` | `exp/ml-topology-search` | Experimental features |

### Branch Lifecycle
1. Create from latest `main`
2. Develop feature/fix
3. Create pull request
4. Review and merge
5. Delete branch after merge

## Development Workflow

### Recommended Workflow (Using Slash Commands)

**This is the preferred workflow for AI assistants:**

1. **Check existing branches**:
```bash
git fetch origin
git branch -r | grep -i feature-keywords
```

2. **Create GitHub issue**:
```bash
# Note: GitHub-specific slash commands (/gh_write-issue, etc.) are not yet implemented
# Use manual workflow below or request these commands be created
```

3. **Implement fix/feature and create PR**:
```bash
# Manual workflow required - see below
```

4. **Optional automated review**:
```bash
# Use code-reviewer agent or manual review process
```

### Manual Workflow (Primary Method)

Use this workflow for all development:

**Starting New Work:**

1. **Check for existing issues**:
```bash
gh issue list --search "keywords"
```

2. **Create issue if needed**:
```bash
gh issue create --title "Description" --label enhancement
```

3. **Create branch**:
```bash
git checkout -b feature/issue-number-description
```

**During Development:**

1. **Regular commits**:
```bash
git add -p  # Interactive staging
git commit -m "feat(cli): add field categorization logic"
```

2. **Keep branch updated**:
```bash
git fetch origin
git rebase origin/main
```

3. **Run tests before pushing**:
```bash
pytest tests/
ruff check src/
```

**Completing Work:**

1. **Push branch**:
```bash
git push origin feature/your-branch
```

2. **Create pull request**:
```bash
gh pr create --base main \
  --title "Feature: Description" \
  --body "Closes #issue-number"
```

## Commit Guidelines

### Commit Message Format
```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation only
- `style`: Code style changes
- `refactor`: Code refactoring
- `test`: Test additions/changes
- `chore`: Maintenance tasks
- `perf`: Performance improvements

### Scopes (Project-Specific)
- `cli`: Command-line interface
- `application`: Application layer use cases
- `domain`: Domain models and business logic
- `infrastructure`: External integrations (PDF, persistence)
- `pdf`: PDF form operations
- `persistence`: Data storage (JSON/YAML)
- `presentation`: User interface layer
- `tests`: Test infrastructure
- `<module>`: Any other module name

### Examples
```bash
# Feature
git commit -m "feat(application): add field categorization logic

Implements automatic categorization of PDF form fields into
personal info, address, and financial categories.

Closes #45"

# Fix
git commit -m "fix(pdf): correct checkbox field handling

Fixes incorrect boolean value mapping for checkbox fields.
Now properly handles True/False conversion to PDF format.

Fixes #67"

# Refactor
git commit -m "refactor(persistence): simplify YAML repository

Reduces complexity of YAML parsing by consolidating
redundant error handling logic."
```

## Issue Management

### Creating Issues

Use GitHub CLI manually:

```bash
gh issue create --title "Bug: Incorrect field mapping for checkbox fields" \
  --label "bug,pdf" \
  --body "## Problem\nDescription...\n\n## Steps to Reproduce\n..."
```

### Issue Labels
- **Type Labels**:
  - `enhancement`: New features
  - `bug`: Defects
  - `documentation`: Doc updates
  - `refactoring`: Code improvements
  - `optimization`: Performance

- **Module Labels**:
  - `cli`: Command-line interface issues
  - `application`: Application layer issues
  - `domain`: Domain logic issues
  - `pdf`: PDF form handling
  - `persistence`: Data storage issues
  - `testing`: Test-related
  - `<module-name>`: Any other module-specific issues

- **Priority Labels**:
  - `critical`: Blocking issues
  - `high`: Important issues
  - `medium`: Normal priority
  - `low`: Nice to have

### Issue Templates

#### Bug Report
```markdown
## Problem Description
Clear description of the bug

## Steps to Reproduce
1. Step one
2. Step two
3. ...

## Expected Behavior
What should happen

## Actual Behavior
What actually happens

## Environment
- Python version:
- PyPDFForm version:
- OS:

## Additional Context
Logs, screenshots, etc.
```

#### Feature Request
```markdown
## Feature Description
Clear description of the feature

## Use Case
Why this feature is needed

## Proposed Solution
How it could be implemented

## Alternatives Considered
Other approaches considered

## Impact
- Affected modules:
- Backward compatibility:
- Performance implications:
```

## Pull Request Process

### Creating PRs

**Manually (standard method)**:
```bash
gh pr create --base main \
  --title "Fix #42: Correct field mapping for checkbox fields" \
  --body "## Summary\n...\n\n## Changes\n...\n\n## Test Plan\n..." \
  --assignee @me
```

### PR Description Template
```markdown
## Summary
Brief description of changes

## Related Issue
Closes #issue-number

## Changes Made
- Change 1
- Change 2
- ...

## Test Plan
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Manual testing completed
- [ ] Documentation updated

## Screenshots (if applicable)
Before/After comparisons

## Performance Impact
Any performance implications

## Breaking Changes
List any breaking changes
```

### Review Process

1. **Self-review checklist**:
   - [ ] Code follows project patterns
   - [ ] Tests added/updated
   - [ ] Documentation updated
   - [ ] No security issues
   - [ ] Backward compatible

2. **Request review**:
```bash
gh pr edit --add-reviewer username
```

3. **Address feedback**:
   - Respond to comments
   - Push fixes as new commits
   - Request re-review when ready

## CI/CD Considerations

### Pre-Push Checks
```bash
# Run tests
pytest tests/

# Check code style
ruff check src/
ruff format src/ --check

# Check types (if using mypy)
mypy src/

# Run CLI commands to verify functionality
extract-required-info --help
update-user-info --help
fill-in-pdf --help
```

### Pipeline Stages (Future)
1. **Build**: Install dependencies
2. **Lint**: Code quality checks
3. **Test**: Unit and integration tests
4. **Security**: Vulnerability scanning
5. **Deploy**: Update documentation

## Troubleshooting

### Common Issues

#### Authentication Failed

**For AI Assistants**: When gh commands fail with authentication errors:
1. DO NOT attempt multiple authentication retries
2. Inform the user that authentication is required
3. Ask the user to run the authentication command manually
4. Wait for user confirmation before retrying gh commands

**User Authentication Steps**:
```bash
# 1. Authenticate with GitHub CLI
gh auth login

# Follow the interactive prompts to authenticate

# 2. Verify authentication
gh auth status  # Should show: ✓ Logged in to github.com
```

**GitHub Authentication Details**:
- Protocol: Git (SSH/HTTPS) for repository operations, HTTPS for API operations (gh CLI)
- The gh CLI will guide you through the authentication process
- Required scopes: `repo`, `read:org`, `workflow`

#### Branch Conflicts
```bash
# Rebase on main
git fetch origin
git rebase origin/main

# If conflicts occur
git status  # See conflicted files
# Edit conflicts
git add <resolved-files>
git rebase --continue
```

#### Accidental Commits
```bash
# Undo last commit (keep changes)
git reset --soft HEAD~1

# Undo last commit (discard changes)
git reset --hard HEAD~1
```

#### Wrong Branch
```bash
# Move commits to new branch
git branch new-branch
git reset --hard origin/main
git checkout new-branch
```

### Getting Help
- Check project documentation: `CLAUDE.md`
- Review similar past PRs: `gh pr list --state merged`
- Check CI logs: `gh run list` and `gh run view`

## Best Practices

### DO's
- ✅ Create issues before starting work
- ✅ Use descriptive branch names
- ✅ Write clear commit messages
- ✅ Keep commits focused and atomic
- ✅ Update documentation with code changes
- ✅ Run tests before pushing
- ✅ Rebase on main regularly
- ✅ Use conventional commit format

### DON'Ts
- ❌ Force push to shared branches
- ❌ Commit directly to main
- ❌ Mix features in one branch
- ❌ Leave commented-out code
- ❌ Ignore failing tests
- ❌ Skip code review
- ❌ Commit sensitive data

## Quick Reference

### Essential Commands
```bash
# Issue management
gh issue list
gh issue view <number>
gh issue create

# Branch management
git checkout -b feature/name
git push origin feature/name
git branch -d feature/name

# PR management
gh pr create
gh pr list
gh pr view <number>
gh pr checkout <number>

# Review
gh pr diff <number>
gh pr comment <number>
```

### Slash Commands
Note: GitHub-specific slash commands are not yet implemented for this repository. Consider creating them following the pattern:
- `/gh_write-issue` - Create new GitHub issue with labels
- `/gh_new-worktree <number>` - Create git worktree for parallel development on an issue
- `/gh_fix-issue <number>` - Complete workflow: create branch, implement fix, run tests, create PR
- `/gh_review-pr <number>` - Automated PR review (use only if no human verification needed)

---

**Last Updated**: 2025-01-12
**Maintainer**: AI Assistant Documentation
