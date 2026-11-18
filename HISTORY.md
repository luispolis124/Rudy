# Rudy Language History & Evolution 🐺

This document chronicles the architectural milestones, design decisions, and major releases of the **Rudy** programming language.

---

## v1.0.0 — Complete AST Engine, Package Manager & Official Docs (2026)

Rudy evolved from a prototype script runner into a structured, portable, and fully documented bilingual (PT/EN) programming language.

### Core Engine & Architecture (`src/rudy.py`)
* **Regex-Based Lexer:** Added structured tokenization supporting bilingual keywords, built-in functions, numbers, strings, comparison/arithmetic operators, and single-line comments (`//`).
* **Abstract Syntax Tree (AST) Parser & Runtime:** Replaced line-by-line evaluation with a proper AST node hierarchy (`ProgramaNode`, `FuncaoNode`, `AtribuicaoNode`, `EscreverNode`, `SalvarNode`, `LimparNode`, `SeNode`, `EnquantoNode`) for clean execution and nested control flow.
* **Full Bilingual Parity (PT/EN):** Enabled seamless mixing of English and Portuguese keywords (`if`/`se`, `then`/`entao`, `else`/`senao`, `while`/`enquanto`, `action`/`acao`, `use`/`usar`) and built-in commands (`write`/`escrever`, `ask`/`ler`, `random`/`aleatorio`, `sleep`/`pausar`, `save`/`salvar`, `load`/`carregar`, `clear`/`limpar`).
* **High-Precision Benchmarking:** Integrated `time.perf_counter()` execution timing reported in milliseconds (`ms`) after every run.

### Tooling & Ecosystem
* **Standalone Executable Compiler (`--build`):** Added PyInstaller bundling (`compilar_para_executavel`) that embeds the `.rudy` source code and AST runtime into a standalone binary inside `dist/`.
* **Package Manager (`rudy install`):** Implemented `rudy_install` and `stdlib/` module resolution (`use`/`usar`), allowing developers to download and import external `.rudy` libraries from GitHub or URLs.

### Documentation & Community Standards
* **Complete Technical Guides (`docs/`):** Authored comprehensive English guides covering `TUTORIAL.md`, `BUILDING.md`, `SYNTAX.md`, `FUNCTIONS.md`, `CONTROL_FLOW.md`, `STRINGS.md`, `ERRORS.md`, and `CLASSES.md`.
* **Repository Hygiene & Governance:** Added `.gitignore`, `CODE_OF_CONDUCT.md`, and `AGENTS.md` to establish open-source and AI-assisted development standards.

---

## v0.1.0 — Initial Prototype & Concept

* **Conception:** Designed by **Luis Felipe** to provide a lightweight, zero-dependency scripting language capable of running identically on desktop PCs and mobile terminals (Termux on Android).
* **Core Focus:** Built around simplicity, retro ASCII game development, and bilingual accessibility for Portuguese and English speakers.
