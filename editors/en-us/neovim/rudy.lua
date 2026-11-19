-- Configuração oficial da linguagem Rudy para Neovim (Lua)
vim.filetype.add({
  extension = {
    rudy = "rudy",
  },
})

vim.api.nvim_create_autocmd("FileType", {
  pattern = "rudy",
  callback = function()
    vim.bo.commentstring = "// %s"
    vim.bo.tabstop = 4
    vim.bo.shiftwidth = 4
    vim.bo.expandtab = true
  end,
})
