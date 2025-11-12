# Create Git Worktree for GitHub Issue

DO NOT IMPLEMENT ANYTHING. DO NOT MODIFY ANY CODE FILES.

This command creates a git worktree for parallel development on a specific GitHub issue.

Follow these steps:

1. **Get repository name:**
   ```bash
   REPO_NAME=$(basename $(git rev-parse --show-toplevel))
   ```

2. **Fetch issue details:**
   ```bash
   gh issue view $ARGUMENTS
   ```

3. **Determine branch type and name:**
   - For bugs → `fix/$ARGUMENTS-<description>`
   - For features/enhancements → `feature/$ARGUMENTS-<description>`
   - Extract a short description (2-4 words) from the issue title
   - Convert to lowercase with hyphens (e.g., "auth-fix", "api-endpoint")

4. **Create the worktree:**
   ```bash
   # Example for feature #5 about user authentication:
   git worktree add -b feature/5-auth-endpoint ../${REPO_NAME}-feature-5 main

   # Pattern:
   # git worktree add -b <branch-name> ../${REPO_NAME}-<type>-<issue-number> main
   ```

5. **Verify creation:**
   ```bash
   git worktree list
   ```

6. **Inform the user with clear next steps:**
   ```
   ✅ Created worktree for issue #$ARGUMENTS
   📂 Location: ../${REPO_NAME}-<type>-<issue-number>
   🌿 Branch: <branch-name>

   Next steps:
   1. Open a new terminal
   2. cd ../${REPO_NAME}-<type>-<issue-number>
   3. Run the setup script:
      bash ../${REPO_NAME}/.claude/scripts/setup_worktree.sh

   4. Start Claude:
      claude

   5. Implement the fix:
      /gh_fix-issue $ARGUMENTS

   The new Claude instance will implement the fix in an isolated worktree.

   ⚠️  CRITICAL:
   - Each worktree has its own .venv (created by setup script)
   - Always activate the virtual environment before working
   - Don't modify files in other worktrees or the main repo
   ```

IMPORTANT:
- This command ONLY creates the worktree - it does NOT implement the fix
- The user will start a new Claude instance in the worktree directory
- The new Claude instance will run `/gh_fix-issue` to implement the solution
- This workflow enables parallel development without branch conflicts

ERROR HANDLING:
- If worktree path already exists, inform user and suggest cleanup:
  ```bash
  git worktree remove ../${REPO_NAME}-<type>-<issue-number>
  ```
- If branch already exists, use it instead of creating new one
- If issue not found, report error and exit
