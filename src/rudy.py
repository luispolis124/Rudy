import sys
import os
import re
import random
import time

def avaliar_valor(expr, variaveis):
    expr = expr.strip()

    # Função de leitura de arquivo: load("arquivo.txt") ou carregar("arquivo.txt")
    if (expr.startswith("load(") or expr.startswith("carregar(")) and expr.endswith(")"):
        idx = expr.index("(")
        path = avaliar_valor(expr[idx+1:-1], variaveis)
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                return f.read()
        return ""

    # Função de pausa/sleep: sleep(segundos) ou pausar(segundos)
    if (expr.startswith("sleep(") or expr.startswith("pausar(")) and expr.endswith(")"):
        idx = expr.index("(")
        tempo = float(avaliar_valor(expr[idx+1:-1], variaveis))
        time.sleep(tempo)
        return 0

    # Função de entrada de dados: ask("pergunta") ou ler("pergunta")
    if (expr.startswith("ask(") or expr.startswith("ler(")) and expr.endswith(")"):
        idx = expr.index("(")
        prompt_expr = expr[idx+1:-1]
        prompt = avaliar_valor(prompt_expr, variaveis)
        return input(str(prompt))

    # Função aleatória: random(min, max) ou aleatorio(min, max)
    if (expr.startswith("random(") or expr.startswith("aleatorio(")) and expr.endswith(")"):
        idx = expr.index("(")
        args = expr[idx+1:-1].split(",")
        min_v = int(avaliar_valor(args[0], variaveis))
        max_v = int(avaliar_valor(args[1], variaveis))
        return random.randint(min_v, max_v)

    # Concatenação de strings e variáveis com operador '+'
    if '"' in expr or "'" in expr:
        partes = expr.split('+')
        resultado = ""
        for p in partes:
            p = p.strip()
            if (p.startswith('"') and p.endswith('"')) or (p.startswith("'") and p.endswith("'")):
                resultado += p[1:-1]
            elif p in variaveis:
                resultado += str(variaveis[p])
            else:
                resultado += p
        return resultado

    # Operações matemáticas básicas (+, -, *, /)
    for op in ['+', '-', '*', '/']:
        if op in expr:
            esq, dir_ = expr.split(op, 1)
            v1 = int(avaliar_valor(esq, variaveis))
            v2 = int(avaliar_valor(dir_, variaveis))
            if op == '+': return v1 + v2
            if op == '-': return v1 - v2
            if op == '*': return v1 * v2
            if op == '/': return v1 // v2

    if expr in variaveis:
        return variaveis[expr]
    if expr.isdigit() or (expr.startswith('-') and expr[1:].isdigit()):
        return int(expr)
    return expr

def avaliar_condicao(cond, variaveis):
    if " and " in cond or " e " in cond:
        separador = " and " if " and " in cond else " e "
        partes = cond.split(separador)
        return all(avaliar_condicao(p, variaveis) for p in partes)
    if " or " in cond or " ou " in cond:
        separador = " or " if " or " in cond else " ou "
        partes = cond.split(separador)
        return any(avaliar_condicao(p, variaveis) for p in partes)

    for op in ['==', '!=', '>=', '<=', '>', '<']:
        if op in cond:
            esq, dir_ = cond.split(op, 1)
            v1 = avaliar_valor(esq.strip(), variaveis)
            v2 = avaliar_valor(dir_.strip(), variaveis)
            if op == '==': return str(v1) == str(v2)
            if op == '!=': return str(v1) != str(v2)
            if op == '>':  return int(v1) > int(v2)
            if op == '<':  return int(v1) < int(v2)
            if op == '>=': return int(v1) >= int(v2)
            if op == '<=': return int(v1) <= int(v2)
    return False

def encontrar_fim_bloco(linhas, inicio):
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

