# Recommended branch protection for `main`

Enable branch protection on `main` with these minimum settings:

1. **Require a pull request before merging**
   - Require at least 1 approving review.
   - Dismiss stale approvals when new commits are pushed.
2. **Require status checks to pass before merging**
   - Require the `Lint` workflow.
   - Require the `Tests` workflow.
3. **Require branches to be up to date before merging**
   - Enable the setting that requires the head branch to be rebased or merged with the latest `main` before merge.

Optional hardening:

- Restrict direct pushes to `main`.
- Require conversation resolution before merging.
- Include administrators if the repository should enforce the same policy for everyone.
