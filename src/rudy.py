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
    
    # F-string corrigida com (?P<nome>padrao)
    padrao_regex = '|'.join(f'(?P<{nome}>{padrao})' for nome, padrao in TOKEN_TIPOS)
    
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
            raise SyntaxError(f"Erro de sintaxe na definição de função: {linha}")
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
                raise SyntaxError(f"Erro na sintaxe de repetição: {linha}")
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
                raise SyntaxError(f"Erro na sintaxe condicional: {linha}")
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


# --- 5. COMPILADOR / EMPACOTADOR STANDALONE (.EXE) ---
def compilar_para_executavel(arquivo_path):
    print(f"--- [Rudy Compiler] Empacotando '{arquivo_path}' para Executável (.exe) ---")
    try:
        import PyInstaller
    except ImportError:
        print("Aviso: O PyInstaller não está instalado. Instalando automaticamente via pip...")
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
            return input(str(self.avaliar_valor(expr[expr.index("(")+1:-1])))
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
                v1, v2 = int(self.avaliar_valor(esq)), int(self.avaliar_valor(dir_))
                return v1 + v2 if op == '+' else (v1 - v2 if op == '-' else (v1 * v2 if op == '*' else v1 // v2))
        if expr in self.variaveis: return self.variaveis[expr]
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
                return (str(v1) == str(v2)) if op == '==' else ((str(v1) != str(v2)) if op == '!=' else (int(v1) > int(v2) if op == '>' else (int(v1) < int(v2) if op == '<' else (int(v1) >= int(v2) if op == '>=' else int(v1) <= int(v2))))
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
    print(f"\\n[Rudy Benchmark] Tempo: {((t_fim - t_inicio) * 1000):.2f} ms")
'''

    stub_filename = "rudy_temp_stub.py"
    with open(stub_filename, 'w', encoding='utf-8') as f:
        f.write(stub_code)

    base_nome = os.path.splitext(os.path.basename(arquivo_path))[0]
    print(f"Gerando executável standalone para '{base_nome}'...")
    subprocess.check_call([sys.executable, "-m", "PyInstaller", "--onefile", "--noconsole", stub_filename])
    
    if os.path.exists(stub_filename):
        os.remove(stub_filename)
        
    print(f"\n[Sucesso!] Executável gerado na pasta 'dist/' para o programa '{base_nome}'.")


# --- 6. FUNÇÃO PRINCIPAL ---
def main():
    if len(sys.argv) < 2:
        print("Uso: python src/rudy.py <arquivo.rudy> [--build / --compilar]")
        return
        
    arquivo_path = sys.argv[1]
    if not os.path.exists(arquivo_path):
        print(f"Erro: Arquivo '{arquivo_path}' não encontrado.")
        return
        
    if len(sys.argv) >= 3 and sys.argv[2] in ('--build', '--compilar', 'build'):
        compilar_para_executavel(arquivo_path)
        return

    with open(arquivo_path, 'r', encoding='utf-8') as f:
        codigo_fonte = f.read()
        
    print(f"--- Compilando e Executando {arquivo_path} com a Rudy (AST Engine) ---")
    
    tempo_inicio = time.perf_counter()
    
    tokens = lexer(codigo_fonte)
    parser = Parser(codigo_fonte.split('\n'))
    ast = parser.parse()
    
    runtime = RudyRuntime()
    runtime.executar(ast)
    
    tempo_fim = time.perf_counter()
    tempo_total_ms = (tempo_fim - tempo_inicio) * 1000
    
    print(f"\n[Rudy Benchmark] Tempo de execução: {tempo_total_ms:.2f} ms")

if __name__ == "__main__":
    main()
