" Detecção e configuração base para arquivos .rudy
au BufRead,BufNewFile *.rudy setfiletype rudy

augroup rudy_settings
  autocmd!
  autocmd FileType rudy setlocal commentstring=//\ %s
  autocmd FileType rudy setlocal tabstop=4 shiftwidth=4 expandtab
augroup END
