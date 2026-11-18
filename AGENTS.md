# AGENTS.md — AI Coding Assistant & Agent Guidelines for Rudy 🐺

This document provides context, architectural constraints, and coding conventions for AI agents and automated tools contributing to the **Rudy** programming language repository.

---

## 1. Project Overview

**Rudy** is a lightweight, bilingual (Portuguese/English) interpreted programming language built in Python, designed for portability across desktop (Windows/Linux/macOS) and mobile environments (Termux on Android), retro ASCII game development, and task automation.

### Repository Layout
* `src/rudy.py`: The complete core engine (Lexer, AST Nodes, Parser, Runtime, Package Manager, and PyInstaller Standalone Compiler).
* `stdlib/`: Standard library modules installed via `rudy install` and imported via `use` / `usar`.
* `examples/`: Sample `.rudy` scripts and ASCII games.
* `docs/`: Complete English technical documentation (`README.md`, `TUTORIAL.md`, `BUILDING.md`, `SYNTAX.md`, `FUNCTIONS.md`, `CONTROL_FLOW.md`, `STRINGS.md`, `ERRORS.md`, `CLASSES.md`).

---

## 2. Core Architectural Rules (Do Not Break)

When modifying `src/rudy.py`, agents **must** preserve the following invariants:

1. **Strict Bilingual Parity (PT/EN):**
   Every keyword, built-in function, and CLI flag must support both English and Portuguese equivalents seamlessly within the same script.
   * Keywords: `if`/`se`, `then`/`entao`, `else`/`senao`, `while`/`enquanto`, `action`/`acao`, `use`/`usar`, `var`.
   * Built-ins: `write`/`escrever`, `ask`/`ler`, `random`/`aleatorio`, `sleep`/`pausar`, `save`/`salvar`, `load`/`carregar`, `clear`/`limpar`.
   * Logical operators: `and`/`e`, `or`/`ou`.

2. **Embedded Stub Synchronization (`compilar_para_executavel`):**
   `src/rudy.py` contains a self-contained `stub_code` template string used by PyInstaller (`--build`) to generate standalone executables. **Any changes made to AST node classes, `Parser`, or `RudyRuntime` must also be mirrored inside `stub_code`** (remembering to escape curly braces `{{` and `}}` inside the Python f-string).

3. **Zero External Runtime Dependencies:**
   Running `.rudy` scripts must rely strictly on the Python 3 standard library (`sys`, `os`, `re`, `random`, `time`, `subprocess`, `urllib.request`) to guarantee instant execution on mobile Termux without extra `pip` setup. `PyInstaller` is strictly optional and only invoked on `--build`.

4. **Execution Benchmark Output:**
   Keep the high-precision execution timer (`time.perf_counter()`) intact at the end of script execution (`[Rudy Benchmark] Tempo de execução: X.XX ms`).

---

## 3. Coding & Documentation Conventions

* **Engine Comments & Identifiers:** Core Python engine internals in `src/rudy.py` use clear Portuguese identifiers and section headers (`# --- 1. LER / ANALISADOR LÉXICO ---`, etc.). Maintain this naming style when extending the engine.
* **Documentation Language:** All files inside `docs/` and root community files (`CODE_OF_CONDUCT.md`, `AGENTS.md`) must be written in clear, technical **English**.
* **Testing Changes:** Before finalizing any PR or code modification, verify both standard execution (`python src/rudy.py examples/<test>.rudy`) and module resolution (`stdlib/`).
