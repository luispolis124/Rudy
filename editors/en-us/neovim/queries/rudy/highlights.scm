; Comentários
(comment) @comment

; Palavras-chave
[
  "action" "acao"
  "if" "se"
  "else" "senao"
  "while" "enquanto"
  "then" "entao"
  "var"
  "use" "usar"
] @keyword

; Funções nativas
[
  "write" "escrever"
  "ask" "ler"
  "random" "aleatorio"
  "sleep" "pausar"
  "save" "salvar"
  "load" "carregar"
  "clear" "limpar"
] @function.builtin

; Literais e Operadores
(string) @string
(number) @number
(identifier) @variable

[
  "==" "!=" ">=" "<=" ">" "<"
  "=" "+" "-" "*" "/"
] @operator

[ "(" ")" "{" "}" "," ] @punctuation.delimiter
