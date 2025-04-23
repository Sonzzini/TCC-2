import re

def extrair_metodos(classe_java: str):
    padrao_metodo = re.compile(
        r'(public|protected|private)?\s+([\w\<\>\[\]]+\s+)?(\w+)\s*\(([^)]*)\)\s*\{',
        re.MULTILINE
    )

    metodos = {}
    pilha = []
    metodo_atual = None
    coletando = False

    linhas = classe_java.splitlines()
    for i, linha in enumerate(linhas):
        if not coletando:
            match = padrao_metodo.search(linha)
            if match:
                assinatura = linha.strip()
                nome_metodo = match.group(3)
                metodo_atual = {
                    "signature": assinatura,
                    "body": []
                }
                metodos[nome_metodo] = metodo_atual
                if "{" in linha:
                    pilha.append("{")
                coletando = True
        else:
            if "{" in linha:
                pilha.append("{")
            if "}" in linha:
                pilha.pop()
            metodo_atual["body"].append(linha.strip())
            if not pilha:
                coletando = False

    return metodos