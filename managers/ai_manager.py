import requests

class AIManager:
    def __init__(self, base_url="http://localhost:11434", model="codellama:13b-instruct"):
        self.base_url = base_url
        self.model = model
        print("AIManager inicializado.")

    def testar_conexao(self, prompt_teste):
        response = requests.post(
            f"{self.base_url}/api/generate",
            json={
                "model": self.model,
                "prompt": prompt_teste,
                "stream": False
            }
        )
        response.raise_for_status()
        return response.json().get("response", "[Sem resposta da IA]")

    def analisar_metodo(self, nome_classe, nome_metodo, assinatura, corpo):
        prompt = f"""Considere a seguinte classe Java chamada \"{nome_classe}\".
Agora analise individualmente o método chamado \"{nome_metodo}\", com a seguinte assinatura e corpo:

{assinatura}
{corpo}

Explique tecnicamente o que esse método faz e, se possível, sugira melhorias ou refatorações.
"""
        response = requests.post(
            f"{self.base_url}/api/generate",
            json={
                "model": self.model,
                "prompt": prompt,
                "stream": False
            }
        )
        response.raise_for_status()
        return response.json().get("response", "[Sem resposta da IA]")
