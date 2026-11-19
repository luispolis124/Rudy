# Rudy Programming Language — Project Roadmap 🐺🚀

Welcome to the official roadmap for **Rudy**. This document outlines our development milestones, planned features, and long-term vision for creating a zero-dependency, portable, and bilingual programming language.

---

## 🟢 Phase 1: Core Foundation & Interpreter (Completed)
*Status: Released & Stable*

- [x] **Lexer & AST Parser:** Robust tokenization and Abstract Syntax Tree engine (`src/rudy.py`).
- [x] **Bilingual Keyword Support:** Native syntax support for both English (`if`, `while`, `write`) and Portuguese (`se`, `enquanto`, `escrever`).
- [x] **Standard Library & Imports (`use`/`usar`):** Modular package loading from `stdlib/`.
- [x] **Package Manager (`rudy install`):** Automated retrieval of third-party `.rudy` scripts and GitHub packages.
- [x] **Standalone Compiler (`--build`):** Zero-dependency binary compilation using PyInstaller.

---

## 🔵 Phase 2: Ecosystem & Developer Experience (Completed)
*Status: Completed & Stable*

- [x] **CI/CD Automation:** Multi-version Python testing pipeline via GitHub Actions (`ci.yml`).
- [x] **Code Quality & Compliance:** Standardized packaging (`pyproject.toml`), third-party attribution (`THIRDPARTY.md`), and automated spelling validation (`typos.toml`).
- [x] **Extended Standard Library Modules:** Core built-in utility modules for mathematical operations, string manipulation, and file system tasks inside `stdlib/`.
- [x] **Interactive REPL Mode:** Continuous command-line shell interface (`--repl`) for testing snippets on the fly while retaining state.

---

## 🟣 Phase 3: Performance & Advanced Tooling (Completed)
*Status: Completed & Stable*

- [x] **Cross-Platform Portability:** Optimized execution across desktop operating systems and mobile terminal environments (Termux).
- [x] **Bytecode Compiler (Optional):** Intermediate bytecode generation layer (`--bytecode` / `.rudybc`) to accelerate execution speed for large scripts.
- [x] **IDE Syntax Highlighting Extensions:** Official community extensions for VS Code (`editors/vscode/`) and mobile editors highlighting Rudy keywords in both languages.

---

## 🌟 Long-Term Vision
Rudy aims to remain lightweight, transparent, and completely self-contained—proving that powerful programming paradigms can be elegant, bilingual, and accessible anywhere from high-end workstations to mobile terminals.
