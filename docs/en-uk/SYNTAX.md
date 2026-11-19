# Rudy Language Syntax Guide 🐺

This document defines the formal grammar, keywords, variable declarations, and structural rules of the **Rudy** programming language. Rudy is designed to be lightweight, readable, and fully bilingual (supporting both English and Portuguese syntax).

---

## 1. Comments
Comments are ignored by the Lexer and Parser. Rudy supports single-line comments using double slashes:
```rudy
// This is a comment in Rudy / Isto é um comentário na Rudy
var score = 10

```

---

## 2. Variables and Data Types

Variables are declared using the `var` keyword followed by an identifier and an assignment operator (`=`). Rudy dynamically handles numbers, strings, and booleans.

* **Syntax (EN/PT):**
```rudy
var name = "Rudy"
var points = 100
var is_active = true

```



---

## 3. Bilingual Keywords Reference

Rudy allows developers to interchange English and Portuguese keywords seamlessly within the same script:

| Category | English Keyword | Portuguese Keyword | Description |
| --- | --- | --- | --- |
| **Control Flow** | `if` | `se` | Conditional branch header |
| **Control Flow** | `then` | `entao` | Executes after the condition |
| **Control Flow** | `else` | `senao` | Alternative conditional branch |
| **Control Flow** | `while` | `enquanto` | Loop repetition structure |
| **Variable** | `var` | `var` | Variable declaration |
| **Function** | `action` | `acao` | Custom user function definition |

---

## 4. Control Structures

### Conditionals (`if` / `se`)

Conditionals evaluate expressions and execute code blocks enclosed in curly braces `{}`.

* **English Style:**
```rudy
if (health > 0) then {
    write("Player is alive")
} else {
    write("Game Over")
}

```


* **Portuguese Style:**
```rudy
se (vida > 0) entao {
    escrever("Jogador está vivo")
} senao {
    escrever("Fim de Jogo")
}

```



### Loops (`while` / `enquanto`)

Loops execute a block of commands repeatedly as long as the logical condition remains true.

* **English Style:**
```rudy
var count = 0
while (count < 3) {
    write("Iteration: " + count)
    count = count + 1
}

```


* **Portuguese Style:**
```rudy
var contador = 0
enquanto (contador < 3) {
    escrever("Iteração: " + contador)
    contador = contador + 1
}

```



---

## 5. User-Defined Functions (`action` / `acao`)

Functions allow you to group reusable blocks of code. They are defined using parentheses `()` and curly braces `{}`.

* **Syntax:**
```rudy
action setup_game() {
    clear()
    write("Initializing retro environment...")
}

acao configurar_jogo() {
    limpar()
    escrever("Inicializando ambiente retro...")
}

```



---

## 6. Expressions and Operators

* **Arithmetic Operators:** `+`, `-`, `*`, `/` (integer division)
* **Comparison Operators:** `==`, `!=`, `>`, `<`, `>=`, `<=`
* **Logical Operators:** `and` / `e`, `or` / `ou`
* **String Concatenation:** Handled via the `+` operator (e.g., `"Score: " + points`).

```

---
