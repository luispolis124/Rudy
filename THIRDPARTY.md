# Third-Party Licenses & Software Attribution 🐺

The **Rudy** programming language project incorporates or relies upon the following open-source software, tools, and libraries. We deeply appreciate the open-source community for making these tools available.

---

## 1. Core Development & Runtime Dependencies
Rudy's core engine relies strictly on the **Python Standard Library** (Python 3.8+), ensuring zero external runtime dependencies for script execution and maximum portability across desktop environments and mobile terminals (Termux).

* **Python Standard Library** (`sys`, `os`, `re`, `random`, `time`, `subprocess`, `urllib.request`)
  * **License:** Python Software Foundation License (PSF License)

---

## 2. Optional Build & Compilation Tools
* **PyInstaller** (Used via `--build` to package `.rudy` scripts into standalone executables)
  * **Repository:** https://github.com/pyinstaller/pyinstaller
  * **License:** GNU General Public License v2.0 (GPLv2) with runtime exception

---

## 3. Code Quality, Formatting & Development Tooling
* **Black** (Python Code Formatter)
  * **Repository:** https://github.com/psf/black
  * **License:** MIT License
* **Setuptools** (Python Packaging Library)
  * **Repository:** https://github.com/pypa/setuptools
  * **License:** MIT License
