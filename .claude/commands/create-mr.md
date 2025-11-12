# Create Merge Request Command

Create a new branch, commit changes, and submit a GitLab merge request.

## Behavior
- Creates a new branch based on current changes
- Formats modified files using ruff (Python formatter)
- Analyzes changes and automatically splits into logical commits when appropriate
- Each commit focuses on a single logical change or feature
- Creates descriptive commit messages following conventional commit format
- Pushes branch to GitLab remote (`origin`)
- Creates merge request with proper summary and test plan

## Guidelines for Automatic Commit Splitting
- Split commits by feature, component, or concern
- Keep related file changes together in the same commit
- Separate refactoring from feature additions
- Ensure each commit can be understood independently
- Multiple unrelated changes should be split into separate commits

## Commit Message Format
Follow conventional commit format:
```
<type>(<scope>): <subject>

<body>

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
```

Types: feat, fix, docs, style, refactor, test, chore

## GitLab Integration
- Uses `glab` CLI for merge request creation
- Pushes to `origin` remote (GitLab)
- ⛔ NEVER uses GitHub (`origin_gh`) or `gh` commands
