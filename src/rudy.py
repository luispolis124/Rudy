import sys
import os
import re
import random
import time
import subprocess

# --- 1. LER / ANALISADOR LÉXICO (LEXER) ---
TOKEN_TIPOS = [
    ('COMENTARIO', r'//.*'),
    ('PALAVRA_CHAVE', r'\b(action|acao|if|se|else|senao|while|enquanto|then|entao|var)\b'),
    ('FUNCAO', r'\b(write|escrever|ask|ler|random|aleatorio|sleep|pausar|save|salvar|load|carregar|clear|limpar)\b'),
    ('IDENTIFICADOR', r'[a-zA-Z_][a-zA-Z0-9_]*'),
    ('NUMERO', r'\b\d+\b'),
    ('STRING', r'"[^"]*"|\'[^\']*\''),
    ('OPERADOR_COMP', r'==|!=|>=|<=|>|<'),
    ('ATRIBUICAO', r'='),
    ('OPERADOR_MAT', r'[\+\-\*/]'),
    ('SIMBOLOS', r'[\(\)\{\},]'),
    ('ESPACO', r'[ \t\r\n]+'),
]

def lexer(codigo_fonte):
    tokens = []
    linha_num = 1
    
    padrao_regex = '|'.join(f'(?P<{nome>}>{padrao})' for nome, padrao in TOKEN_TIPOS)
    
    for match in re.finditer(padrao_regex, codigo_fonte):
        tipo = match.lastgroup
        valor = match.group(tipo)
        
        if tipo == 'ESPACO':
            linha_num += valor.count('\n')
            continue
        elif tipo == 'COMENTARIO':
            continue
        elif tipo is not None:
            tokens.append((tipo, valor, linha_num))
        else:
            raise SyntaxError(f"Erro léxico desconhecido na linha {linha_num}: {valor}")
            
    return tokens


