# Rudy Language Tutorial: Building Your First Script 🐺

Welcome to the official **Rudy** tutorial! In this guide, you will learn how to write, execute, and compile your very first script using Rudy's lightweight bilingual (PT/EN) syntax.

---

## Step 1: Setting Up Your Workspace

Ensure your repository structure is clean and organized, with your core engine in `src/rudy.py` and your test scripts inside an `examples/` directory:

```text
Rudy/
├── src/
│   └── rudy.py
├── examples/
│   └── first_game.rudy
└── docs/
    └── TUTORIAL.md

```

---

## Step 2: Writing Your First Rudy Script

Create a new file named `examples/first_game.rudy` and open it in your text editor (or via Termux on mobile). Let's build a simple interactive ASCII greeting script:

```rudy
// My First Rudy Script / Meu Primeiro Script em Rudy

clear()
write("========================================")
write("   WELCOME TO THE RUDY LANGUAGE! 🐺     ")
write("========================================")

// Ask for user input
var player_name = ask("What is your name? / Qual o seu nome? ")

write("Hello, " + player_name + "! Let's test your luck.")

// Generate a random number between 1 and 6
var lucky_number = random(1, 6)
write("Your generated lucky number is: " + lucky_number)

// Conditional check
if (lucky_number >= 4) then {
    write("Fantastic! You got a high roll! 🌟")
} else {
    write("Not bad! Try again for a higher roll. 🎲")
}

```

---

## Step 3: Running Your Script

To execute your script using the Python-based AST interpreter, run the following command in your terminal or Termux environment:

```bash
python src/rudy.py examples/first_game.rudy

```

You will see the output appear on your screen instantly, along with the precise execution benchmark timer in milliseconds (`ms`) at the end!

---

## Step 4: Compiling to a Standalone Executable

If you want to package your `.rudy` script into a standalone binary executable using PyInstaller (`--build`), run:

```bash
python src/rudy.py examples/first_game.rudy --build

```

The compiled standalone executable will be automatically generated inside the `dist/` folder, ready to run anywhere without requiring external script files!

---

## Next Steps

Now that you've mastered the basics, explore the other documentation guides to level up your Rudy projects:

* Check out [SYNTAX.md](https://www.google.com/search?q=./SYNTAX.md) for grammar rules.
* Explore [FUNCTIONS.md](https://www.google.com/search?q=./FUNCTIONS.md) for available built-in commands.
* Learn about [CONTROL_FLOW.md](https://www.google.com/search?q=./CONTROL_FLOW.md) for loops and conditionals.

```

---
