# Create GitHub Issue with Agent Analysis and Child Issue Support

DO NOT IMPLEMENT ANYTHING. DO NOT MODIFY ANY CODE FILES.

## Phase 1: Agent-Based Analysis

Based on the nature of $ARGUMENTS, use the appropriate agent(s) to analyze requirements:

### Agent Selection Logic:
- **Complex features or architectural changes**: Use `architect-reviewer` agent to review architecture impact
- **Bug fixes or debugging tasks**: Use `general-purpose` agent to analyze the bug context
- **Performance optimizations**: Use `general-purpose` agent to identify bottlenecks
- **Code quality improvements**: Use `code-reviewer` agent to assess current state
- **Documentation tasks**: Use `general-purpose` agent to identify gaps
- **Exploration tasks**: Use `Explore` agent to understand codebase areas

Launch the appropriate agent(s) with Task tool:
```
Task: Analyze requirements for: $ARGUMENTS
- Review architecture impact if relevant
- Identify affected components
- Suggest implementation approach
- Determine if task should be split into subtasks
- Estimate complexity and effort
```

## Phase 2: Issue Complexity Assessment

Based on agent analysis, determine if the issue needs to be split:

### Split into child issues when:
- Task requires changes across 3+ modules
- Implementation has 5+ distinct phases
- Different expertise needed for subtasks (e.g., backend + frontend)
- Task involves both refactoring AND new features
- Estimated effort > 2 days
- Agent recommends splitting for clarity

### If splitting is needed:
1. Create parent issue (epic/feature)
2. Create child issues for each subtask
3. Reference child issues in parent using task list

## Phase 3: Create GitHub Issue(s)

Read available project documentation (CLAUDE.md, README.md, CONTRIBUTING.md, etc.) for context.

### For Single Issue:
Generate and execute 'gh issue create' with:
- Detailed title describing the task
- Problem/feature description with architecture context
- Agent analysis results integrated into description
- Affected components and files
- Technical considerations
- Suggested implementation approach (from agent analysis)

```bash
gh issue create --title "[Type]: Brief description" \
                --label "enhancement" \
                --body "## Overview
$DESCRIPTION

## Agent Analysis
$AGENT_RESULTS

## Affected Components
- [Component/Module 1]: [specific files]
- [Component/Module 2]: [specific files]

## Technical Approach
[Agent-recommended approach]

## Acceptance Criteria
- [ ] Criterion 1
- [ ] Criterion 2"
```

### For Parent + Child Issues:

#### Step 1: Create child issues first (bottom-up)
```bash
# Create each child issue and capture its number
CHILD1_NUM=$(gh issue create --title "[Subtask] Specific component work" \
                             --label "enhancement,subtask" \
                             --body "## Subtask Description
[Detailed description]

## Dependencies
- Depends on: [Other tasks if any]
- Blocks: [Tasks this blocks]

## Implementation Notes
[From agent analysis]" --json number --jq '.number')

CHILD2_NUM=$(gh issue create --title "[Subtask] Another component" \
                             --label "enhancement,subtask" \
                             --body "## Subtask Description
[Details]" --json number --jq '.number')
```

#### Step 2: Create parent issue with task list referencing children
```bash
# Create parent issue with child issue references in task list
gh issue create --title "[Epic] $FEATURE_NAME" \
                --label "epic,enhancement" \
                --body "## Overview
$EPIC_DESCRIPTION

## Architecture Impact
[From agent analysis]

## Subtasks
- [ ] #$CHILD1_NUM Specific component work
- [ ] #$CHILD2_NUM Another component
- [ ] #$CHILD3_NUM Additional work

## Success Criteria
[Overall success metrics]

---
**Child Issues**: #$CHILD1_NUM, #$CHILD2_NUM, #$CHILD3_NUM"
```

#### Step 3: Update child issues to reference parent
```bash
# After parent is created, update each child to reference it
PARENT_NUM=$(gh issue list --label "epic" --limit 1 --json number --jq '.[0].number')

gh issue edit $CHILD1_NUM --add-label "epic:$PARENT_NUM" \
                          --body "$(gh issue view $CHILD1_NUM --json body --jq '.body')

---
**Parent Epic**: #$PARENT_NUM"

gh issue edit $CHILD2_NUM --add-label "epic:$PARENT_NUM" \
                          --body "$(gh issue view $CHILD2_NUM --json body --jq '.body')

---
**Parent Epic**: #$PARENT_NUM"
```

### Auto-detect labels:
- **Type labels**: 'enhancement', 'bug', 'documentation', 'refactoring', 'optimization'
- **Scope labels**: 'epic', 'feature', 'subtask'
- **Module labels**: Detect from project structure (e.g., 'backend', 'frontend', 'api', 'database', 'infrastructure')
- **Priority labels**: 'critical', 'high', 'medium', 'low' (based on agent assessment)
- **Epic tracking**: 'epic:N' where N is the parent issue number

### Relationship Indicators:
GitHub doesn't have native issue linking like GitLab, but we can use:
- **Task lists**: Checkbox lists with `#issue_number` references
- **Labels**: `epic:N` label to group related issues
- **Body references**: Mention related issues in the body
- **Keywords**: Use "Blocks #N", "Depends on #N", "Part of #N" in issue descriptions

## Phase 4: Verify and Report

After creating issues:
1. List created issues with their numbers
2. Show the hierarchy (if parent/child created)
3. Provide links to view issues in browser:
   ```bash
   gh issue view $ISSUE_NUMBER --web
   ```

## Example: Complex Feature Breakdown

**User Request**: "Add comprehensive testing framework with coverage reports"

**Agent Analysis Result**: Task is complex, spans multiple modules, ~3-4 days effort

**Created Structure**:
```
[Epic] #100: Add comprehensive testing framework
├── #101: Set up pytest infrastructure (subtask of #100)
├── #102: Add unit tests for circuit_graph (subtask of #100)
├── #103: Add integration tests (subtask of #100)
└── #104: Set up coverage reporting (subtask of #100)
```

## IMPORTANT:
- **Always use agents first**: Let specialized agents analyze before creating issues
- **Wait for agent completion**: Don't proceed until agent analysis is complete
- **If requirements unclear**: Ask user for clarification BEFORE creating issues
- **Check authentication**: If gh commands fail, ask user to check authentication with `gh auth status`
- **Save drafts on failure**: If API calls fail, save issue descriptions to files
- **GitHub API rate limits**: Be mindful of rate limits when creating multiple issues

Your job ends after creating and linking the issue(s). Do NOT write any code or modify any files.
