import sys
import os
import re
import random
import time
import subprocess
import urllib.request
import marshal
from typing import Any, Union

RudyValor = Union[str, int, float]

LOCALES_SUPORTADOS = ("en-us", "en-uk")


def obter_localidade():
    for arg in sys.argv[1:]:
        if arg.startswith("--locale="):
            locale = arg.split("=", 1)[1].strip().lower()
            if locale in LOCALES_SUPORTADOS:
                return locale
        if arg in ("--en-us", "--usa", "en-us"):
            return "en-us"
        if arg in ("--en-uk", "--uk", "en-uk"):
            return "en-uk"

    locale = os.environ.get("RUDY_LOCALE", "en-us").strip().lower()
    return locale if locale in LOCALES_SUPORTADOS else "en-us"


LOCALIDADE = obter_localidade()

MENSAGENS = {
    "en-us": {
        "unknown_character": "Unknown lexical character on line",
        "package_missing": "Warning: Library '{pkg}' not found in the stdlib/ folder. Run 'python src/rudy.py install {pkg}'.",
        "function_syntax": "Syntax error in function definition",
        "loop_syntax": "Syntax error in loop",
        "if_syntax": "Syntax error in conditional",
        "unknown_command": "Unknown command",
        "input_interrupted": "Input interrupted by the user.",
        "package_install": "--- [Rudy Package Manager] Installing library '{pkg}' ---",
        "download": "Downloading from",
        "installed": "Package '{pkg}' installed successfully in 'stdlib/{file}'.",
        "download_error": "Error downloading package '{pkg}'",
        "fallback": "Created local fallback package in '{dest}'.",
        "fallback_comment": "// Standard library installed locally",
        "fallback_loaded": "Library {pkg} loaded successfully!",
        "bytecode_compile": "--- [Rudy Bytecode Engine] Compiling '{file}' to optimized bytecode ---",
        "bytecode_success": "Bytecode generated and compressed in '{file}'",
        "execution_time": "Execution time",
        "repl_title": "Rudy Interactive Shell (v1.0 - Bilingual PT/EN)",
        "repl_help": "Enter Rudy commands or 'sair' / 'exit' to close.",
        "repl_bye": "Goodbye!",
        "repl_interrupt": "Use 'sair' or 'exit' to close the shell.",
        "rudy_error": "[Rudy Error]",
        "compiler": "--- [Rudy Compiler] Packaging '{file}' as a standalone executable (.exe) ---",
        "pyinstaller_missing": "Warning: PyInstaller is not installed. Installing automatically with pip...",
        "generating": "Generating standalone executable for",
        "success_exe": "Executable generated in the 'dist/' folder",
        "missing_arg": "Error: Specify a package name or library URL.",
        "file_missing": "Error: File '{file}' was not found.",
        "bytecode_running": "Running through the Rudy Bytecode Virtual Machine...",
        "benchmark": "Rudy Benchmark",
        "total_time": "Total time",
        "ast_running": "Compiling and running {file} with Rudy (AST Engine)",
    },
    "en-uk": {
        "unknown_character": "Unknown lexical character on line",
        "package_missing": "Warning: Library '{pkg}' not found in the stdlib/ folder. Run 'python src/rudy.py install {pkg}'.",
        "function_syntax": "Syntax error in function definition",
        "loop_syntax": "Syntax error in loop",
        "if_syntax": "Syntax error in conditional",
        "unknown_command": "Unknown command",
        "input_interrupted": "Input interrupted by the user.",
        "package_install": "--- [Rudy Package Manager] Installing library '{pkg}' ---",
        "download": "Downloading from",
        "installed": "Package '{pkg}' installed successfully in 'stdlib/{file}'.",
        "download_error": "Error downloading package '{pkg}'",
        "fallback": "Created local fallback package in '{dest}'.",
        "fallback_comment": "// Standard library installed locally",
        "fallback_loaded": "Library {pkg} loaded successfully!",
        "bytecode_compile": "--- [Rudy Bytecode Engine] Compiling '{file}' to optimised bytecode ---",
        "bytecode_success": "Bytecode generated and compressed in '{file}'",
        "execution_time": "Execution time",
        "repl_title": "Rudy Interactive Shell (v1.0 - Bilingual PT/EN)",
        "repl_help": "Enter Rudy commands or 'exit' / 'sair' to close.",
        "repl_bye": "Goodbye!",
        "repl_interrupt": "Use 'exit' or 'sair' to close the shell.",
        "rudy_error": "[Rudy Error]",
        "compiler": "--- [Rudy Compiler] Packaging '{file}' as a standalone executable (.exe) ---",
        "pyinstaller_missing": "Warning: PyInstaller is not installed. Installing automatically with pip...",
        "generating": "Generating standalone executable for",
        "success_exe": "Executable generated in the 'dist/' folder",
        "missing_arg": "Error: Specify a package name or library URL.",
        "file_missing": "Error: File '{file}' was not found.",
        "bytecode_running": "Running through the Rudy Bytecode Virtual Machine...",
        "benchmark": "Rudy Benchmark",
        "total_time": "Total time",
        "ast_running": "Compiling and running {file} with Rudy (AST Engine)",
    },
}


