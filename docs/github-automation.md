# GitHub Automation Guide

This document explains the end-to-end CI/CD, security scanning, and PR management
automation implemented in this repository, and how to **reuse it in other repos**.

---

## Overview

```
.github/
├── CODEOWNERS                        # Auto-assigns reviewers by file path
├── dependabot.yml                    # Automated dependency updates
├── labeler.yml                       # PR auto-labeling rules
├── codeql-config.yml                 # CodeQL query + path configuration
└── workflows/
    ├── ci.yml                        # Main orchestrator (push + PR)
    ├── ci-reusable.yml               # ★ Reusable CI template (workflow_call)
    ├── codeql.yml                    # ★ Reusable CodeQL security scanner
    ├── pr-automation.yml             # PR labeling, size detection, Copilot review
    ├── auto-merge.yml                # Auto-merge after checks pass
    └── setup-repo.yml                # One-time branch-protection setup (manual)
```

---

## Workflows in Detail

### `ci.yml` — Main CI Orchestrator

Triggered on: `push` to `main`/`develop`, `pull_request` targeting those branches.

| Job | What it does |
|-----|-------------|
| `ci` | Calls `ci-reusable.yml` — lint, type-check, test, security scan |
| `codeql` | Calls `codeql.yml` — static security analysis for Python + JS/TS |
| `dependency-review` | PR-only — checks new dependencies for known vulnerabilities |
| `all-checks-passed` | Gate job — fails if any required job fails; required by branch protection |

---

### `ci-reusable.yml` — Reusable CI Template ⭐

This workflow can be **called from any repository** via `workflow_call`.

#### Inputs

| Input | Type | Default | Description |
|-------|------|---------|-------------|
| `python-version` | string | `3.11` | Python version |
| `node-version` | string | `18` | Node.js version |
| `backend-dir` | string | `./backend` | Path to Python backend |
| `frontend-dir` | string | `./web` | Path to Next.js frontend |
| `run-backend-tests` | boolean | `true` | Run pytest |
| `run-frontend-tests` | boolean | `true` | Run `npm test` |
| `run-security-scan` | boolean | `true` | Run pip-audit + npm audit |

#### Secrets

| Secret | Required | Description |
|--------|----------|-------------|
| `codecov-token` | No | Upload coverage to Codecov |

#### Usage in another repository

```yaml
# .github/workflows/ci.yml  (in your other repo)
name: CI
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  ci:
    uses: abhilashjaiswal0110/presentation_app/.github/workflows/ci-reusable.yml@main
    with:
      python-version: '3.12'
      node-version: '20'
      backend-dir: './src/backend'
      frontend-dir: './src/frontend'
    secrets:
      codecov-token: ${{ secrets.CODECOV_TOKEN }}
```

> **Note**: The calling repository must have access to this repository.
> For a private repo, make the workflow callable across org or use a copy.

---

### `codeql.yml` — Reusable CodeQL Security Scanner ⭐

Scans Python and JavaScript/TypeScript for security vulnerabilities using
GitHub's CodeQL engine. Results appear in **Security → Code scanning alerts**.

Can also be called as a reusable workflow:

```yaml
jobs:
  security:
    uses: abhilashjaiswal0110/presentation_app/.github/workflows/codeql.yml@main
    permissions:
      actions: read
      contents: read
      security-events: write
```

---

### `pr-automation.yml` — PR Automation

Runs on every non-draft PR event. Provides:

1. **Path-based labels** via `labeler.yml` (e.g., `backend`, `frontend`, `documentation`)
2. **Size labels** (`size/XS` through `size/XL`) based on lines changed
3. **Copilot review request** — automatically requests GitHub Copilot as a reviewer
   _(requires GitHub Copilot Enterprise or Copilot Business with code review enabled)_
4. **Welcome comment** with a checklist of running checks

---

### `auto-merge.yml` — Automatic Merge

Enables GitHub's built-in auto-merge when:

- The PR was opened by **Dependabot** (patch/minor updates auto-approved), **or**
- The PR carries the **`auto-merge`** label

The merge is deferred until ALL required status checks pass and required reviews
are approved. Uses squash-merge to keep history clean.

> **Major Dependabot updates** are NOT auto-approved — they receive a comment
> requesting manual review.

---

### `setup-repo.yml` — Branch Protection Setup (One-time)

