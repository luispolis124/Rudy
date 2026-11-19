# 🐺 Rudy Commands Guide — PC & Termux (Android)

Welcome to the official command reference guide for **Rudy**. Whether you are developing on a desktop workstation or coding on the go using your smartphone, this guide covers everything you need to run, compile, and test your Rudy scripts.

---

## 💻 1. PC Environment (Windows / Linux / macOS)

Make sure you have **Python 3** installed on your system.

### Running a Script (AST Interpreter)
Execute any `.rudy` file directly through the core interpreter engine:

python src/rudy.py examples/masmorra.rudy

Running via Bytecode VM (High Performance)
To compile and execute your script using the intermediate bytecode optimization layer:
python src/rudy.py examples/masmorra.rudy --bytecode

Interactive REPL Shell
Launch the continuous command-line shell to test snippets on the fly while keeping variable states in memory:
python src/rudy.py --repl

(Or simply run python src/rudy.py without arguments).
Installing Packages from Standard Library / GitHub
Download and install third-party .rudy modules directly into your local stdlib/ folder:
python src/rudy.py install math

Building Standalone Binaries (.exe / Executable)
Bundle your script and the interpreter into a single standalone binary using PyInstaller:
python src/rudy.py examples/masmorra.rudy --build

(The generated executable will be placed inside the dist/ folder).
📱 2. Mobile Environment — Termux (Android)
Rudy runs exceptionally well on mobile devices via Termux, turning your Android phone into a full portable development studio.
Initial Setup in Termux
First, update your packages, install Python, Git, and clone your repository:
pkg update && pkg upgrade
pkg install python git
git clone https://github.com/luispolis124/Rudy.git
cd Rudy

Running Scripts on Mobile
Execute your scripts directly in your phone's terminal:
python src/rudy.py examples/masmorra.rudy

Using the Mobile REPL Shell
Test your bilingual logic on the fly right from your phone:
python src/rudy.py

Installing Packages on Termux
Download modules on the go:
python src/rudy.py install math

⌨️ Quick Command Cheat Sheet
| Action | PC Command | Termux (Android) Command |
|---|---|---|
| Run Script | python src/rudy.py file.rudy | python src/rudy.py file.rudy |
| Bytecode Mode | python src/rudy.py file.rudy --bytecode | python src/rudy.py file.rudy --bytecode |
| Interactive REPL | python src/rudy.py | python src/rudy.py |
| Install Package | python src/rudy.py install <pkg> | python src/rudy.py install <pkg> |
| Build Binary | python src/rudy.py file.rudy --build | Not recommended on mobile |

---
