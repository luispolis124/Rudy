# Building & Compilation Guide for Rudy 🐺

This document covers how to set up, execute, and package **Rudy** scripts and the interpreter engine across different environments, including PCs (Windows/Linux/macOS) and mobile environments (Termux on Android).

---

## 1. Requirements

To run, develop, or compile Rudy, ensure you have the following installed:
* **Python 3.x** (compatible with modern Python versions)
* **PyInstaller** (optional, required only for standalone binary compilation via `--build`)

---

## 2. Running Rudy Scripts

The core interpreter engine resides in `src/rudy.py`. To execute any `.rudy` script, pass the script path as an argument to the interpreter:

```bash
python src/rudy.py examples/your_script.rudy

```

The engine will tokenize the source code via the Lexer, parse it into an Abstract Syntax Tree (AST), execute the runtime commands, and output the precise execution benchmark timer in milliseconds (`ms`).

---

## 3. Standalone Compilation (`--build`)

Rudy features a built-in compiler function (`compilar_para_executavel`) that automatically generates standalone executables from any `.rudy` script using PyInstaller.

### How to Compile:

```bash
python src/rudy.py examples/your_script.rudy --build

```

### What Happens During the Build Process:

1. **Dependency Check:** Automatically checks if `PyInstaller` is installed in your Python environment (and installs it via `pip` if missing).
2. **Stub Generation:** Embeds your Rudy script into a self-contained Python stub (`rudy_temp_stub.py`) containing the complete AST parser and runtime engine.
3. **Binary Packaging:** Invokes PyInstaller (`--onefile --noconsole`) to compile the stub into a standalone binary.
4. **Output Directory:** The resulting standalone executable is safely generated inside the **`dist/`** directory.
5. **Cleanup:** Automatically removes temporary build files and spec artifacts, keeping your repository pristine.

---

## 4. Cross-Platform Environment Notes

* **PC (Windows / Linux / macOS):** Fully supports standard execution and PyInstaller binary compilation (`.exe` on Windows, native binaries on Unix).
* **Termux (Android):** Optimized for lightweight execution using Python in the terminal (`python src/rudy.py`). Binary compilation via PyInstaller in mobile Termux depends on host architecture support.

```

---
