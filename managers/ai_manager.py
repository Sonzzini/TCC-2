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

    def gerar_prompt_classe(self, estrutura_classe):
        tipo = estrutura_classe.get("type", "")
        nome_classe = estrutura_classe.get("name", "ClasseDesconhecida")
        assinatura = estrutura_classe.get("signature", "Assinatura não fornecida")
        metodos = estrutura_classe.get("methods", {})

        metodos_str = ""
        for nome_metodo, dados_metodo in metodos.items():
            assinatura_metodo = dados_metodo.get("signature", "Assinatura não fornecida")
            corpo_metodo = "\n".join(dados_metodo.get("body", []))
            metodos_str += f"\n// Método: {nome_metodo}\n// Assinatura: {assinatura_metodo}\n// Corpo: {corpo_metodo}\n"

        if tipo == "class":
            prompt = f"""
Você é um especialista em design de software, especializado em princípios SOLID. Sua tarefa é analisar uma classe Java específica, avaliando se ela está em conformidade com cada um dos princípios SOLID. Forneça sua análise de forma clara, concisa e objetiva.
Contexto da classe:
Nome da classe: "{nome_classe}"
Assinatura da classe: "{assinatura}"
Corpo da classe: 
{metodos_str}

Analise a classe e seus métodos de acordo com os seguintes critérios:
1. Princípio da Responsabilidade Única (SRP): O método tem apenas uma responsabilidade bem definida? Justifique.
2. Princípio Aberto/Fechado (OCP): O método está aberto para extensão, mas fechado para modificação? Justifique.
3. Princípio de Substituição de Liskov (LSP): O método respeita o comportamento esperado de sua superclasse ou interface? Justifique.
4. Princípio de Segregação de Interface (ISP): O método depende apenas das interfaces necessárias? Justifique.
5. Princípio da Inversão de Dependência (DIP): O método depende de abstrações em vez de implementações concretas? Justifique.

Para cada método, forneça:
- Nome do Método.
- SRP: {{ "status": "Conforme/Não Conforme/Parcialmente Conforme", "justificativa": "...", "sugestão": "..." }}
- OCP: {{ "status": "Conforme/Não Conforme/Parcialmente Conforme", "justificativa": "...", "sugestão": "..." }}
- LSP: {{ "status": "Conforme/Não Conforme/Parcialmente Conforme", "justificativa": "...", "sugestão": "..." }}
- ISP: {{ "status": "Conforme/Não Conforme/Parcialmente Conforme", "justificativa": "...", "sugestão": "..." }}
- DIP: {{ "status": "Conforme/Não Conforme/Parcialmente Conforme", "justificativa": "...", "sugestão": "..." }}

Responda no seguinte formato JSON:
{{
	"classe": "Nome da Classe",
	"status": "...",
        "metodos": [
        {{
            "nome_metodo": "Nome do Método",
            "SRP": {{"status": "...", "justificativa": "...", "sugestão": "..."}},
            "OCP": {{"status": "...", "justificativa": "...", "sugestão": "..."}},
            "LSP": {{"status": "...", "justificativa": "...", "sugestão": "..."}},
            "ISP": {{"status": "...", "justificativa": "...", "sugestão": "..."}},
            "DIP": {{"status": "...", "justificativa": "...", "sugestão": "..."}}
        }}
    ]
}}
Se o status da classe for "Conforme", inclua um ✅ no campo do status.
Se o status da classe for "Parcialmente Conforme, inclua um ⚠️ no campo do status.
Se o status da classe for "Não Conforme", inclua um ❌ no campo do status.
"""
        elif tipo == "interface":
            prompt = f"""
Você é um especialista em design de software, especializado em princípios SOLID. Sua tarefa é analisar uma interface Java específica, avaliando se ela está em conformidade com os princípios SOLID. Forneça sua análise de forma clara, concisa e objetiva.
Contexto da interface:
Nome da interface: "{nome_classe}"
Assinatura da interface: "{assinatura}"
Métodos da interface:
{metodos_str}

Analise a interface e seus métodos de acordo com os seguintes critérios:
1. Princípio da Segregação de Interface (ISP): A interface está bem segmentada e contém apenas métodos relevantes? Justifique.
2. Princípio da Inversão de Dependência (DIP): A interface depende de abstrações em vez de implementações concretas? Justifique.

Para cada método, forneça:
- Nome do Método.
- ISP: {{ "status": "Conforme/Não Conforme/Parcialmente Conforme", "justificativa": "...", "sugestão": "..." }}
- DIP: {{ "status": "Conforme/Não Conforme/Parcialmente Conforme", "justificativa": "...", "sugestão": "..." }}

Responda no seguinte formato JSON:
{{
	"interface": "Nome da Interface",
	"status": "...",
        "metodos": [
        {{
            "ISP": {{"status": "...", "justificativa": "...", "sugestão": "..."}},
            "DIP": {{"status": "...", "justificativa": "...", "sugestão": "..."}}
        }}
    ]
}}
Se o status da interface for "Conforme", inclua um ✅ no campo do status.
Se o status da interface for "Parcialmente Conforme, inclua um ⚠️ no campo do status.
Se o status da interface for "Não Conforme", inclua um ❌ no campo do status.
"""
        else:
            prompt = f"""
Estrutura desconhecida: {tipo}. Não foi possível gerar um prompt para análise.
"""

        return prompt, tipo
    
    def analisar_classe(self, prompt):
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

    def analisar_metodo(self, nome_classe, nome_metodo, assinatura, corpo):
        prompt = f"""
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
                "prompt": prompt,
                "stream": False
            }
        )
        response.raise_for_status()
        return response.json().get("response", "[Sem resposta da IA]")
