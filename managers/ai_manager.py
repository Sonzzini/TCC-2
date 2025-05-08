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
#         prompt = f"""Considere a seguinte classe/interface Java chamada \"{nome_classe}\".
# Agora analise individualmente o método chamado \"{nome_metodo}\", com a seguinte assinatura e corpo:

# {assinatura}
# {corpo}

# De forma sucinta e objetiva, indique os princípios SOLID implementados em formato de bullet list e, caso haja alguma falta de implementação desses princípios, sugira refatorações.
# """
        new_prompt = f"""
Você é um especialista em design de software, especializado em princípios SOLID. Sua tarefa é analisar um método Java específico em uma classe, avaliando se ele está em conformidade com cada um dos princípios SOLID. Forneça sua análise de forma clara, concisa e objetiva.

Contexto da classe: 
Nome da classe: "{nome_classe}"
Assinatura e corpo do método "{nome_metodo}":
{assinatura}
{corpo}

Analise o método de acordo com os seguintes critérios:
1. Princípio da Responsabilidade Única (SRP): O método tem apenas uma responsabilidade bem definida? Justifique.
2. Princípio Aberto/Fechado (OCP): O método está aberto para extensão, mas fechado para modificação? Justifique.
3. Princípio de Substituição de Liskov (LSP): O método respeita o comportamento esperado de sua superclasse ou interface? Justifique.
4. Princípio de Segregação de Interface (ISP): O método depende apenas das interfaces necessárias? Justifique.
5. Princípio da Inversão de Dependência (DIP): O método depende de abstrações em vez de implementações concretas? Justifique.

Para cada princípio, forneça:
- Status: "Conforme", "Não Conforme" ou "Parcialmente Conforme".
- Justificativa: Uma breve explicação.
- Sugestão de Refatoração (se necessário): Proponha uma melhoria objetiva e prática para garantir conformidade com o princípio.

Responda no seguinte formato JSON:
{{
    "SRP": {{"status": "Conforme/Não Conforme/Parcialmente Conforme", "justificativa": "...", "sugestão": "..."}},
    "OCP": {{"status": "Conforme/Não Conforme/Parcialmente Conforme", "justificativa": "...", "sugestão": "..."}},
    "LSP": {{"status": "Conforme/Não Conforme/Parcialmente Conforme", "justificativa": "...", "sugestão": "..."}},
    "ISP": {{"status": "Conforme/Não Conforme/Parcialmente Conforme", "justificativa": "...", "sugestão": "..."}},
    "DIP": {{"status": "Conforme/Não Conforme/Parcialmente Conforme", "justificativa": "...", "sugestão": "..."}}
}}
"""
        response = requests.post(
            f"{self.base_url}/api/generate",
            json={
                "model": self.model,
                "prompt": new_prompt,
                "stream": False
            }
        )
        response.raise_for_status()
        return response.json().get("response", "[Sem resposta da IA]")
