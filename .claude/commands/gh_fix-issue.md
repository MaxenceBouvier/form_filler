# Fix GitHub Issue

Follow these steps:
1. Use 'gh issue view #$ARGUMENTS --json title,body,labels,assignees,state' to get the issue details from GitHub
2. Search the codebase with grep/glob to find:
   - Existing similar implementations we can reuse
   - Related files mentioned in project documentation (CLAUDE.md, README.md, etc.)
   - Existing utilities/components that solve similar problems
3. Before writing ANY new code, explicitly check if we already have:
   - Similar modules or patterns elsewhere in the codebase
   - Existing utilities that can be extended or reused
   - Relevant tests that demonstrate similar functionality
4. Create a branch following naming convention:
   - For bugs: 'fix/$ARGUMENTS-description'
   - For features: 'feature/$ARGUMENTS-description'
5. Implement the fix by REUSING existing code wherever possible
6. Run tests and linting using the project's configured tools:
   - Check for test commands in package.json, Makefile, or scripts/
   - Run linting/formatting tools as configured (eslint, prettier, ruff, black, etc.)
7. Commit with conventional format: 'fix(scope): description (#$ARGUMENTS)'
8. Push branch and create PR with:
   ```bash
   gh pr create --base main --title "Fix #$ARGUMENTS: [description]" \
                --body "Closes #$ARGUMENTS

## Summary
[Describe changes]

## Test Plan
[How tested]"
   ```

CRITICAL:
- Maximize code reuse. Check project documentation for architecture patterns.
- Follow the project's established architecture and coding conventions
- Maintain backward compatibility with existing APIs and interfaces
- **File Placement:** NEVER create files in root directory:
  - Tests → tests/ or test/
  - Scripts → scripts/
  - Documentation → docs/ or .claude/docs/
  - Examples → examples/
  - Check project structure and follow existing conventions
- **When uncertain about implementation approach:** Use AskUserQuestion tool to clarify
- **Favor best practices over user preferences** (but explain trade-offs)
