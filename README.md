<div align="center">
  <img src="assets/logo-rudy.png" alt="Rudy Logo - Maned Wolf" width="220"/>

  # Rudy
  **Rudy — A versatile, cross-platform programming language inspired by the Maned Wolf.**

  [![License](https://img.shields.io/badge/License-Apache_2.0-D9531E.svg)](https://opensource.org/licenses/Apache-2.0)
  [![Status](https://img.shields.io/badge/Status-Active_Development-2E7D32.svg)]()
  [![Made in Brazil](https://img.shields.io/badge/Made_in-Brazil_🇧🇷-009C3B.svg)]()
</div>

---

## About Rudy

**Rudy** is a multipurpose programming language designed to unite **panoramic readability**, **cross-platform portability** (PC and Termux/Android), and **complete flexibility**. Inspired by the **Maned Wolf** (*Chrysocyon brachyurus*) — our official mascot and symbol of the Brazilian Cerrado —, Rudy empowers developers to build anything: from text-based games (RPGs, Roguelikes) and ASCII animations to utilities, calculators, and system scripts.

* **Bilingual Syntax Support:** Write natively using either English keywords (`action`, `write`, `while`, `if`, `else`, `ask`) or Portuguese keywords (`acao`, `escrever`, `enquanto`, `se`, `senao`, `ler`).
* **Multipurpose Engine:** Capable of handling logic, math, random generation, file persistence (`save`/`load`), and terminal timing (`sleep`/`clear`).
* **Lightweight & Portable:** Built with a clean Python interpreter core, running smoothly across desktop environments and mobile terminals.
* **National Identity:** Crafted in Brazil for the global open-source community under the Apache 2.0 License.

---

## Code Example (RPG / Interactive Script)

Here is how flexible and intuitive a program looks in **Rudy** (`.rudy` extension):

```rudy
// Interactive adventure example in Rudy
action main() {
    write("=== WELCOME TO RUDY ===")
    name = ask("What is your character name? ")
    
    hp = 50
    write("Hello, " + name + "! Your initial HP is " + hp)

    // Using random and conditions
    damage = random(10, 25)
    hp = hp - damage
    write("A wild obstacle appeared and caused " + damage + " damage!")

    if (hp > 25) then {
        write("Status: You are still strong!")
    } else {
        write("Status: Warning! HP is low!")
    }
}

Core Features & Built-in Functions
The Rudy interpreter supports a rich set of runtime tools for developers:
 * Input & Output: write(...) / escrever(...) and ask(...) / ler(...)
 * Control Flow: if (...) then { ... } else { ... } and while (...) { ... }
 * Randomization & Math: random(min, max) / aleatorio(min, max) and basic arithmetic (+, -, *, /)
 * Time & Animation Control: sleep(seconds) / pausar(seconds) and clear() / limpar() for ASCII frame rendering
 * File Persistence: save(path, content) / salvar(path, content) and load(path) / carregar(path)
Project Structure
 * assets/ — Official logos, icons, and brand assets
 * src/ — Interpreter and core engine (rudy.py)
 * examples/ — Sample .rudy scripts, programs, and mini-games
 * LICENSE — Apache 2.0 License
 * README.md — Main project documentation
How to Run
Make sure you have Python 3 installed, then run any .rudy script from your terminal:
python src/rudy.py examples/example.rudy

How to Contribute
Contributions, ideas, and suggestions are always welcome! Feel free to open an Issue or submit a Pull Request.
License
This project is licensed under the Apache License 2.0. See the LICENSE file for more details.
<div align="center">
Made with dedication in Brazil 🇧🇷 by <b>Luis Felipe</b>
</div>

---
