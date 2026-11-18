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

## 🔵 Phase 2: Ecosystem & Developer Experience (Current Focus)
*Status: In Progress*

- [x] **CI/CD Automation:** Multi-version Python testing pipeline via GitHub Actions (`ci.yml`).
- [x] **Code Quality & Compliance:** Standardized packaging (`pyproject.toml`), third-party attribution (`THIRDPARTY.md`), and automated spelling validation (`typos.toml`).
- [ ] **Extended Standard Library Modules:** Implement core built-in modules for mathematical operations, string manipulation, and file system utilities.
- [ ] **Interactive REPL Mode:** Develop a continuous command-line interface shell for testing snippets on the fly.

---

## 🟣 Phase 3: Performance & Advanced Tooling
*Status: Planned*

- [x] **Cross-Platform Portability:** Optimized execution across desktop operating systems and mobile terminal environments (Termux).
- [ ] **Bytecode Compiler (Optional):** Explore bytecode generation layer to improve execution speed for large scripts.
- [ ] **IDE Syntax Highlighting Extensions:** Create community extensions for VS Code and mobile editors highlighting Rudy keywords in both languages.

---

## 🌟 Long-Term Vision
Rudy aims to remain lightweight, transparent, and completely self-contained—proving that powerful programming paradigms can be elegant, bilingual, and accessible anywhere from high-end workstations to mobile terminals.