def executar_bloco(linhas, inicio, fim, variaveis):
    i = inicio
    while i <= fim:
        linha = linhas[i].strip()

        # Ignora linhas vazias e comentários
        if not linha or linha.startswith("//") or linha == "}":
            i += 1
            continue

        # Comando clear() ou limpar() para animações e telas dinâmicas
        if linha == "clear()" or linha == "limpar()":
            os.system('cls' if os.name == 'nt' else 'clear')
            i += 1
            continue

        # Ignora declarações de ação (action main() { ou acao principal() {)
        if (linha.startswith("action ") or linha.startswith("acao ")) and linha.endswith("{"):
            i += 1
            continue

        # Estrutura de repetição: while (...) { ou enquanto (...) {
        if (linha.startswith("while") or linha.startswith("enquanto")) and linha.endswith("{"):
            match = re.search(r'(?:while|enquanto)\s*\((.*?)\)\s*\{', linha)
            fim_bloco = encontrar_fim_bloco(linhas, i)
            if match:
                cond = match.group(1)
                while avaliar_condicao(cond, variaveis):
                    executar_bloco(linhas, i + 1, fim_bloco - 1, variaveis)
            i = fim_bloco + 1
            continue

        # Estrutura condicional: if (...) then { [else { ... }] } ou se (...) entao { [senao { ... }] }
        if (linha.startswith("if") or linha.startswith("se")) and ("then" in linha or "entao" in linha) and linha.endswith("{"):
            match = re.search(r'(?:if|se)\s*\((.*?)\)\s*(?:then|entao)', linha)
            fim_if = encontrar_fim_bloco(linhas, i)
            
            condicao_atendida = False
            if match and avaliar_condicao(match.group(1), variaveis):
                condicao_atendida = True
                executar_bloco(linhas, i + 1, fim_if - 1, variaveis)
            
            # Verifica se logo após o fechamento do if tem um else / senao
            proxima_linha_idx = fim_if + 1
            if proxima_linha_idx < len(linhas):
                prox_linha = linhas[proxima_linha_idx].strip()
                if prox_linha.startswith("else") or prox_linha.startswith("senao"):
                    fim_else = encontrar_fim_bloco(linhas, proxima_linha_idx)
                    if not condicao_atendida:
                        executar_bloco(linhas, proxima_linha_idx + 1, fim_else - 1, variaveis)
                    i = fim_else + 1
                    continue

            i = fim_if + 1
            continue

        # Comandos de gravação em arquivo: save("arq.txt", texto) ou salvar("arq.txt", texto)
        if (linha.startswith("save(") or linha.startswith("salvar(")) and linha.endswith(")"):
            idx = linha.index("(")
            args_str = linha[idx+1:-1]
            # Divide os argumentos separando por vírgula (cuidado simples)
            partes = args_str.split(",", 1)
            if len(partes) == 2:
                path = avaliar_valor(partes[0].strip(), variaveis)
                conteudo = avaliar_valor(partes[1].strip(), variaveis)
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(str(conteudo))
            i += 1
            continue

        # Comandos de escrita: write(...) ou escrever(...)
        if (linha.startswith("write(") or linha.startswith("escrever(")) and linha.endswith(")"):
            idx = linha.index("(")
            conteudo = linha[idx+1:-1]
            print(avaliar_valor(conteudo, variaveis))
            i += 1
            continue

        # Atribuição de variáveis
        if "=" in linha and not linha.startswith("if") and not linha.startswith("while") and not linha.startswith("se") and not linha.startswith("enquanto") and not linha.startswith("else") and not linha.startswith("senao"):
            nome, expr = linha.split("=", 1)
            variaveis[nome.strip()] = avaliar_valor(expr.strip(), variaveis)
            i += 1
            continue

        print(f"Erro de sintaxe na linha {i+1}: {linha}")
        i += 1

def main():
    if len(sys.argv) < 2:
        print("Uso: python src/rudy.py <arquivo.rudy>")
        return
        
    arquivo_path = sys.argv[1]
    if not os.path.exists(arquivo_path):
        print(f"Erro: Arquivo '{arquivo_path}' não encontrado.")
        return
        
    with open(arquivo_path, 'r', encoding='utf-8') as f:
        linhas = f.readlines()
        
    print(f"--- Executando {arquivo_path} com a Rudy ---")
    executar_bloco(linhas, 0, len(linhas) - 1, {})

if __name__ == "__main__":
    main()
