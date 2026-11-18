# Rudy Programming Language — Testing Guide 🐺🧪

This document outlines the testing strategy, test suites, and instructions for running automated and manual tests for the **Rudy** programming language.

---

## 1. Overview
Rudy's testing philosophy focuses on **portability, syntax integrity, and AST execution robustness**. Because the core engine is zero-dependency and runs entirely on the Python Standard Library, testing requires minimal setup.

Automated tests run continuously via **GitHub Actions** (`.github/workflows/ci.yml`) across multiple Python versions (`3.10`, `3.11`, `3.12`, `3.13`) on every push and pull request.

---

## 2. Running Tests Locally

### A. Quick Syntax & Engine Check
To verify that the interpreter loads correctly and parses its internal arguments without syntax errors, run:
```bash
python src/rudy.py --help

B. Executing Example Scripts
Rudy includes an automated integration check that iterates through all .rudy scripts in the examples/ directory and executes them through the AST engine. To run them manually:
for script in examples/*.rudy; do
  echo "Running test: $script"
  python src/rudy.py "$script"
done

3. Writing New Tests
When adding new language features (such as keywords, built-in functions, or control structures), follow these steps to ensure test coverage:
 * Create a new test script inside the examples/ directory (e.g., examples/test_feature.rudy).
 * Write assertions or print statements demonstrating the feature in both English and Portuguese syntax variants.
 * Run the script locally using python src/rudy.py examples/test_feature.rudy.
 * Commit your changes—the GitHub Actions CI pipeline will automatically pick up and validate the new example file.
4. Code Quality & Spelling Checks
We use Typos to prevent spelling errors across documentation and source code files, configured via typos.toml.
To check spelling locally (if you have the typos binary installed):
typos
