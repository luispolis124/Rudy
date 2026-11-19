# Rudy Language Control Flow Guide 🐺

This document covers the control flow structures in **Rudy**, detailing how scripts handle conditional branching, looping, and logical evaluations across both English and Portuguese keywords.

---

## 1. Conditionals (`if` / `se`)

Conditionals allow the interpreter to execute specific blocks of code only when a given boolean condition evaluates to `true`. Rudy supports alternative paths using `else` / `senao`.

### Syntax Rules
* Must use parentheses `()` around the logical condition.
* Must include the `then` or `entao` keyword right before the opening curly brace `{`.
* Code blocks must be enclosed in curly braces `{}`.

### Examples

**English Style:**
```rudy
var score = 85

if (score >= 90) then {
    write("Grade: A - Excellent!")
} else {
    if (score >= 70) then {
        write("Grade: B - Good job!")
    } else {
        write("Grade: Needs Improvement")
    }
}

```

**Portuguese Style:**

```rudy
var pontuacao = 85

se (pontuacao >= 90) entao {
    escrever("Nota: A - Excelente!")
} senao {
    se (pontuacao >= 70) entao {
        escrever("Nota: B - Bom trabalho!")
    } senao {
        escrever("Nota: Precisa melhorar")
    }
}

```

---

## 2. Loops (`while` / `enquanto`)

Loops execute a sequence of commands repeatedly as long as the specified condition remains true. They are ideal for retro animations, counters, and game loops.

### Syntax Rules

* Requires parentheses `()` around the loop condition.
* Requires opening and closing curly braces `{}` to define the repeating block body.

### Examples

**English Style:**

```rudy
var countdown = 3

while (countdown > 0) {
    write("T-minus: " + countdown)
    countdown = countdown - 1
}

write("Liftoff! 🚀")

```

**Portuguese Style:**

```rudy
var contagem = 3

enquanto (contagem > 0) {
    escrever("Contagem regressiva: " + contagem)
    contagem = contagem - 1
}

escrever("Fogo! 🚀")

```

---

## 3. Logical Operators & Complex Conditions

You can combine multiple comparisons inside conditionals and loops using logical conjunctions. Rudy natively supports both English and Portuguese logical operators:

* **AND Operator:** `and` or `e`
* **OR Operator:** `or` or `ou`

### Example with Combined Conditions:

```rudy
var player_hp = 50
var has_key = true

if (player_hp > 0 and has_key == true) then {
    write("Door unlocked! Proceeding to the next level.")
}

// Using Portuguese keywords:
se (vida_jogador > 0 e tem_chave == true) entao {
    escrever("Porta destrancada! Avançando de nível.")
}

```

---

## 4. Comparison Operators Reference

The runtime evaluates conditions using standard comparison operators:

| Operator | Meaning | Example |
| --- | --- | --- |
| `==` | Equal to | `a == b` |
| `!=` | Not equal to | `a != b` |
| `>` | Greater than | `a > b` |
| `<` | Less than | `a < b` |
| `>=` | Greater than or equal to | `a >= b` |
| `<=` | Less than or equal to | `a <= b` |

```

---
