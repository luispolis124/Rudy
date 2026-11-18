# Rudy Programming Language — Continuous Integration (CI/CD) Guide 🐺⚙️

This document describes the automated CI/CD pipelines, security audits, and ecosystem mapping workflows configured for the **Rudy** programming language repository.

---

## 1. Overview of Workflows
All automated workflows reside in the **`.github/workflows/`** directory and execute on GitHub Actions runners (Ubuntu Linux environments). They ensure that every push and pull request maintains strict syntax integrity, multi-version compatibility, clean spelling, and security compliance.

---

## 2. Active Workflows & Pipelines

### A. Rudy CI (`ci.yml`)
* **Triggers:** Push or Pull Request to `main` / `master`.
* **Matrix Testing:** Runs the test suite across multiple Python versions in parallel: **`3.10`**, **`3.11`**, **`3.12`**, and **`3.13`**.
* **Steps Performed:**
  1. Clones the repository and sets up the selected Python version.
  2. Upgrades `pip` and installs the package locally (`pip install .`).
  3. Executes parser and interpreter sanity checks (`python src/rudy.py`).
  4. Iterates through all integration test scripts inside the `examples/` directory to validate AST execution.
* **Spell Checking:** Integrates `crate-ci/typos` to automatically catch typos across documentation and source code (customized via `typos.toml`).

### B. Security & Advisory Review (`advisory-review.yml`)
* **Triggers:** Push, Pull Request, and a weekly cron schedule (Mondays at 08:00 UTC).
* **Purpose:** Performs dependency vulnerability scanning using `pip-audit` to ensure the project environment remains secure against known vulnerabilities.

### C. Rudy Cloud & Ecosystem Mapping (`cloud-maps.yml`)
* **Triggers:** Push to `main` / `master` or manual dispatch.
* **Purpose:** Automatically indexes the repository structure—scanning the standard library (`stdlib/`), editor configurations (`editors/`), and example scripts—to generate an `ecosystem-map.json` topology artifact.

### D. Generated & Regeneration Pipeline (`generated-regen.yml`)
* **Triggers:** Changes to `src/` or `examples/` directories.
* **Purpose:** Installs PyInstaller and tests standalone binary compilation (`python src/rudy.py <script> --build`) in a clean CI environment, packaging the resulting binaries into downloadable GitHub Actions artifacts.

---

## 3. Contributing & Local Pipeline Verification
If you want to verify that your local changes will pass all CI checks before pushing to GitHub:

1. **Test Syntax & Interpreter:**
   ```bash
   python src/rudy.py examples/ola.rudy

 * Test Standalone Compilation:
   python src/rudy.py examples/ola.rudy --build

 * Run Spelling Check (if typos is installed):
   typos


---
