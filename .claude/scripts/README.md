# Worktree Scripts

This directory contains utility scripts for git worktree management.

## Available Scripts

### `setup_worktree.sh`

Automated setup script for git worktrees. This script configures an isolated development environment in a newly created worktree.

**Usage:**
```bash
# From within a worktree directory
cd ../form_filler-feature-1
bash ../form_filler/.claude/scripts/setup_worktree.sh
```

**What it does:**
1. Verifies you're in a git worktree
2. Creates an isolated Python virtual environment (`.venv`)
3. Activates the virtual environment
4. Installs all dependencies using `uv` (or `pip` as fallback)
5. Copies `.env.example` to `.env` if needed
6. Verifies the installation
7. Displays next steps

**Requirements:**
- Python 3.13+
- `uv` (recommended) or `pip`
- Git worktree already created

**Features:**
- Color-coded output for easy reading
- Error handling with clear messages
- Automatic detection of available tools (`uv` vs `pip`)
- Verification of successful setup
- Helpful reminders and next steps

## Integration with GitHub Workflow

This script is automatically referenced by the `/gh_new-worktree` command:

```bash
# 1. Create worktree
/gh_new-worktree 42

# 2. In new terminal, navigate and setup
cd ../form_filler-feature-42
bash ../form_filler/.claude/scripts/setup_worktree.sh

# 3. Start working
claude
/gh_fix-issue 42
```

## Troubleshooting

**Script fails with "Not in a git repository":**
- Ensure you're running the script from within a worktree directory
- Verify the worktree was created correctly with `git worktree list`

**Virtual environment activation fails:**
- Check Python installation: `python --version`
- Ensure `.venv` directory was created: `ls -la .venv`

**Dependency installation fails:**
- Check network connectivity
- Verify `pyproject.toml` exists in the worktree
- Try running manually: `uv pip install -e ".[dev]"`

**Import verification fails:**
- Ensure the virtual environment is activated
- Check for syntax errors in the codebase
- Review the installation output for errors