# --- 2. ANALISADOR SINTÁTICO (PARSER) ---
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def token_atual(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return ('EOF', 'EOF', -1)

    def consumir(self, tipo_esperado=None):
        tok = self.token_atual()
        if tipo_esperado and tok[0] != tipo_esperado and tok[1] != tipo_esperado:
            raise SyntaxError(f"Erro de sintaxe na linha {tok[2]}: Esperado '{tipo_esperado}', encontrado '{tok[1]}'")
        self.pos += 1
        return tok

    def parse(self):
        arvore = []
        while self.token_atual()[0] != 'EOF':
            tok = self.token_atual()
            if tok[1] in ('action', 'acao'):
                arvore.append(self.parse_funcao())
            else:
                self.pos += 1
        return arvore

    def parse_funcao(self):
        self.consumir() # action ou acao
        nome = self.consumir('IDENTIFICADOR')[1]
        self.consumir('(')
        self.consumir(')')
        self.consumir('{')
        return ("FUNCAO", nome)


# --- 3. AMBIENTE DE EXECUÇÃO (RUNTIME) ---
class RudyRuntime:
    def __init__(self):
        self.variaveis = {}

    def avaliar_valor(self, expr):
        expr = expr.strip()

        if (expr.startswith("load(") or expr.startswith("carregar(")) and expr.endswith(")"):
            idx = expr.index("(")
            path = self.avaliar_valor(expr[idx+1:-1])
            if os.path.exists(str(path)):
                with open(str(path), 'r', encoding='utf-8') as f:
                    return f.read()
            return ""

        if (expr.startswith("sleep(") or expr.startswith("pausar(")) and expr.endswith(")"):
            idx = expr.index("(")
            tempo = float(self.avaliar_valor(expr[idx+1:-1]))
            time.sleep(tempo)
            return 0

        if (expr.startswith("ask(") or expr.startswith("ler(")) and expr.endswith(")"):
            idx = expr.index("(")
            prompt_expr = expr[idx+1:-1]
            prompt = self.avaliar_valor(prompt_expr)
            return input(str(prompt))

        if (expr.startswith("random(") or expr.startswith("aleatorio(")) and expr.endswith(")"):
            idx = expr.index("(")
            args = expr[idx+1:-1].split(",")
            min_v = int(self.avaliar_valor(args[0]))
            max_v = int(self.avaliar_valor(args[1]))
            return random.randint(min_v, max_v)

        if '"' in expr or "'" in expr:
            partes = expr.split('+')
            resultado = ""
            for p in partes:
                p = p.strip()
                if (p.startswith('"') and p.endswith('"')) or (p.startswith("'") and p.endswith("'")):
                    resultado += p[1:-1]
                elif p in self.variaveis:
                    resultado += str(self.variaveis[p])
                else:
                    resultado += p
            return resultado

        for op in ['+', '-', '*', '/']:
            if op in expr:
                esq, dir_ = expr.split(op, 1)
                v1 = int(self.avaliar_valor(esq))
                v2 = int(self.avaliar_valor(dir_))
                if op == '+': return v1 + v2
                if op == '-': return v1 - v2
                if op == '*': return v1 * v2
                if op == '/': return v1 // v2

        if expr in self.variaveis:
            return self.variaveis[expr]
        if expr.isdigit() or (expr.startswith('-') and expr[1:].isdigit()):
            return int(expr)
        return expr

    def avaliar_condicao(self, cond):
        if " and " in cond or " e " in cond:
            separador = " and " if " and " in cond else " e "
            partes = cond.split(separador)
            return all(self.avaliar_condicao(p) for p in partes)
        if " or " in cond or " ou " in cond:
            separador = " or " if " or " in cond else " ou "
            partes = cond.split(separador)
            return any(self.avaliar_condicao(p) for p in partes)

        for op in ['==', '!=', '>=', '<=', '>', '<']:
            if op in cond:
                esq, dir_ = cond.split(op, 1)
                v1 = self.avaliar_valor(esq.strip())
                v2 = self.avaliar_valor(dir_.strip())
                if op == '==': return str(v1) == str(v2)
                if op == '!=': return str(v1) != str(v2)
                if op == '>':  return int(v1) > int(v2)
                if op == '<':  return int(v1) < int(v2)
                if op == '>=': return int(v1) >= int(v2)
                if op == '<=': return int(v1) <= int(v2)
        return False

    def encontrar_fim_bloco(self, linhas, inicio):
        nivel = 0
        for i in range(inicio, len(linhas)):
            l = linhas[i].strip()
            if l.endswith("{"):
                nivel += 1
            if l == "}":
                nivel -= 1
                if nivel == 0:
                    return i
        return len(linhas) - 1

    def executar_bloco(self, linhas, inicio, fim):
        i = inicio
        while i <= fim:
            linha = linhas[i].strip()

            if not linha or linha.startswith("//") or linha == "}":
                i += 1
                continue

            if linha == "clear()" or linha == "limpar()":
                os.system('cls' if os.name == 'nt' else 'clear')
                i += 1
                continue

            if (linha.startswith("action ") or linha.startswith("acao ")) and linha.endswith("{"):
                i += 1
                continue

            if (linha.startswith("while") or linha.startswith("enquanto")) and linha.endswith("{"):
                match = re.search(r'(?:while|enquanto)\s*\((.*?)\)\s*\{', linha)
                fim_bloco = self.encontrar_fim_bloco(linhas, i)
                if match:
                    cond = match.group(1)
                    while self.avaliar_condicao(cond):
                        self.executar_bloco(linhas, i + 1, fim_bloco - 1)
                i = fim_bloco + 1
                continue

            if (linha.startswith("if") or linha.startswith("se")) and ("then" in linha or "entao" in linha) and linha.endswith("{"):
                match = re.search(r'(?:if|se)\s*\((.*?)\)\s*(?:then|entao)', linha)
                fim_if = self.encontrar_fim_bloco(linhas, i)
                
                condicao_atendida = False
                if match and self.avaliar_condicao(match.group(1)):
                    condicao_atendida = True
                    self.executar_bloco(linhas, i + 1, fim_if - 1)
                
                proxima_linha_idx = fim_if + 1
                if proxima_linha_idx < len(linhas):
                    prox_linha = linhas[proxima_linha_idx].strip()
                    if prox_linha.startswith("else") or prox_linha.startswith("senao"):
                        fim_else = self.encontrar_fim_bloco(linhas, proxima_linha_idx)
                        if not condicao_atendida:
                            self.executar_bloco(linhas, proxima_linha_idx + 1, fim_else - 1)
                        i = fim_else + 1
                        continue

                i = fim_if + 1
                continue

            if (linha.startswith("save(") or linha.startswith("salvar(")) and linha.endswith(")"):
                idx = linha.index("(")
                args_str = linha[idx+1:-1]
                partes = args_str.split(",", 1)
                if len(partes) == 2:
                    path = self.avaliar_valor(partes[0].strip())
                    conteudo = self.avaliar_valor(partes[1].strip())
                    with open(str(path), 'w', encoding='utf-8') as f:
                        f.write(str(conteudo))
                i += 1
                continue

            if (linha.startswith("write(") or linha.startswith("escrever(")) and linha.endswith(")"):
                idx = linha.index("(")
                conteudo = linha[idx+1:-1]
                print(self.avaliar_valor(conteudo))
                i += 1
                continue

            limpa_linha = linha
            if limpa_linha.startswith("var "):
                limpa_linha = limpa_linha[4:].strip()

            if "=" in limpa_linha and not limpa_linha.startswith("if") and not limpa_linha.startswith("while") and not limpa_linha.startswith("se") and not limpa_linha.startswith("enquanto") and not limpa_linha.startswith("else") and not limpa_linha.startswith("senao"):
                nome, expr = limpa_linha.split("=", 1)
                self.variaveis[nome.strip()] = self.avaliar_valor(expr.strip())
                i += 1
                continue

            print(f"Erro de sintaxe na linha {i+1}: {linha}")
            i += 1


# --- 4. COMPILADOR / EMPACOTADOR STANDALONE (.EXE) ---
def compilar_para_executavel(arquivo_path):
    print(f"--- [Rudy Compiler] Empacotando '{arquivo_path}' para Executável (.exe) ---")
    
    # Valida se o PyInstaller está disponível no ambiente (PC ou Termux)
    try:
        import PyInstaller
    except ImportError:
        print("Aviso: O PyInstaller não está instalado. Instalando automaticamente via pip...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])

    # Cria um script temporário em Python que embute o interpretador e o código Rudy
    with open(arquivo_path, 'r', encoding='utf-8') as f:
        codigo_rudy = f.read()

    stub_code = f'''
import sys
import os
import re
import random
import time

# Código Rudy embarcado embutido no executável standalone
CODIGO_EMBARCADO = """{codigo_rudy}"""

# [Runtime embutido para o binário]
TOKEN_TIPOS = [
    ('COMENTARIO', r'//.*'),
    ('PALAVRA_CHAVE', r'\\b(action|acao|if|se|else|senao|while|enquanto|then|entao|var)\\b'),
    ('FUNCAO', r'\\b(write|escrever|ask|ler|random|aleatorio|sleep|pausar|save|salvar|load|carregar|clear|limpar)\\b'),
    ('IDENTIFICADOR', r'[a-zA-Z_][a-zA-Z0-9_]*'),
    ('NUMERO', r'\\b\\d+\\b'),
    ('STRING', r'"[^"]*"|\'[^\']*\''),
    ('OPERADOR_COMP', r'==|!=|>=|<=|>|<'),
    ('ATRIBUICAO', r'='),
    ('OPERADOR_MAT', r'[\\+\\-\\*/]'),
    ('SIMBOLOS', r'[\\(\\\)\\{\\\},]'),
    ('ESPACO', r'[ \\t\\r\\n]+'),
]

class RudyRuntime:
    def __init__(self):
        self.variaveis = {{}}

    def avaliar_valor(self, expr):
        expr = expr.strip()
        if (expr.startswith("load(") or expr.startswith("carregar(")) and expr.endswith(")"):
            idx = expr.index("(")
            path = self.avaliar_valor(expr[idx+1:-1])
            if os.path.exists(str(path)):
                with open(str(path), 'r', encoding='utf-8') as f:
                    return f.read()
            return ""
        if (expr.startswith("sleep(") or expr.startswith("pausar(")) and expr.endswith(")"):
            idx = expr.index("(")
            tempo = float(self.avaliar_valor(expr[idx+1:-1]))
            time.sleep(tempo)
            return 0
        if (expr.startswith("ask(") or expr.startswith("ler(")) and expr.endswith(")"):
            idx = expr.index("(")
            prompt_expr = expr[idx+1:-1]
            prompt = self.avaliar_valor(prompt_expr)
            return input(str(prompt))
        if (expr.startswith("random(") or expr.startswith("aleatorio(")) and expr.endswith(")"):
            idx = expr.index("(")
            args = expr[idx+1:-1].split(",")
            min_v = int(self.avaliar_valor(args[0]))
            max_v = int(self.avaliar_valor(args[1]))
            return random.randint(min_v, max_v)
        if '"' in expr or "'" in expr:
            partes = expr.split('+')
            resultado = ""
            for p in partes:
                p = p.strip()
                if (p.startswith('"') and p.endswith('"')) or (p.startswith("'") and p.endswith("'")):
                    resultado += p[1:-1]
                elif p in self.variaveis:
                    resultado += str(self.variaveis[p])
                else:
                    resultado += p
            return resultado
        for op in ['+', '-', '*', '/']:
            if op in expr:
                esq, dir_ = expr.split(op, 1)
                v1 = int(self.avaliar_valor(esq))
                v2 = int(self.avaliar_valor(dir_))
                if op == '+': return v1 + v2
                if op == '-': return v1 - v2
                if op == '*': return v1 * v2
                if op == '/': return v1 // v2
        if expr in self.variaveis:
            return self.variaveis[expr]
        if expr.isdigit() or (expr.startswith('-') and expr[1:].isdigit()):
            return int(expr)
        return expr

    def avaliar_condicao(self, cond):
        if " and " in cond or " e " in cond:
            separador = " and " if " and " in cond else " e "
            partes = cond.split(separador)
            return all(self.avaliar_condicao(p) for p in partes)
        if " or " in cond or " ou " in cond:
            separador = " or " if " or " in cond else " ou "
            partes = cond.split(separador)
            return any(self.avaliar_condicao(p) for p in partes)
        for op in ['==', '!=', '>=', '<=', '>', '<']:
            if op in cond:
                esq, dir_ = cond.split(op, 1)
                v1 = self.avaliar_valor(esq.strip())
                v2 = self.avaliar_valor(dir_.strip())
                if op == '==': return str(v1) == str(v2)
                if op == '!=': return str(v1) != str(v2)
                if op == '>':  return int(v1) > int(v2)
                if op == '<':  return int(v1) < int(v2)
                if op == '>=': return int(v1) >= int(v2)
                if op == '<=': return int(v1) <= int(v2)
        return False

    def encontrar_fim_bloco(self, linhas, inicio):
        nivel = 0
        for i in range(inicio, len(linhas)):
            l = linhas[i].strip()
            if l.endswith("{{"):
                nivel += 1
            if l == "}}":
                nivel -= 1
                if nivel == 0:
                    return i
        return len(linhas) - 1

    def executar_bloco(self, linhas, inicio, fim):
        i = inicio
        while i <= fim:
            linha = linhas[i].strip()
            if not linha or linha.startswith("//") or linha == "}}":
                i += 1
                continue
            if linha == "clear()" or linha == "limpar()":
                os.system('cls' if os.name == 'nt' else 'clear')
                i += 1
                continue
            if (linha.startswith("action ") or linha.startswith("acao ")) and linha.endswith("{{"):
                i += 1
                continue
            if (linha.startswith("while") or linha.startswith("enquanto")) and linha.endswith("{{"):
                match = re.search(r'(?:while|enquanto)\\s*\\((.*?)\\)\\s*\\{{', linha)
                fim_bloco = self.encontrar_fim_bloco(linhas, i)
                if match:
                    cond = match.group(1)
                    while self.avaliar_condicao(cond):
                        self.executar_bloco(linhas, i + 1, fim_bloco - 1)
                i = fim_bloco + 1
                continue
            if (linha.startswith("if") or linha.startswith("se")) and ("then" in linha or "entao" in linha) and linha.endswith("{{"):
                match = re.search(r'(?:if|se)\\s*\\((.*?)\\)\\s*(?:then|entao)', linha)
                fim_if = self.encontrar_fim_bloco(linhas, i)
                condicao_atendida = False
                if match and self.avaliar_condicao(match.group(1)):
                    condicao_atendida = True
                    self.executar_bloco(linhas, i + 1, fim_if - 1)
                proxima_linha_idx = fim_if + 1
                if proxima_linha_idx < len(linhas):
                    prox_linha = linhas[proxima_linha_idx].strip()
                    if prox_linha.startswith("else") or prox_linha.startswith("senao"):
                        fim_else = self.encontrar_fim_bloco(linhas, proxima_linha_idx)
                        if not condicao_atendida:
                            self.executar_bloco(linhas, proxima_linha_idx + 1, fim_else - 1)
                        i = fim_else + 1
                        continue
                i = fim_if + 1
                continue
            if (linha.startswith("save(") or linha.startswith("salvar(")) and linha.endswith(")"):
                idx = linha.index("(")
                args_str = linha[idx+1:-1]
                partes = args_str.split(",", 1)
                if len(partes) == 2:
                    path = self.avaliar_valor(partes[0].strip())
                    conteudo = self.avaliar_valor(partes[1].strip())
                    with open(str(path), 'w', encoding='utf-8') as f:
                        f.write(str(conteudo))
                i += 1
                continue
            if (linha.startswith("write(") or linha.startswith("escrever(")) and linha.endswith(")"):
                idx = linha.index("(")
                conteudo = linha[idx+1:-1]
                print(self.avaliar_valor(conteudo))
                i += 1
                continue
            limpa_linha = linha
            if limpa_linha.startswith("var "):
                limpa_linha = limpa_linha[4:].strip()
            if "=" in limpa_linha and not limpa_linha.startswith("if") and not limpa_linha.startswith("while") and not limpa_linha.startswith("se") and not limpa_linha.startswith("enquanto") and not limpa_linha.startswith("else") and not limpa_linha.startswith("senao"):
                nome, expr = limpa_linha.split("=", 1)
                self.variaveis[nome.strip()] = self.avaliar_valor(expr.strip())
                i += 1
                continue
            i += 1

if __name__ == "__main__":
    runtime = RudyRuntime()
    linhas = CODIGO_EMBARCADO.split('\\n')
    runtime.executar_bloco(linhas, 0, len(linhas) - 1)
'''

    stub_filename = "rudy_temp_stub.py"
    with open(stub_filename, 'w', encoding='utf-8') as f:
        f.write(stub_code)

    base_nome = os.path.splitext(os.path.basename(arquivo_path))[0]
    
    # Executa o PyInstaller para gerar o executável standalone (--onefile)
    print(f"Gerando executável standalone para '{base_nome}'...")
    subprocess.check_call([sys.executable, "-m", "PyInstaller", "--onefile", "--noconsole", stub_filename])
    
    # Limpeza dos arquivos temporários de compilação
    if os.path.exists(stub_filename):
        os.remove(stub_filename)
        
    print(f"\n[Sucesso!] Executável gerado na pasta 'dist/' para o programa '{base_nome}'.")


# --- 5. FUNÇÃO PRINCIPAL ---
def main():
    if len(sys.argv) < 2:
        print("Uso: python src/rudy.py <arquivo.rudy> [--build / --compilar]")
        return
        
    arquivo_path = sys.argv[1]
    if not os.path.exists(arquivo_path):
        print(f"Erro: Arquivo '{arquivo_path}' não encontrado.")
        return
        
    # Verifica se o usuário pediu para compilar para executável
    if len(sys.argv) >= 3 and sys.argv[2] in ('--build', '--compilar', 'build'):
        compilar_para_executavel(arquivo_path)
        return

    with open(arquivo_path, 'r', encoding='utf-8') as f:
        codigo_fonte = f.read()
        
    print(f"--- Compilando e Executando {arquivo_path} com a Rudy ---")
    
    tokens = lexer(codigo_fonte)
    parser = Parser(tokens)
    parser.parse()
    
    runtime = RudyRuntime()
    linhas = codigo_fonte.split('\n')
    runtime.executar_bloco(linhas, 0, len(linhas) - 1)

if __name__ == "__main__":
    main()