A **manually triggered** (`workflow_dispatch`) workflow that configures:

- Branch protection on `main` (required checks, required reviews, no force push)
- Vulnerability alerts
- Automated Dependabot security fixes
- Squash-only merge strategy + auto-merge enabled + branch deletion on merge

#### How to run

1. Go to **Actions → Setup Repository Branch Protection**
2. Click **Run workflow**
3. Type `yes` in the confirm field
4. Optionally adjust `required-approvals` and `required-checks`
5. Click **Run workflow**

---

## Reusing in a New Repository

To adopt this automation template in a new repository:

### Step 1 — Copy the GitHub config files

```bash
# From this repo, copy the .github directory to your new repo
cp -r .github/dependabot.yml          <new-repo>/.github/
cp -r .github/CODEOWNERS              <new-repo>/.github/
cp -r .github/labeler.yml             <new-repo>/.github/
cp -r .github/codeql-config.yml       <new-repo>/.github/
cp -r .github/workflows/codeql.yml    <new-repo>/.github/workflows/
cp -r .github/workflows/ci-reusable.yml <new-repo>/.github/workflows/
cp -r .github/workflows/pr-automation.yml <new-repo>/.github/workflows/
cp -r .github/workflows/auto-merge.yml  <new-repo>/.github/workflows/
cp -r .github/workflows/setup-repo.yml  <new-repo>/.github/workflows/
```

### Step 2 — Create a minimal `ci.yml` calling the reusable workflow

```yaml
name: CI/CD Pipeline
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

permissions:
  contents: read

jobs:
  ci:
    uses: ./.github/workflows/ci-reusable.yml
    with:
      python-version: '3.11'
      node-version: '18'
      backend-dir: './backend'
      frontend-dir: './web'

  codeql:
    uses: ./.github/workflows/codeql.yml
    permissions:
      actions: read
      contents: read
      security-events: write

  all-checks-passed:
    name: All Checks Passed
    needs: [ci, codeql]
    runs-on: ubuntu-latest
    if: always()
    steps:
      - run: |
          [[ "${{ needs.ci.result }}" == "success" ]] && exit 0 || exit 1
```

### Step 3 — Update CODEOWNERS

Edit `.github/CODEOWNERS` and replace `@abhilashjaiswal0110` with your GitHub username.

### Step 4 — Run branch protection setup

Trigger the `setup-repo.yml` workflow once as a repository admin.

### Step 5 — Configure optional secrets

| Secret | Where to add | Used by |
|--------|-------------|---------|
| `CODECOV_TOKEN` | Repo secrets | Coverage upload |

---

## Security Model

| Concern | Tool | Where results appear |
|---------|------|----------------------|
| Static code analysis | CodeQL | Security → Code scanning alerts |
| Dependency vulnerabilities (Python) | pip-audit | CI job log |
| Dependency vulnerabilities (JS) | npm audit | CI job log |
| New dependency review | dependency-review-action | PR checks + comment |
| Automated dependency updates | Dependabot | Automatic PRs |
| Secret scanning | GitHub native | Security → Secret scanning alerts |

---

## FAQ

**Q: Why do workflows show `action_required` on the first run?**  
A: GitHub requires the repository owner to manually approve the first workflow run
triggered by a bot actor (such as the Copilot SWE Agent). Go to **Actions tab →
find the pending run → click "Approve and run"**. This is a one-time step. All
subsequent runs from the repo owner's commits will execute automatically.

**Q: Why is my PR blocked from merging?**  
A: The `All Checks Passed` job failed. Check individual job logs for details.

**Q: How do I bypass branch protection for an emergency fix?**  
A: Repository admins can bypass protection by going to the PR and clicking
"Merge without waiting for requirements to be met". The `setup-repo.yml`
workflow sets `enforce_admins: false` for this reason.

**Q: Copilot review isn't being requested — why?**  
A: GitHub Copilot code review requires GitHub Copilot Enterprise or Copilot
Business with the code-review feature enabled on the repository. The step
uses `continue-on-error: true` so it won't block CI if unavailable.

**Q: Can I disable auto-merge for a specific PR?**  
A: Remove the `auto-merge` label, or close and reopen the PR without the label.
For Dependabot PRs, you can comment `@dependabot squash and merge` or
`@dependabot ignore this major version` as needed.
