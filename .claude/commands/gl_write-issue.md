# Create GitLab Issue

DO NOT IMPLEMENT ANYTHING. DO NOT MODIFY ANY CODE FILES.

Read CLAUDE.md and .claude/docs/CODEBASE_DOCUMENTATION.md. For: $ARGUMENTS, ONLY create a GitLab issue (do not implement the feature/fix).

Generate and execute 'glab issue create' with:
- Detailed title describing the task
- Problem/feature description with architecture context (three-layer model)
- Affected components and files:
  - circuit_graph module paths
  - ngspice_optimizer module paths
  - Relevant device specs, parameters, or templates
- Technical considerations:
  - Impact on netlist generation
  - PDK mode compatibility
  - Backward compatibility requirements
- Suggested implementation approach (describe in words, no code changes)

Auto-detect type and add appropriate labels:
- 'enhancement' for new features
- 'bug' for defects
- 'documentation' for doc updates
- 'refactoring' for code improvements
- 'optimization' for performance improvements
- Add module label if specific: 'circuit-graph', 'ngspice-optimizer'

Example command:
```bash
glab issue create --title "[Type]: Brief description" \
                  --label "enhancement,circuit-graph" \
                  --description "## Overview\n$DESCRIPTION\n\n## Affected Components\n...\n\n## Technical Approach\n..."
```

Your job ends after creating the issue. Do NOT write any code or modify any files.

IMPORTANT:
- **If requirements are unclear or ambiguous:** Ask the user for clarification BEFORE creating the issue
- **If multiple valid approaches exist:** Present options in the issue description with pros/cons
- **Favor best practices:** Recommend state-of-the-art solutions in the suggested approach
