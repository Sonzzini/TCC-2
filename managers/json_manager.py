import re

class JsonManager:

    def __init__(self):
        print("JsonManager inicializado.")

    def extrair_metodos(self, classe_java: str):
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

    def gerar_json(self, texto):
        blocos = re.split(r'// Arquivo: .*\.java', texto)
        jsons = []

        for bloco in blocos:
            if not bloco.strip():
                continue

            classe_match = re.search(r'class\s+(\w+)', bloco)
            nome_classe = classe_match.group(1) if classe_match else "ClasseDesconhecida"
            metodos = self.extrair_metodos(bloco)

            estrutura_json = {
                "class": nome_classe,
                "methods": metodos
            }

            jsons.append(estrutura_json)

        return jsons
