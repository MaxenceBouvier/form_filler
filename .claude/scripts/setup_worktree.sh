#!/bin/bash
# Setup script for git worktrees
# This script sets up an isolated development environment in a git worktree

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Helper functions
print_step() {
    echo -e "${BLUE}==>${NC} $1"
}

print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

# Check if running in a worktree
print_step "Verifying worktree environment..."
if ! git rev-parse --is-inside-work-tree &>/dev/null; then
    print_error "Not in a git repository!"
    exit 1
fi

WORKTREE_DIR=$(git rev-parse --show-toplevel)
WORKTREE_NAME=$(basename "$WORKTREE_DIR")

# Check if this is actually a worktree (not the main repo)
if git rev-parse --git-common-dir 2>/dev/null | grep -q "$(git rev-parse --git-dir)"; then
    print_warning "This appears to be the main repository, not a worktree."
    print_warning "This script is intended for worktree setup, but continuing anyway..."
fi

print_success "Working in: $WORKTREE_DIR"
print_success "Branch: $(git branch --show-current)"

# Setup Python virtual environment
print_step "Setting up Python virtual environment..."
if [ -d ".venv" ]; then
    print_warning "Virtual environment already exists. Skipping creation."
else
    if command -v uv &>/dev/null; then
        print_step "Using uv to create virtual environment..."
        uv venv .venv
    else
        print_step "Using python to create virtual environment..."
        python -m venv .venv
    fi
    print_success "Virtual environment created at .venv/"
fi

# Activate virtual environment
print_step "Activating virtual environment..."
source .venv/bin/activate

# Verify activation
if [ "$VIRTUAL_ENV" != "" ]; then
    print_success "Virtual environment activated: $VIRTUAL_ENV"
else
    print_error "Failed to activate virtual environment!"
    exit 1
fi

# Install dependencies
print_step "Installing dependencies..."
if command -v uv &>/dev/null; then
    print_step "Using uv pip install..."
    uv pip install -e ".[dev]"
else
    print_step "Using pip install..."
    pip install -e ".[dev]"
fi
print_success "Dependencies installed"

# Setup environment file if needed
print_step "Checking for environment configuration..."
if [ -f ".env.example" ] && [ ! -f ".env" ]; then
    print_step "Copying .env.example to .env..."
    cp .env.example .env
    print_success "Created .env file"
    print_warning "Remember to update .env with worktree-specific paths if needed!"
elif [ -f ".env" ]; then
    print_success ".env file already exists"
else
    print_success "No .env.example found (may not be needed for this project)"
fi

# Verify installation
print_step "Verifying installation..."
if python -c "import form_filler" 2>/dev/null; then
    print_success "form_filler package is importable"
else
    print_error "Failed to import form_filler package!"
    exit 1
fi

# Show installed packages
print_step "Installed packages:"
if command -v uv &>/dev/null; then
    uv pip list
else
    pip list
fi

echo ""
print_success "Worktree setup complete!"
echo ""
echo -e "${BLUE}Next steps:${NC}"
echo "1. Ensure you're in the worktree directory: cd $WORKTREE_DIR"
echo "2. Activate the virtual environment: source .venv/bin/activate"
echo "3. Start working on your feature/fix"
echo ""
echo -e "${YELLOW}Important reminders:${NC}"
echo "• This worktree has its own isolated .venv"
echo "• Always activate the virtual environment before working"
echo "• Don't modify files in other worktrees or the main repo"
echo "• Use 'deactivate' to exit the virtual environment when done"
