# Fix GitLab Issue

Follow these steps:
1. Use 'glab issue view $ARGUMENTS' to get the issue details from GitLab
2. Search the codebase with grep/glob to find:
   - Existing similar implementations we can reuse
   - Related files mentioned in CLAUDE.md architecture
   - Existing utilities/components that solve similar problems
3. Before writing ANY new code, explicitly check if we already have:
   - Similar modules in src/circuit_graph or src/ngspice_optimizer
   - Similar patterns elsewhere in the codebase
   - Existing device specs, parameters, or optimizations
4. Create a branch following naming convention:
   - For bugs: 'fix/$ARGUMENTS-description'
   - For features: 'feature/$ARGUMENTS-description'
5. Implement the fix by REUSING existing code wherever possible
6. Run tests and linting:
   - pytest for unit tests
   - ruff check for linting
7. Commit with conventional format: 'fix(scope): description (#$ARGUMENTS)'
8. Push branch and create MR with:
   ```bash
   glab mr create --target-branch master --title "Fix #$ARGUMENTS: [description]" \
                  --description "Closes #$ARGUMENTS\n\n## Summary\n[Describe changes]\n\n## Test Plan\n[How tested]"
   ```

CRITICAL:
- Maximize code reuse. Check CLAUDE.md for architecture patterns.
- Follow three-layer architecture (circuit_graph, circuit_explorer, ngspice_optimizer)
- Maintain backward compatibility with ngspice_param_optimizer shim
- **File Placement:** NEVER create files in root directory:
  - Tests → tests/
  - Scripts → scripts/
  - Documentation → docs/ or .claude/docs/
  - Examples → examples/
  - See CLAUDE.md "File Placement Rules" section
- **When uncertain about implementation approach:** Use AskUserQuestion tool to clarify
- **Favor best practices over user preferences** (but explain trade-offs)
