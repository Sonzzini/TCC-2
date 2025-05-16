import sys
import os
from managers.json_manager import JsonManager
from managers.ai_manager import AIManager
import argparse

def montar_estrutura_pasta(pasta):
    estrutura = {}
    for item in os.listdir(pasta):
        caminho_completo = os.path.join(pasta, item)
        if os.path.isdir(caminho_completo):
            estrutura[item] = montar_estrutura_pasta(caminho_completo)
        else:
            estrutura[item] = None
    if debug_mode:
        print(f"📁 Estrutura da pasta '{pasta}': {estrutura}")
    return estrutura

def gerar_estrutura_projeto(caminhos_arquivos):
    estrutura = {}

    for caminho in caminhos_arquivos:
        if os.path.isfile(caminho):
            pasta = os.path.dirname(caminho) or "."
            nome_arquivo = os.path.basename(caminho)
            if pasta not in estrutura:
                estrutura[pasta] = {}
            estrutura[pasta][nome_arquivo] = None
        elif os.path.isdir(caminho):
            nome_pasta = os.path.basename(caminho)
            estrutura[nome_pasta] = montar_estrutura_pasta(caminho)

    if debug_mode:
        print(f"💾 Estrutura do projeto: {estrutura}")
    return estrutura

def processar_arquivos_cli(caminhos_arquivos, debug_mode=False):
    arquivos_validos = []

    for caminho in caminhos_arquivos:
        if os.path.isfile(caminho) and caminho.endswith(".java"):
            arquivos_validos.append(caminho)
        elif os.path.isdir(caminho):
            for raiz, _, arquivos in os.walk(caminho):
                for arquivo in arquivos:
                    if arquivo.endswith(".java"):
                        arquivos_validos.append(os.path.join(raiz, arquivo))

    if not arquivos_validos:
        print("⚠️ Nenhum arquivo .java válido fornecido.")
        return

    if debug_mode:
        print("\n✅ Arquivos .java encontrados:")
        for arq in arquivos_validos:
            print(f"- {arq}")

    estrutura = gerar_estrutura_projeto(caminhos_arquivos)

    if debug_mode:
        with open("estrutura_projeto.json", "w", encoding="utf-8") as f:
            import json
            json.dump(estrutura, f, indent=2, ensure_ascii=False)
        print("\n📁 Estrutura do projeto salva em 'estrutura_projeto.json'.")

    print("\n🔍 Analisando arquivos...")

    json_manager = JsonManager(debug_mode=debug_mode)
    ai_manager = AIManager(debug_mode=debug_mode)

    conteudo_total = ""
    for caminho in arquivos_validos:
        try:
            with open(caminho, "r", encoding="utf-8") as arquivo:
                conteudo = arquivo.read()
                nome = os.path.basename(caminho)
                conteudo_total += f"// Arquivo: {nome}\n{conteudo}\n\n"
        except Exception as e:
            print(f"❌ Erro ao abrir {caminho}:\n{e}")

    estruturas = json_manager.extrair_classes_interfaces_javalang(conteudo_total)

    if debug_mode:
        print(f"JSON gerado: {estruturas}")

    analise_por_classe(estruturas, ai_manager, debug_mode)

def analise_por_metodos(estruturas, ai_manager: AIManager):
    for estrutura in estruturas:
        nome_classe_interface = estrutura.get("name", "ClasseDesconhecida")
        metodos = estrutura.get("methods", {})

        print(f"\n📘 Classe/Interface: {nome_classe_interface}")
        for nome_metodo, dados in metodos.items():
            assinatura = dados.get("signature", "")
            corpo = "\n".join(dados.get("body", []))
            try:
                resposta = ai_manager.analisar_metodo(nome_classe_interface, nome_metodo, assinatura, corpo)
                print(f"\n🔹 Método: {nome_metodo}\n{resposta}\n")
            except Exception as e:
                print(f"⚠️ Erro ao analisar {nome_metodo}: {e}")

def analise_por_classe(estruturas, ai_manager: AIManager, debug_mode=False):
    for estrutura in estruturas:

        nome_classe = estrutura.get("name", "ClasseDesconhecida")

        prompt, tipo = ai_manager.gerar_prompt_classe(estrutura)

        if debug_mode:
            print(f"📝 Prompt gerado:\n{'-' * 100}\n{prompt}\n{'-' * 100}")

        try:
            resposta = ai_manager.analisar_classe(prompt)
            print(f"\n🔹 {tipo.capitalize()}: {nome_classe}\n{resposta}\n")
        except Exception as e:
            print(f"⚠️ Erro ao analisar {nome_classe}: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ferramenta de análise de classes e interfaces Java com IA.")
    parser.add_argument("caminhos", nargs="+", help="Arquivos ou diretórios .java a serem analisados.")
    parser.add_argument("--debug", action="store_true", help="Exibe informações detalhadas de depuração.")

    args = parser.parse_args()
    debug_mode = args.debug

    if debug_mode:
        print("🔧 Modo de depuração ativado.")

    processar_arquivos_cli(args.caminhos, debug_mode)