# Rudy Language Strings & Text Guide 🐺

This document covers how text and strings are handled in the **Rudy** programming language, including quotes, concatenation, escape handling, and text output.

---

## 1. String Literals and Quotes

Strings represent textual data and can be enclosed in either **double quotes (`"`)** or **single quotes (`'`)**. 

* **Syntax Rules:**
  * Both quote types are fully supported by the Lexer and Runtime.
  * Strings must start and end with the same quotation mark.

### Examples:
```rudy
var greeting = "Hello, retro world!"
var title = 'Rudy Language v1.0'

write(greeting)
write(title)

```

---

## 2. String Concatenation

Rudy supports string concatenation using the **plus operator (`+`)**. You can combine literal strings, stored variables, and numerical values seamlessly.

### Example:

```rudy
var player_name = "Rudy"
var score = 1500

// Combining strings and variables
write("Player: " + player_name + " | Score: " + score)

```

*(Note: When numbers are added to strings using `+`, the runtime automatically converts them into their string representation for seamless message formatting).*

---

## 3. Empty Strings & Dynamic Text

You can initialize empty strings or update their values dynamically throughout the execution of a script or game loop.

### Example:

```rudy
var status = ""
status = "Loading ASCII assets..."
write(status)

status = "Ready!"
write(status)

```

---

## 4. File I/O Text Handling

When saving or loading files using `save()` / `salvar()` and `load()` / `carregar()`, strings serve as the raw contents written to or read from disk.

### Example:

```rudy
var save_data = "level=3|score=4500"
save("savegame.dat", save_data)

var loaded_data = load("savegame.dat")
write("Loaded save file: " + loaded_data)

```

```

Basta salvar este conteúdo dentro de **`docs/STRINGS.md`**, e a documentação oficial da Rudy (Functions, Errors, Syntax, Control Flow e Strings) estará completamente estruturada, limpa e com padrão profissional de código aberto! 🐺📁✨

```
