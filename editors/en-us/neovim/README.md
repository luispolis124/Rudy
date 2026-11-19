# 🐺 Neovim Support for the Rudy Programming Language

Official filetype detection, indentation, and bilingual (Portuguese/English) syntax highlighting support for `.rudy` files in **Neovim**.

## 📦 Manual Installation (Linux / macOS / Termux)

1. Copy the configuration files into your Neovim directory (`~/.config/nvim/`):

```bash
mkdir -p ~/.config/nvim/plugin ~/.config/nvim/syntax ~/.config/nvim/queries/rudy
cp rudy.lua ~/.config/nvim/plugin/rudy.lua
cp syntax/rudy.vim ~/.config/nvim/syntax/rudy.vim
cp queries/rudy/highlights.scm ~/.config/nvim/queries/rudy/highlights.scm

 * Open any .rudy script in Neovim:
nvim examples/masmorra.rudy

🔌 Installation via Lazy.nvim
Add the Rudy repository to your plugin list pointing to the editors/neovim subdirectory:
{
  "luispolis124/Rudy",
  rtp = "editors/neovim",
  ft = "rudy",
}

