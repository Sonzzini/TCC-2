import requests

def testar_conexao_com_ollama():
    prompt = """
Considere o seguinte método em Java:

public int somar(int a, int b) {
    return a + b;
}

Explique o que esse método faz.
"""

    try:
        resposta = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "codellama:13b-instruct",
                "prompt": prompt,
                "stream": False
            }
        )

        resposta.raise_for_status()  # Gera exceção se a resposta for erro HTTP
        resultado = resposta.json()
        output = resultado.get("response", "[Sem resposta da IA]")
        print("\n🔍 Resposta da IA:\n")
        print(output)

    except requests.exceptions.RequestException as e:
        print("❌ Erro ao se comunicar com a IA:")
        print(e)

if __name__ == "__main__":
    testar_conexao_com_ollama()
