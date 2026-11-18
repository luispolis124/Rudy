# Rudy Language Error Reference 🐺

This document lists the standard error messages, syntax warnings, and lexical exceptions that can be thrown by the **Rudy** interpreter (`src/rudy.py`) during development or script execution.

---

## 1. Lexical Errors

### `Lexical error unknown on line {line}: {token}`
* **Cause:** The Lexer encountered a character, symbol, or token pattern that does not match any valid definition in the language grammar (such as unrecognized symbols or illegal characters outside strings/comments).
* **Fix:** Check the specified line number in your `.rudy` script and remove or correct the invalid character.

---

## 2. Syntax Errors

### `Syntax error on line {line}: Expected '{expected}', found '{found}'`
* **Cause:** The Parser expected a specific syntactic token (like a parenthesis `(`, closing brace `}`, or comma `,`), but encountered something else.
* **Fix:** Ensure all open brackets, parentheses, and code blocks `{}` are properly closed.

### `Syntax error in function definition: {line}`
* **Cause:** A function or action declaration was written incorrectly (e.g., missing parentheses `()`, a missing function name, or forgetting the opening brace `{`).
* **Fix:** Verify your function declarations follow the correct format:
  ```rudy
  action my_function() {
      // code here
  }

```

*(Or using Portuguese keywords: `acao minha_funcao() { ... }`)*

### `Syntax error in repetition syntax: {line}`

* **Cause:** A `while` or `enquanto` loop header was malformed, typically missing parentheses around the condition or missing the opening brace `{`.
* **Fix:** Ensure loops are structured correctly:
```rudy
while (condition) {
    // code here
}

```



### `Syntax error in conditional syntax: {line}`

* **Cause:** An `if` or `se` statement was written without proper syntax structure, such as missing the condition parentheses or omitting the `then` / `entao` keyword before the block.
* **Fix:** Ensure conditionals follow the proper bilingual syntax:
```rudy
if (score > 10) then {
    write("Winner!")
}

```


*(Or: `se (pontos > 10) entao { ... }`)*

---

## 3. Runtime & Execution Errors

### Unhandled Variable or Undefined Reference

* **Cause:** Trying to use a variable or identifier in an expression or mathematical operation before it has been declared with `var`.
* **Fix:** Declare the variable beforehand:
```rudy
var score = 0
score = score + 1

```



### File Not Found Warnings (`load()` / `carregar()`)

* **Cause:** The `load()` or `carregar()` function tried to read a file path that does not exist on disk.
* **Fix:** Ensure the target file exists in the correct directory relative to where the script is being executed, or verify the file path string.

```

---
