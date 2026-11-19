# Rudy Language Internal Classes Reference 🐺

This document details the core internal Python classes that power the **Rudy** interpreter engine (`src/rudy.py`), including the Abstract Syntax Tree (AST) nodes, the Parser, and the Runtime execution environment.

---

## 1. Abstract Syntax Tree (AST) Nodes

The AST breaks down source code into structured object nodes that the runtime can execute recursively.

### `NoAST`
* **Description:** Base abstract class for all AST nodes in the Rudy engine.

### `ProgramaNode`
* **Description:** Represents the root node of a Rudy script.
* **Attributes:** 
  * `declaracoes` (list): A collection of statements or function declarations contained in the program.

### `FuncaoNode`
* **Description:** Represents a user-defined function or action block (`action` / `acao`).
* **Attributes:**
  * `nome` (str): The identifier name of the function.
  * `corpo` (list): A list of command nodes executed when the function is called.

### `AtribuicaoNode`
* **Description:** Handles variable declarations and value assignments.
* **Attributes:**
  * `nome` (str): The name of the variable.
  * `expr` (str): The expression or value assigned to the variable.

### `EscreverNode`
* **Description:** Represents output operations (`write` / `escrever`).
* **Attributes:**
  * `conteudo` (str): The text or expression evaluated and printed to the terminal.

### `SalvarNode`
* **Description:** Represents file writing operations (`save` / `salvar`).
* **Attributes:**
  * `path` (str): The destination file path.
  * `conteudo` (str): The content written into the file.

### `LimparNode`
* **Description:** Represents terminal screen clearing (`clear` / `limpar`). Has no attributes.

### `SeNode`
* **Description:** Represents conditional branches (`if` / `se` / `else` / `senao`).
* **Attributes:**
  * `condicao` (str): The boolean condition to evaluate.
  * `bloco_entao` (list): Commands executed if the condition is true.
  * `bloco_senao` (list, optional): Commands executed if the condition is false.

### `EnquantoNode`
* **Description:** Represents repetition loops (`while` / `enquanto`).
* **Attributes:**
  * `condicao` (str): The loop continuation condition.
  * `bloco` (list): Commands executed repeatedly while the condition holds true.

---

## 2. Syntactic Analyzer (`Parser`)

### `Parser`
* **Description:** Processes lines of source code, strips comments, manages pointer positions, and builds the AST hierarchy.
* **Key Methods:**
  * `parse()`: Initiates parsing across the script lines, returning a `ProgramaNode`.
  * `parse_funcao()`: Parses action blocks and their inner scopes.
  * `parse_comando(linha)`: Evaluates individual lines and maps them to their respective AST node classes.

---

## 3. Execution Environment (`RudyRuntime`)

### `RudyRuntime`
* **Description:** The execution engine responsible for evaluating expressions, managing variable scopes, handling built-in functions, and walking through the AST nodes.
* **Key Methods:**
  * `avaliar_valor(expr)`: Evaluates literals, string concatenations, arithmetic operations, and built-in functions like `load()`, `ask()`, and `random()`.
  * `avaliar_condicao(cond)`: Evaluates logical expressions, comparison operators (`==`, `!=`, `>`, `<`), and logical operators (`and`, `or`).
  * `executar(no)`: Recursively walks the AST tree nodes and executes their runtime behavior.