def mensagem(chave, **valores):
    return MENSAGENS[LOCALIDADE][chave].format(**valores)


# --- 1. LER / ANALISADOR LÉXICO (LEXER) ---
TOKEN_TIPOS = [
    ('COMENTARIO', r'//.*'),
    ('PALAVRA_CHAVE', r'\b(action|acao|if|se|else|senao|while|enquanto|then|entao|var|use|usar)\b'),
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
    
    padrao_regex = '|'.join(f'(?P<{nome}>{padrao})' for nome, padrao in TOKEN_TIPOS)
    
    for match in re.finditer(padrao_regex, codigo_fonte):
        tipo = match.lastgroup
        if tipo is None:
            raise SyntaxError(f"{mensagem('unknown_character')} {linha_num}: {match.group(0)}")
        valor = match.group(tipo)
        
        if tipo == 'ESPACO':
            linha_num += valor.count('\n')
            continue
        elif tipo == 'COMENTARIO':
            continue
        tokens.append((tipo, valor, linha_num))
            
    return tokens


# --- 2. NÓS DA ÁRVORE DE SINTAXE ABSTRATA (AST) ---
class NoAST:
    pass

class ProgramaNode(NoAST):
    def __init__(self, declaracoes):
        self.declaracoes = declaracoes

class FuncaoNode(NoAST):
    def __init__(self, nome, corpo):
        self.nome = nome
        self.corpo = corpo

class AtribuicaoNode(NoAST):
    def __init__(self, nome, expr):
        self.nome = nome
        self.expr = expr

class EscreverNode(NoAST):
    def __init__(self, conteudo):
        self.conteudo = conteudo

class SalvarNode(NoAST):
    def __init__(self, path, conteudo):
        self.path = path
        self.conteudo = conteudo

class LimparNode(NoAST):
    pass

class SeNode(NoAST):
    def __init__(self, condicao, bloco_entao, bloco_senao=None):
        self.condicao = condicao
        self.bloco_entao = bloco_entao
        self.bloco_senao = bloco_senao

class EnquantoNode(NoAST):
    def __init__(self, condicao, bloco):
        self.condicao = condicao
        self.bloco = bloco


# --- 3. ANALISADOR SINTÁTICO (PARSER COM AST) ---
class Parser:
    def __init__(self, linhas):
        self.linhas = [l.strip() for l in linhas if l.strip() and not l.strip().startswith("//")]
        self.pos = 0

    def linha_atual(self):
        if self.pos < len(self.linhas):
            return self.linhas[self.pos]
        return None

    def parse(self):
        declaracoes = []
        while self.pos < len(self.linhas):
            linha = self.linha_atual()
            if linha is None:
                break
            
            # Tratamento de importação de pacotes (use / usar)
            if linha.startswith("use ") or linha.startswith("usar "):
                match = re.search(r'(?:use|usar)\s+([a-zA-Z_][a-zA-Z0-9_]*)', linha)
                if match:
                    pkg_nome = match.group(1)
                    pkg_path = os.path.join("stdlib", f"{pkg_nome}.rudy")
                    if os.path.exists(pkg_path):
                        with open(pkg_path, 'r', encoding='utf-8') as f:
                            sub_codigo = f.read()
                        sub_parser = Parser(sub_codigo.split('\n'))
                        sub_ast = sub_parser.parse()
                        declaracoes.extend(sub_ast.declaracoes)
                    else:
                        print(mensagem("package_missing", pkg=pkg_nome))
                self.pos += 1
                continue

            if (linha.startswith("action ") or linha.startswith("acao ")) and linha.endswith("{"):
                declaracoes.append(self.parse_funcao())
            else:
                declaracoes.append(self.parse_comando(linha))
                self.pos += 1
                
        return ProgramaNode(declaracoes)

    def parse_funcao(self):
        linha = self.linhas[self.pos]
        match = re.search(r'(?:action|acao)\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\(\s*\)\s*\{', linha)
        if not match:
            raise SyntaxError(f"{mensagem('function_syntax')}: {linha}")
        nome = match.group(1)
        self.pos += 1
        
        corpo = []
        nivel = 1
        while self.pos < len(self.linhas):
            l = self.linhas[self.pos]
            if l.endswith("{"):
                nivel += 1
            if l == "}":
                nivel -= 1
                if nivel == 0:
                    self.pos += 1
                    break
            corpo.append(self.parse_comando(l))
            self.pos += 1
            
        return FuncaoNode(nome, corpo)

    def parse_comando(self, linha):
        if linha == "clear()" or linha == "limpar()":
            return LimparNode()

        if (linha.startswith("write(") or linha.startswith("escrever(")) and linha.endswith(")"):
            idx = linha.index("(")
            conteudo = linha[idx+1:-1].strip()
            return EscreverNode(conteudo)

        if (linha.startswith("save(") or linha.startswith("salvar(")) and linha.endswith(")"):
            idx = linha.index("(")
            args = linha[idx+1:-1].split(",", 1)
            if len(args) == 2:
                return SalvarNode(args[0].strip(), args[1].strip())

        if (linha.startswith("while") or linha.startswith("enquanto")) and linha.endswith("{"):
            match = re.search(r'(?:while|enquanto)\s*\((.*?)\)\s*\{', linha)
            if not match:
                raise SyntaxError(f"{mensagem('loop_syntax')}: {linha}")
            cond = match.group(1)
            self.pos += 1
            bloco = []
            nivel = 1
            while self.pos < len(self.linhas):
                l = self.linhas[self.pos]
                if l.endswith("{"): nivel += 1
                if l == "}":
                    nivel -= 1
                    if nivel == 0: break
                bloco.append(self.parse_comando(l))
                self.pos += 1
            return EnquantoNode(cond, bloco)

        if (linha.startswith("if") or linha.startswith("se")) and ("then" in linha or "entao" in linha) and linha.endswith("{"):
            match = re.search(r'(?:if|se)\s*\((.*?)\)\s*(?:then|entao)', linha)
            if not match:
                raise SyntaxError(f"{mensagem('if_syntax')}: {linha}")
            cond = match.group(1)
            self.pos += 1
            bloco_entao = []
            nivel = 1
            while self.pos < len(self.linhas):
                l = self.linhas[self.pos]
                if l.endswith("{"): nivel += 1
                if l == "}":
                    nivel -= 1
                    if nivel == 0: break
                bloco_entao.append(self.parse_comando(l))
                self.pos += 1
            
            bloco_senao = None
            if self.pos + 1 < len(self.linhas):
                prox = self.linhas[self.pos + 1].strip()
                if prox.startswith("else") or prox.startswith("senao"):
                    self.pos += 2
                    bloco_senao = []
                    nivel_else = 1
                    while self.pos < len(self.linhas):
                        l = self.linhas[self.pos]
                        if l.endswith("{"): nivel_else += 1
                        if l == "}":
                            nivel_else -= 1
                            if nivel_else == 0: break
                        bloco_senao.append(self.parse_comando(l))
                        self.pos += 1

            return SeNode(cond, bloco_entao, bloco_senao)

        limpa_linha = linha
        if limpa_linha.startswith("var "):
            limpa_linha = limpa_linha[4:].strip()

        if "=" in limpa_linha:
            nome, expr = limpa_linha.split("=", 1)
            return AtribuicaoNode(nome.strip(), expr.strip())

        return EscreverNode(f"// Comando desconhecido: {linha}")


# --- 4. AMBIENTE DE EXECUÇÃO (RUNTIME BASEADO EM AST) ---
class RudyRuntime:
    def __init__(self):
        self.variaveis = {}

    def avaliar_valor(self, expr: str) -> RudyValor:
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
            try:
                return input(str(prompt))
            except KeyboardInterrupt:
                print("\n[Rudy] Entrada interrompida pelo usuário.")
                sys.exit(0)

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
                val_esq = self.avaliar_valor(esq)
                val_dir = self.avaliar_valor(dir_)
                
                try:
                    v1 = int(val_esq) if str(val_esq).strip() != '' else 0
                except ValueError:
                    v1 = 0
                try:
                    v2 = int(val_dir) if str(val_dir).strip() != '' else 0
                except ValueError:
                    v2 = 0

                if op == '+': return v1 + v2
                if op == '-': return v1 - v2
                if op == '*': return v1 * v2
                if op == '/': return v1 // v2 if v2 != 0 else 0

        if expr in self.variaveis:
            val = self.variaveis[expr]
            if str(val).isdigit() or (str(val).startswith('-') and str(val)[1:].isdigit()):
                return int(val)
            return val
            
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
                try:
                    iv1 = int(v1) if str(v1).strip() != '' else 0
                    iv2 = int(v2) if str(v2).strip() != '' else 0
                except ValueError:
                    iv1, iv2 = 0, 0
                if op == '>':  return iv1 > iv2
                if op == '<':  return iv1 < iv2
                if op == '>=': return iv1 >= iv2
                if op == '<=': return iv1 <= iv2
        return False

    def executar(self, no):
        if isinstance(no, ProgramaNode):
            for decl in no.declaracoes:
                self.executar(decl)
        elif isinstance(no, FuncaoNode):
            for cmd in no.corpo:
                self.executar(cmd)
        elif isinstance(no, AtribuicaoNode):
            self.variaveis[no.nome] = self.avaliar_valor(no.expr)
        elif isinstance(no, EscreverNode):
            print(self.avaliar_valor(no.conteudo))
        elif isinstance(no, SalvarNode):
            path = self.avaliar_valor(no.path)
            conteudo = self.avaliar_valor(no.conteudo)
            with open(str(path), 'w', encoding='utf-8') as f:
                f.write(str(conteudo))
        elif isinstance(no, LimparNode):
            os.system('cls' if os.name == 'nt' else 'clear')
        elif isinstance(no, EnquantoNode):
            while self.avaliar_condicao(no.condicao):
                for cmd in no.bloco:
                    self.executar(cmd)
        elif isinstance(no, SeNode):
            if self.avaliar_condicao(no.condicao):
                for cmd in no.bloco_entao:
                    self.executar(cmd)
            elif no.bloco_senao:
                for cmd in no.bloco_senao:
                    self.executar(cmd)


# --- 5. GERENCIADOR DE PACOTES (RUDY INSTALL) ---
def rudy_install(pacote_nome):
    print(mensagem("package_install", pkg=pacote_nome))
    os.makedirs("stdlib", exist_ok=True)
    
    if pacote_nome.startswith("http://") or pacote_nome.startswith("https://"):
        url = pacote_nome
        nome_arquivo = url.split("/")[-1]
        if not nome_arquivo.endswith(".rudy"):
            nome_arquivo += ".rudy"
    else:
        url = f"https://raw.githubusercontent.com/luispolis124/Rudy/main/stdlib/{pacote_nome}.rudy"
        nome_arquivo = f"{pacote_nome}.rudy"
        
    destino = os.path.join("stdlib", nome_arquivo)
    
    try:
        print(f"{mensagem('download')}: {url}")
        urllib.request.urlretrieve(url, destino)
        print(f"[Success!] {mensagem('installed', pkg=pacote_nome, file=nome_arquivo)}")
    except Exception as e:
        print(f"{mensagem('download_error', pkg=pacote_nome)}: {e}")
        with open(destino, 'w', encoding='utf-8') as f:
            f.write(f"{mensagem('fallback_comment')}: {pacote_nome}\n")
            f.write(f'write("{mensagem("fallback_loaded", pkg=pacote_nome)}")\n')
        print(f"[Fallback] {mensagem('fallback', dest=destino)}")


# --- 6. BYTECODE COMPILER LAYER (OPCIONAL) ---
def compilar_para_bytecode(arquivo_path):
    print(mensagem("bytecode_compile", file=arquivo_path))
    with open(arquivo_path, 'r', encoding='utf-8') as f:
        codigo_fonte = f.read()
    
    t_inicio = time.perf_counter()
    objeto_bytecode = compile(codigo_fonte, arquivo_path, 'exec')
    
    base_nome = os.path.splitext(arquivo_path)[0]
    bytecode_path = f"{base_nome}.rudybc"
    with open(bytecode_path, 'wb') as bc_file:
        bc_file.write(marshal.dumps(objeto_bytecode))
        
    t_fim = time.perf_counter()
    print(f"[Success!] {mensagem('bytecode_success', file=bytecode_path)} ({((t_fim - t_inicio) * 1000):.4f} ms).")
    return objeto_bytecode


# --- 7. MODO INTERATIVO (REPL SHELL) ---
def iniciar_repl():
    print("====================================================")
    print(f"🐺 {mensagem('repl_title')}")
    print(mensagem("repl_help"))
    print("====================================================")
    
    runtime = RudyRuntime() # Mantém as variáveis ativas durante a sessão
    
    while True:
        try:
            linha = input("\nrudy> ").strip()
            if not linha:
                continue
            if linha.lower() in ('exit', 'sair', 'quit'):
                print(f"{mensagem('repl_bye')} 🐺")
                break
                
            parser = Parser([linha])
            ast = parser.parse()
            runtime.executar(ast)
            
        except KeyboardInterrupt:
            print(f"\n{mensagem('repl_interrupt')}")
        except Exception as e:
            print(f"{mensagem('rudy_error')} {e}")


# --- 8. COMPILADOR / EMPACOTADOR STANDALONE (.EXE) ---
def compilar_para_executavel(arquivo_path):
    print(mensagem("compiler", file=arquivo_path))
    try:
        import PyInstaller
    except ImportError:
        print(mensagem("pyinstaller_missing"))
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])

    with open(arquivo_path, 'r', encoding='utf-8') as f:
        codigo_rudy = f.read()

    stub_code = f'''
import sys
import os
import re
import random
import time

CODIGO_EMBARCADO = """{codigo_rudy}"""

class ProgramaNode:
    def __init__(self, declaracoes): self.declaracoes = declaracoes
class FuncaoNode:
    def __init__(self, nome, corpo): self.nome = nome; self.corpo = corpo
class AtribuicaoNode:
    def __init__(self, nome, expr): self.nome = nome; self.expr = expr
class EscreverNode:
    def __init__(self, conteudo): self.conteudo = conteudo
class SalvarNode:
    def __init__(self, path, conteudo): self.path = path; self.conteudo = conteudo
class LimparNode: pass
class SeNode:
    def __init__(self, condicao, bloco_entao, bloco_senao=None): self.condicao = condicao; self.bloco_entao = bloco_entao; self.bloco_senao = bloco_senao
class EnquantoNode:
    def __init__(self, condicao, bloco): self.condicao = condicao; self.bloco = bloco

class Parser:
    def __init__(self, linhas):
        self.linhas = [l.strip() for l in linhas if l.strip() and not l.strip().startswith("//")]
        self.pos = 0
    def linha_atual(self): return self.linhas[self.pos] if self.pos < len(self.linhas) else None
    def parse(self):
        declaracoes = []
        while self.pos < len(self.linhas):
            linha = self.linha_atual()
            if linha.startswith("use ") or linha.startswith("usar "):
                self.pos += 1
                continue
            if (linha.startswith("action ") or linha.startswith("acao ")) and linha.endswith("{{"):
                declaracoes.append(self.parse_funcao())
            else:
                declaracoes.append(self.parse_comando(linha))
                self.pos += 1
        return ProgramaNode(declaracoes)
    def parse_funcao(self):
        linha = self.linhas[self.pos]
        match = re.search(r'(?:action|acao)\\s+([a-zA-Z_][a-zA-Z0-9_]*)\\s*\\(\\s*\\)\\s*\\{{', linha)
        nome = match.group(1)
        self.pos += 1
        corpo = []
        nivel = 1
        while self.pos < len(self.linhas):
            l = self.linhas[self.pos]
            if l.endswith("{{"): nivel += 1
            if l == "}}":
                nivel -= 1
                if nivel == 0:
                    self.pos += 1
                    break
            corpo.append(self.parse_comando(l))
            self.pos += 1
        return FuncaoNode(nome, corpo)
    def parse_comando(self, linha):
        if linha == "clear()" or linha == "limpar()": return LimparNode()
        if (linha.startswith("write(") or linha.startswith("escrever(")) and linha.endswith(")"):
            return EscreverNode(linha[linha.index("(")+1:-1].strip())
        if (linha.startswith("save(") or linha.startswith("salvar(")) and linha.endswith(")"):
            args = linha[linha.index("(")+1:-1].split(",", 1)
            return SalvarNode(args[0].strip(), args[1].strip())
        if (linha.startswith("while") or linha.startswith("enquanto")) and linha.endswith("{{"):
            match = re.search(r'(?:while|enquanto)\\s*\\((.*?)\\)\\s*\\{{', linha)
            cond = match.group(1)
            self.pos += 1
            bloco = []
            nivel = 1
            while self.pos < len(self.linhas):
                l = self.linhas[self.pos]
                if l.endswith("{{"): nivel += 1
                if l == "}}":
                    nivel -= 1
                    if nivel == 0: break
                bloco.append(self.parse_comando(l))
                self.pos += 1
            return EnquantoNode(cond, bloco)
        if (linha.startswith("if") or linha.startswith("se")) and ("then" in linha or "entao" in linha) and linha.endswith("{{"):
            match = re.search(r'(?:if|se)\\s*\\((.*?)\\)\\s*(?:then|entao)', linha)
            cond = match.group(1)
            self.pos += 1
            bloco_entao = []
            nivel = 1
            while self.pos < len(self.linhas):
                l = self.linhas[self.pos]
                if l.endswith("{{"): nivel += 1
                if l == "}}":
                    nivel -= 1
                    if nivel == 0: break
                bloco_entao.append(self.parse_comando(l))
                self.pos += 1
            bloco_senao = None
            if self.pos + 1 < len(self.linhas):
                prox = self.linhas[self.pos + 1].strip()
                if prox.startswith("else") or prox.startswith("senao"):
                    self.pos += 2
                    bloco_senao = []
                    nivel_else = 1
                    while self.pos < len(self.linhas):
                        l = self.linhas[self.pos]
                        if l.endswith("{{"): nivel_else += 1
                        if l == "}}":
                            nivel_else -= 1
                            if nivel_else == 0: break
                        bloco_senao.append(self.parse_comando(l))
                        self.pos += 1
            return SeNode(cond, bloco_entao, bloco_senao)
        limpa_linha = linha[4:].strip() if linha.startswith("var ") else linha
        if "=" in limpa_linha:
            nome, expr = limpa_linha.split("=", 1)
            return AtribuicaoNode(nome.strip(), expr.strip())
        return EscreverNode("")

class RudyRuntime:
    def __init__(self): self.variaveis = {{}}
    def avaliar_valor(self, expr):
        expr = expr.strip()
        if (expr.startswith("load(") or expr.startswith("carregar(")) and expr.endswith(")"):
            path = self.avaliar_valor(expr[expr.index("(")+1:-1])
            if os.path.exists(str(path)):
                with open(str(path), 'r', encoding='utf-8') as f: return f.read()
            return ""
        if (expr.startswith("sleep(") or expr.startswith("pausar(")) and expr.endswith(")"):
            time.sleep(float(self.avaliar_valor(expr[expr.index("(")+1:-1])))
            return 0
        if (expr.startswith("ask(") or expr.startswith("ler(")) and expr.endswith(")"):
            try:
                return input(str(self.avaliar_valor(expr[expr.index("(")+1:-1])))
            except KeyboardInterrupt:
                print("\\n[Rudy] Entrada interrompida pelo usuário.")
                sys.exit(0)
        if (expr.startswith("random(") or expr.startswith("aleatorio(")) and expr.endswith(")"):
            args = expr[expr.index("(")+1:-1].split(",")
            return random.randint(int(self.avaliar_valor(args[0])), int(self.avaliar_valor(args[1])))
        if '"' in expr or "'" in expr:
            resultado = ""
            for p in expr.split('+'):
                p = p.strip()
                if (p.startswith('"') and p.endswith('"')) or (p.startswith("'") and p.endswith("'")):
                    resultado += p[1:-1]
                elif p in self.variaveis:
                    resultado += str(self.variaveis[p])
                else: resultado += p
            return resultado
        for op in ['+', '-', '*', '/']:
            if op in expr:
                esq, dir_ = expr.split(op, 1)
                val_esq, val_dir = self.avaliar_valor(esq), self.avaliar_valor(dir_)
                try: v1 = int(val_esq) if str(val_esq).strip() != '' else 0
                except ValueError: v1 = 0
                try: v2 = int(val_dir) if str(val_dir).strip() != '' else 0
                except ValueError: v2 = 0
                return v1 + v2 if op == '+' else (v1 - v2 if op == '-' else (v1 * v2 if op == '*' else (v1 // v2 if v2 != 0 else 0)))
        if expr in self.variaveis:
            val = self.variaveis[expr]
            if str(val).isdigit() or (str(val).startswith('-') and str(val)[1:].isdigit()): return int(val)
            return val
        if expr.isdigit() or (expr.startswith('-') and expr[1:].isdigit()): return int(expr)
        return expr

    def avaliar_condicao(self, cond):
        if " and " in cond or " e " in cond:
            return all(self.avaliar_condicao(p) for p in cond.split(" and " if " and " in cond else " e "))
        if " or " in cond or " ou " in cond:
            return any(self.avaliar_condicao(p) for p in cond.split(" or " if " or " in cond else " ou "))
        for op in ['==', '!=', '>=', '<=', '>', '<']:
            if op in cond:
                esq, dir_ = cond.split(op, 1)
                v1, v2 = self.avaliar_valor(esq.strip()), self.avaliar_valor(dir_.strip())
                if op == '==': return str(v1) == str(v2)
                if op == '!=': return str(v1) != str(v2)
                try:
                    iv1 = int(v1) if str(v1).strip() != '' else 0
                    iv2 = int(v2) if str(v2).strip() != '' else 0
                except ValueError:
                    iv1, iv2 = 0, 0
                return iv1 > iv2 if op == '>' else (iv1 < iv2 if op == '<' else (iv1 >= iv2 if op == '>=' else iv1 <= iv2))
        return False

    def executar(self, no):
        if isinstance(no, ProgramaNode):
            for decl in no.declaracoes: self.executar(decl)
        elif isinstance(no, FuncaoNode):
            for cmd in no.corpo: self.executar(cmd)
        elif isinstance(no, AtribuicaoNode):
            self.variaveis[no.nome] = self.avaliar_valor(no.expr)
        elif isinstance(no, EscreverNode):
            print(self.avaliar_valor(no.conteudo))
        elif isinstance(no, SalvarNode):
            with open(str(self.avaliar_valor(no.path)), 'w', encoding='utf-8') as f:
                f.write(str(self.avaliar_valor(no.conteudo)))
        elif isinstance(no, LimparNode):
            os.system('cls' if os.name == 'nt' else 'clear')
        elif isinstance(no, EnquantoNode):
            while self.avaliar_condicao(no.condicao):
                for cmd in no.bloco: self.executar(cmd)
        elif isinstance(no, SeNode):
            if self.avaliar_condicao(no.condicao):
                for cmd in no.bloco_entao: self.executar(cmd)
            elif no.bloco_senao:
                for cmd in no.bloco_senao: self.executar(cmd)

if __name__ == "__main__":
    t_inicio = time.perf_counter()
    parser = Parser(CODIGO_EMBARCADO.split('\\n'))
    ast = parser.parse()
    runtime = RudyRuntime()
    runtime.executar(ast)
    t_fim = time.perf_counter()
    print(f"\\n[Rudy Benchmark] Tempo: {{((t_fim - t_inicio) * 1000):.2f}} ms")
'''

    stub_filename = "rudy_temp_stub.py"
    with open(stub_filename, 'w', encoding='utf-8') as f:
        f.write(stub_code)

    base_nome = os.path.splitext(os.path.basename(arquivo_path))[0]
    print(f"{mensagem('generating')} '{base_nome}'...")
    subprocess.check_call([sys.executable, "-m", "PyInstaller", "--onefile", "--noconsole", stub_filename])
    
    if os.path.exists(stub_filename):
        os.remove(stub_filename)
        
    print(f"\n[Success!] {mensagem('success_exe')} for '{base_nome}'.")


