import sys
import os

def executar_rudy(codigo_fonte):
    linhas = codigo_fonte.split('\n')
    for linha in linhas:
        linha = linha.strip()
        
        # Ignora comentários
        if linha.startswith("//") or not linha:
            continue
            
        # Comando básico 'escrever("texto")'
        if linha.startswith("escrever(") and linha.endswith(")"):
            # Extrai o que está dentro das aspas
            conteudo = linha[9:-1].strip()
            if (conteudo.startswith('"') and conteudo.endswith('"')) or (conteudo.startswith("'") and conteudo.endswith("'")):
                print(conteudo[1:-1])
            else:
                print(f"Erro: Esperado texto entre aspas em: {linha}")
        else:
            if linha and not linha.startswith("acao") and linha != "}" and linha != "{":
                print(f"Comando desconhecido: {linha}")

def main():
    if len(sys.argv) < 2:
        print("Uso: python rudy.py <arquivo.rudy>")
        return
        
    arquivo_path = sys.argv[1]
    if not os.path.exists(arquivo_path):
        print(f"Erro: Arquivo '{arquivo_path}' não encontrado.")
        return
        
    with open(arquivo_path, 'r', encoding='utf-8') as f:
        codigo = f.read()
        
    print(f"--- Executando {arquivo_path} com a Rudy ---")
    executar_rudy(codigo)

if __name__ == "__main__":
    main()
