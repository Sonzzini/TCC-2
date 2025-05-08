import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, Toplevel
from managers.json_manager import JsonManager
from managers.ai_manager import AIManager
import os
import json

class AppGUI:
    def __init__(self):
        self.json_manager = JsonManager()
        self.ai_manager = AIManager()
        self.arquivos_selecionados = []
        self._criar_janela()

    def _criar_janela(self):
        self.janela = tk.Tk()
        self.janela.title("Visualizador de Arquivo Java")
        self.janela.geometry("700x500")

        frame_botoes = tk.Frame(self.janela)
        frame_botoes.pack(pady=10)

        tk.Button(frame_botoes, text="Abrir Arquivo .java", command=self.abrir_arquivo).grid(row=0, column=0, padx=5)
        tk.Button(frame_botoes, text="Gerar JSON", command=self.exibir_json).grid(row=0, column=1, padx=5)
        tk.Button(frame_botoes, text="Mandar para IA", command=self.mandar_para_ia).grid(row=0, column=2, padx=5)
        tk.Button(frame_botoes, text="Testar IA", command=self.testar_ia).grid(row=0, column=3, padx=5)

        self.area_texto = scrolledtext.ScrolledText(self.janela, wrap=tk.WORD, font=("Courier", 12))
        self.area_texto.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.frame_arquivos = tk.Frame(self.janela)
        self.frame_arquivos.pack(fill=tk.X, padx=10, pady=(0, 10))
        self.atualizar_pills_arquivos()

    def run(self):
        self.janela.mainloop()

    def atualizar_pills_arquivos(self):
        for widget in self.frame_arquivos.winfo_children():
            widget.destroy()

        for caminho in self.arquivos_selecionados:
            nome_arquivo = os.path.basename(caminho)
            frame_pill = tk.Frame(self.frame_arquivos, bg="#ddd", bd=1, relief="solid")
            frame_pill.pack(side=tk.LEFT, padx=4, pady=2)

            tk.Button(frame_pill, text="✕", command=lambda c=caminho: self.remover_arquivo(c), bg="#ddd", bd=0).pack(side=tk.LEFT, padx=(4, 0))
            tk.Label(frame_pill, text=nome_arquivo, bg="#ddd").pack(side=tk.LEFT, padx=(4, 6))

        tk.Button(self.frame_arquivos, text="+", command=self.abrir_arquivo, bg="#ccc", width=2).pack(side=tk.LEFT, padx=4)

    def remover_arquivo(self, caminho):
        self.arquivos_selecionados = [c for c in self.arquivos_selecionados if c != caminho]
        self.atualizar_pills_arquivos()

    def abrir_arquivo(self):
        novos = filedialog.askopenfilenames(filetypes=[("Arquivos Java", "*.java"), ("Todos os arquivos", "*.*")])
        novos = [f for f in novos if f not in self.arquivos_selecionados]

        if novos:
            self.arquivos_selecionados += novos
            self.atualizar_pills_arquivos()
            conteudo_total = ""
            for caminho in self.arquivos_selecionados:
                try:
                    with open(caminho, "r", encoding="utf-8") as arquivo:
                        conteudo = arquivo.read()
                        conteudo_total += f"// Arquivo: {os.path.basename(caminho)}\n" + conteudo + "\n\n"
                except Exception as e:
                    messagebox.showerror("Erro", f"Erro ao abrir o arquivo:\n{caminho}\n{e}")

            self.area_texto.delete(1.0, tk.END)
            self.area_texto.insert(tk.END, conteudo_total)

    def exibir_json(self):
        try:
            estrutura = self.json_manager.extrair_classes_interfaces(self.area_texto.get(1.0, tk.END))
            if estrutura:
                self.abrir_tela_json(estrutura)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao gerar JSONs:\n{e}")

    def abrir_tela_json(self, estrutura):
        janela_json = Toplevel(self.janela)
        janela_json.title("Visualizador de JSON")
        janela_json.geometry("600x400")

        texto_formatado = json.dumps(estrutura, indent=4, ensure_ascii=False)

        area_json = scrolledtext.ScrolledText(janela_json, wrap=tk.WORD, font=("Courier", 11))
        area_json.insert(tk.END, texto_formatado)
        area_json.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def testar_ia(self):
        try:
            self.ai_manager.testar_conexao("Explique o que este método Java faz: public int soma(int a, int b) { return a + b; }")
            messagebox.showinfo("IA", "✅ Teste de conexão com a IA realizado com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", f"❌ Erro ao se conectar com a IA:\n{e}")

    def mandar_para_ia(self):
        try:
            estruturas = self.json_manager.extrair_classes_interfaces(self.area_texto.get(1.0, tk.END))
            if not estruturas:
                return

            output_final = ""
            for estrutura in estruturas:
                nome_classe = estrutura.get("class", "ClasseDesconhecida")
                metodos = estrutura.get("methods", {})
                output_final += f"\U0001F4D8 Análise da Classe Java: **{nome_classe}**\n\n"

                for nome_metodo, dados in metodos.items():
                    assinatura = dados.get("signature", "")
                    corpo = "\n".join(dados.get("body", []))
                    try:
                        resposta = self.ai_manager.analisar_metodo(nome_classe, nome_metodo, assinatura, corpo)
                        output_final += f"🔹 Método: **{nome_metodo}**\n{resposta}\n\n"
                    except Exception as e:
                        output_final += f"⚠️ Erro ao analisar o método {nome_metodo}:\n{e}\n\n"

            self.area_texto.delete(1.0, tk.END)
            self.area_texto.insert(tk.END, output_final)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao enviar para IA:\n{e}")
