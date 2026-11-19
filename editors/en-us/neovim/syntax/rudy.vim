if exists("b:current_syntax")
  finish
endif

" Comentários
syn match rudyComment "//.*$"

" Palavras-chave (PT/EN)
syn keyword rudyKeyword action acao if se else senao while enquanto then entao var use usar

" Funções nativas da Standard Library
syn keyword rudyFunction write escrever ask ler random aleatorio sleep pausar save salvar load carregar clear limpar

" Strings
syn region rudyString start=+"+ skip=+\\"+ end=+"+
syn region rudyString start=+'+ skip=+\\'+ end=+'+

" Números
syn match rudyNumber "\<\d\+\>"

" Operadores e delimitadores
syn match rudyOperator "\(==\|!=\|>=\|<=\|>\|<\|=\|+\|-\|\*\|/\)"
syn match rudyDelimiter "[\(\)\{\},]"

" Vinculação de cores do tema
hi def link rudyComment   Comment
hi def link rudyKeyword   Keyword
hi def link rudyFunction  Function
hi def link rudyString    String
hi def link rudyNumber    Number
hi def link rudyOperator  Operator
hi def link rudyDelimiter Delimiter

let b:current_syntax = "rudy"
