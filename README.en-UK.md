# Rudy

Rudy is a lightweight, bilingual programming language built with Python and an abstract syntax tree interpreter. It supports English and Portuguese syntax and runs on Windows, Linux, macOS and Termux.

## English (United Kingdom) Guide

See [the full documentation](docs/en-uk/README.md), [the tutorial](docs/en-uk/TUTORIAL.md), and [editor setup](editors/en-uk/README.md).

## Quick Start

```bash
python src/rudy.py examples/en-uk/example.rudy
python src/rudy.py examples/en-uk/example.rudy --build
python src/rudy.py --repl
```

Select localised interpreter messages with `--locale=en-us`, `--locale=en-uk`, or `RUDY_LOCALE=en-uk`.

## Locale Packages

- `en-us`: American English output and CLI messages
- `en-uk`: British English output and CLI messages
- Existing Portuguese keywords remain supported
