# Fix GitHub Issue

Follow these steps:
1. Use 'gh issue view $ARGUMENTS' to get the issue details
2. Search the codebase with grep/glob to find:
   - Existing similar implementations we can reuse
   - Related files mentioned in CLAUDE.md architecture
   - Existing utilities/components that solve similar problems
3. Before writing ANY new code, explicitly check if we already have:
   - Similar components in /components
   - Similar utilities in /utils
   - Similar patterns elsewhere in the codebase
4. Implement the fix by REUSING existing code wherever possible
5. Run tests and linting
6. Create a branch named 'fix-issue-$ARGUMENTS'
7. Commit with message referencing the issue
8. Create PR with 'gh pr create --base dev'

CRITICAL: Maximize code reuse. Check CLAUDE.md for architecture patterns.
