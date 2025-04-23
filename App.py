import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from JavaToJSON import extrair_metodos
import re
import requests
import json


def gerar_json():
    try:
        texto = area_texto.get(1.0, tk.END)
        blocos = re.split(r'// Arquivo: .*\.java', texto)
        jsons = []

        for bloco in blocos:
            if not bloco.strip():
                continue

            classe_match = re.search(r'class\s+(\w+)', bloco)
            nome_classe = classe_match.group(1) if classe_match else "ClasseDesconhecida"

            metodos = extrair_metodos(bloco)

            estrutura_json = {
                "class": nome_classe,
                "methods": metodos
            }

            jsons.append(estrutura_json)

        return jsons
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao gerar JSONs:\n{e}")
        return []

def exibir_json():
    estrutura_json = gerar_json()
    if estrutura_json:
        messagebox.showinfo("JSON Gerado")

def testar_conexao_com_ollama():
    prompt_teste = "Explique o que este método Java faz: public int soma(int a, int b) { return a + b; }"
    try:
        resposta = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "codellama:13b-instruct",
                "prompt": prompt_teste,
                "stream": False
            }
        )
        resposta.raise_for_status()
        messagebox.showinfo("Conexão com IA", "✅ Teste de conexão com a IA realizado com sucesso!")
    except Exception as e:
        messagebox.showerror("Erro", f"❌ Erro ao se conectar com a IA:\n{e}")

def give_IA():
    estruturas_json = gerar_json()
    if not estruturas_json:
        return

    output_final = ""

    for estrutura_json in estruturas_json:
        nome_classe = estrutura_json.get("class", "ClasseDesconhecida")
        metodos = estrutura_json.get("methods", {})

        output_final += f"📘 Análise da Classe Java: **{nome_classe}**\n\n"

        for nome_metodo, dados_metodo in metodos.items():
            assinatura = dados_metodo.get("signature", "")
            corpo = "\n".join(dados_metodo.get("body", []))

            prompt = f"""Considere a seguinte classe Java chamada "{nome_classe}".
Agora analise individualmente o método chamado "{nome_metodo}", com a seguinte assinatura e corpo:

{assinatura}
{corpo}

Explique tecnicamente o que esse método faz e, se possível, sugira melhorias ou refatorações.
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
                resposta.raise_for_status()
                resultado = resposta.json()
                saida = resultado.get("response", "[Sem resposta da IA]")
                output_final += f"🔹 Método: **{nome_metodo}**\n{saida}\n\n"

            except Exception as e:
                output_final += f"⚠️ Erro ao analisar o método {nome_metodo}:\n{e}\n\n"

    area_texto.delete(1.0, tk.END)
    area_texto.insert(tk.END, output_final)


# Criação da Janela
janela = tk.Tk()
janela.title("Visualizador de Arquivo Java")
janela.geometry("700x500")

frame_botoes = tk.Frame(janela)
frame_botoes.pack(pady=10)

botao_abrir = tk.Button(frame_botoes, text="Abrir Arquivo .java", command=lambda: abrir_arquivo())
botao_abrir.grid(row=0, column=0, padx=5)

botao_gerar = tk.Button(frame_botoes, text="Gerar JSON", command=exibir_json)
botao_gerar.grid(row=0, column=1, padx=5)

botao_mandar = tk.Button(frame_botoes, text="Mandar para IA", command=give_IA)
botao_mandar.grid(row=0, column=2, padx=5)

botao_teste = tk.Button(frame_botoes, text="Testar IA", command=testar_conexao_com_ollama)
botao_teste.grid(row=0, column=3, padx=5)

# Área de texto com barra de rolagem
area_texto = scrolledtext.ScrolledText(janela, wrap=tk.WORD, font=("Courier", 12))
area_texto.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# Frame horizontal para arquivos
frame_arquivos = tk.Frame(janela)
frame_arquivos.pack(fill=tk.X, padx=10, pady=(0, 10))

arquivos_selecionados = []

def atualizar_pills_arquivos():
    for widget in frame_arquivos.winfo_children():
        widget.destroy()

    for caminho in arquivos_selecionados:
        nome_arquivo = caminho.split("/")[-1]
        frame_pill = tk.Frame(frame_arquivos, bg="#ddd", bd=1, relief="solid")
        frame_pill.pack(side=tk.LEFT, padx=4, pady=2)

        btn_fechar = tk.Button(frame_pill, text="✕", command=lambda c=caminho: remover_arquivo(c), bg="#ddd", bd=0)
        btn_fechar.pack(side=tk.LEFT, padx=(4, 0))

        lbl_nome = tk.Label(frame_pill, text=nome_arquivo, bg="#ddd")
        lbl_nome.pack(side=tk.LEFT, padx=(4, 6))

    btn_add = tk.Button(frame_arquivos, text="+", command=abrir_arquivo, bg="#ccc", width=2)
    btn_add.pack(side=tk.LEFT, padx=4)

def remover_arquivo(caminho):
    global arquivos_selecionados
    arquivos_selecionados = [c for c in arquivos_selecionados if c != caminho]
    atualizar_pills_arquivos()

def abrir_arquivo():
    global arquivos_selecionados
    novos_arquivos = filedialog.askopenfilenames(
        filetypes=[("Arquivos Java", "*.java"), ("Todos os arquivos", "*.*")]
    )
    novos_arquivos = [f for f in novos_arquivos if f not in arquivos_selecionados]

    if novos_arquivos:
        arquivos_selecionados += novos_arquivos
        atualizar_pills_arquivos()

        conteudo_total = ""
        for caminho in arquivos_selecionados:
            try:
                with open(caminho, "r", encoding="utf-8") as arquivo:
                    conteudo = arquivo.read()
                    conteudo_total += f"// Arquivo: {caminho.split('/')[-1]}\n" + conteudo + "\n\n"
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao abrir o arquivo:\n{caminho}\n{e}")

        area_texto.delete(1.0, tk.END)
        area_texto.insert(tk.END, conteudo_total)

atualizar_pills_arquivos()

# Loop principal
janela.mainloop()
