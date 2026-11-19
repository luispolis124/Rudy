# Rudy

Rudy is a lightweight, bilingual programming language built with Python and an abstract syntax tree interpreter. It supports English and Portuguese syntax and runs on Windows, Linux, macOS, and Termux.

## English (United States) Guide

See [the full documentation](docs/en-us/README.md), [the tutorial](docs/en-us/TUTORIAL.md), and [editor setup](editors/en-us/README.md).

## Quick Start

```bash
python src/rudy.py examples/en-us/example.rudy
python src/rudy.py examples/en-us/example.rudy --build
python src/rudy.py --repl
```

Select localized interpreter messages with `--locale=en-us`, `--locale=en-uk`, or `RUDY_LOCALE=en-us`.

## Locale Packages

- `en-us`: American English output and CLI messages
- `en-uk`: British English output and CLI messages
- Existing Portuguese keywords remain supported