# --- 9. FUNÇÃO PRINCIPAL ---
def main():
    localidade_recursos = obter_localidade()
    if LOCALIDADE != localidade_recursos:
        globals()["LOCALIDADE"] = localidade_recursos

    # Se nenhum argumento for passado ou se usar --repl / -i, abre o REPL interactivo
    if len(sys.argv) < 2 or sys.argv[1] in ('--repl', '-i', 'repl'):
        iniciar_repl()
        return
        
    comando_ou_arquivo = sys.argv[1]
    
    if comando_ou_arquivo in ('install', 'instalar'):
        if len(sys.argv) < 3:
            print(mensagem("missing_arg"))
            return
        rudy_install(sys.argv[2])
        return

    arquivo_path = comando_ou_arquivo
    if not os.path.exists(arquivo_path):
        print(mensagem("file_missing", file=arquivo_path))
        return
        
    # Tratamento da flag de Bytecode (--bytecode / -b)
    if len(sys.argv) >= 3 and sys.argv[2] in ('--bytecode', '-b', 'bytecode'):
        t_inicio = time.perf_counter()
        bc = compilar_bytecode = compilar_para_bytecode(arquivo_path)
        print(mensagem("bytecode_running"))
        
        exec(bc, {'__builtins__': None}, {'print': print, 'input': input, 'os': os, 'random': random, 'time': time, 'sys': sys})
        
        t_fim = time.perf_counter()
        print(f"\n[Rudy Benchmark - Bytecode] {mensagem('total_time')}: {((t_fim - t_inicio) * 1000):.2f} ms")
        return

    # Tratamento da flag de Compilação Standalone (--build)
    if len(sys.argv) >= 3 and sys.argv[2] in ('--build', '--compilar', 'build'):
        compilar_para_executavel(arquivo_path)
        return

    # Execução padrão via AST Interpreter
    with open(arquivo_path, 'r', encoding='utf-8') as f:
        codigo_fonte = f.read()
        
    print(f"--- {mensagem('ast_running', file=arquivo_path)} ---")
    
    tempo_inicio = time.perf_counter()
    
    tokens = lexer(codigo_fonte)
    parser = Parser(codigo_fonte.split('\n'))
    ast = parser.parse()
    
    runtime = RudyRuntime()
    runtime.executar(ast)
    
    tempo_fim = time.perf_counter()
    tempo_total_ms = (tempo_fim - tempo_inicio) * 1000
    
    print(f"\n[Rudy Benchmark] {mensagem('execution_time')}: {tempo_total_ms:.2f} ms")

if __name__ == "__main__":
    main()
