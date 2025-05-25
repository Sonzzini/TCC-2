import os
import json
from tqdm import tqdm
import antlr4
from antlr4 import FileStream, CommonTokenStream
from JavaParserListener import JavaParserListener
from JavaLexer import JavaLexer
from JavaParser import JavaParser

class JavaProjectAnalyzer:
    def __init__(self, project_path):
        self.project_path = project_path
        self.total_files = 0
        self.total_classes = 0
        self.total_methods = 0
        self.total_lines = 0

    def analyze(self):
        java_files = []
        for root, _, files in os.walk(self.project_path):
            for file in files:
                if file.endswith('.java'):
                    file_path = os.path.join(root, file)
                    java_files.append(file_path)

        self.total_files = len(java_files)

        for file_path in tqdm(java_files, desc="Analisando arquivos Java"):
            self.process_file(file_path)

    def process_file(self, file_path):
        try:
            input_stream = FileStream(file_path, encoding='utf-8')
            lexer = JavaLexer(input_stream)
            token_stream = CommonTokenStream(lexer)
            parser = JavaParser(token_stream)
            tree = parser.compilationUnit()

            listener = JavaStructureListener()
            walker = antlr4.ParseTreeWalker()
            walker.walk(listener, tree)

            self.total_classes += listener.class_count
            self.total_methods += listener.method_count
            self.total_lines += listener.line_count
        except Exception as e:
            print(f"Erro ao processar o arquivo: {file_path} - {str(e)}")

    def generate_json_per_class(self, output_path="classes_json", output_file="project_structure.json"):
        os.makedirs(output_path, exist_ok=True)
        all_classes = []
        for root, _, files in os.walk(self.project_path):
            for file in files:
                if file.endswith('.java'):
                    file_path = os.path.join(root, file)
                    try:
                        input_stream = FileStream(file_path, encoding='utf-8')
                        lexer = JavaLexer(input_stream)
                        token_stream = CommonTokenStream(lexer)
                        parser = JavaParser(token_stream)
                        tree = parser.compilationUnit()

                        listener = JavaStructureListener()
                        walker = antlr4.ParseTreeWalker()
                        walker.walk(listener, tree)

                        for class_data in listener.classes:
                            class_json = {
                                "class_name": class_data.get("name", "UnnamedClass"),
                                "methods": class_data.get("methods", []),
                                "attributes": class_data.get("attributes", []),
                                "visibility": class_data.get("visibility", "package-private"),
                                "extends": class_data.get("extends", None),
                                "implements": class_data.get("implements", [])
                            }
                            all_classes.append(class_json)
                    except Exception as e:
                        print(f"Erro ao processar o arquivo para JSON: {file_path} - {str(e)}")

        output_path_file = os.path.join(output_path, output_file)
        with open(output_path_file, "w", encoding="utf-8") as f:
            json.dump(all_classes, f, indent=4, ensure_ascii=False)

    def report(self):
        print(f"Total de Arquivos (.java): {self.total_files}")
        print(f"Total de Classes: {self.total_classes}")
        print(f"Total de Métodos: {self.total_methods}")
        print(f"Total de Linhas: {self.total_lines}")
        if self.total_classes > 0:
            print(f"Média de Linhas por Classe: {self.total_lines / self.total_classes:.2f}")
        if self.total_methods > 0:
            print(f"Média de Linhas por Método: {self.total_lines / self.total_methods:.2f}")

class JavaStructureListener(JavaParserListener):
    def __init__(self):
        self.class_count = 0
        self.method_count = 0
        self.line_count = 0
        self.classes = []

    def enterClassDeclaration(self, ctx):
        self.class_count += 1
        class_name = ctx.identifier().getText() if ctx.identifier() else "UnnamedClass"
        extends = ctx.typeType().getText() if ctx.typeType() else None
        implements = []
        try:
            if hasattr(ctx, "typeList") and ctx.typeList():
                if hasattr(ctx.typeList(), "typeType"):
                    implements = [impl.getText() for impl in ctx.typeList().typeType()]
        except Exception:
            implements = []

        visibility = "package-private"
        if ctx.parentCtx and hasattr(ctx.parentCtx, "modifier"):
            modifiers = [mod.getText() for mod in ctx.parentCtx.modifier()]
            if "public" in modifiers:
                visibility = "public"
            elif "private" in modifiers:
                visibility = "private"
            elif "protected" in modifiers:
                visibility = "protected"

        self.classes.append({
            "name": class_name,
            "methods": [],
            "attributes": [],
            "visibility": visibility,
            "extends": extends,
            "implements": implements
        })

    def enterMethodDeclaration(self, ctx):
        method_name = ctx.identifier().getText()
        start_line = ctx.start.line
        end_line = ctx.stop.line
        parameters = ctx.formalParameters().getText()
        visibility = "package-private"

        if ctx.parentCtx and hasattr(ctx.parentCtx, "modifier"):
            modifiers = [mod.getText() for mod in ctx.parentCtx.modifier()]
            if "public" in modifiers:
                visibility = "public"
            elif "private" in modifiers:
                visibility = "private"
            elif "protected" in modifiers:
                visibility = "protected"

        if self.classes:
            self.method_count += 1
            self.line_count += end_line - start_line + 1
            self.classes[-1]["methods"].append({
                "name": method_name,
                "parameters": parameters,
                "start_line": start_line,
                "end_line": end_line,
                "visibility": visibility
            })

    def enterFieldDeclaration(self, ctx):
        if not self.classes:
            return

        type_text = ctx.typeType().getText()
        visibility = "package-private"

        if ctx.parentCtx and hasattr(ctx.parentCtx, "modifier"):
            modifiers = [mod.getText() for mod in ctx.parentCtx.modifier()]
            if "public" in modifiers:
                visibility = "public"
            elif "private" in modifiers:
                visibility = "private"
            elif "protected" in modifiers:
                visibility = "protected"

        for var_decl in ctx.variableDeclarators().variableDeclarator():
            attr_name = var_decl.variableDeclaratorId().getText()
            self.classes[-1]["attributes"].append({
                "name": attr_name,
                "type": type_text,
                "visibility": visibility
            })

if __name__ == '__main__':
    project_path = input("Digite o caminho do projeto Java: ")
    analyzer = JavaProjectAnalyzer(project_path)
    analyzer.analyze()
    analyzer.report()

    analyzer.generate_json_per_class()
