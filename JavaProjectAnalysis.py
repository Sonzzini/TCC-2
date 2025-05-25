import os

class JavaAnalyzer:
    def __init__(self, root_directory):
        self.root_directory = root_directory
        self.total_lines = 0
        self.total_classes = 0
        self.total_methods = 0
        self.class_line_counts = []  # (class_name, lines)
        self.method_line_counts = []  # (method_name, lines)

    def analyze_file(self, file_path):
        inside_class = False
        inside_method = False
        current_class_lines = 0
        current_method_lines = 0

        with open(file_path, "r", encoding="utf-8", errors="ignore") as file:
            for line in file:
                stripped_line = line.strip()
                self.total_lines += 1

                # Detecting class definition
                if "class " in stripped_line and not inside_class:
                    self.total_classes += 1
                    inside_class = True
                    current_class_lines = 0

                if inside_class:
                    current_class_lines += 1

                    # Detecting method definition
                    if "(" in stripped_line and ")" in stripped_line and "{" in stripped_line:
                        self.total_methods += 1
                        inside_method = True
                        current_method_lines = 0

                    if inside_method:
                        current_method_lines += 1
                        if "}" in stripped_line:
                            self.method_line_counts.append(("Method", current_method_lines))
                            inside_method = False

                    # Closing class
                    if "}" in stripped_line and not inside_method:
                        self.class_line_counts.append(("Class", current_class_lines))
                        inside_class = False

    def analyze_project(self):
        for root, _, files in os.walk(self.root_directory):
            for file in files:
                if file.endswith(".java"):
                    file_path = os.path.join(root, file)
                    self.analyze_file(file_path)

    def report(self):
        print(f"Total de Arquivos (.java): {len(self.class_line_counts)}")
        print(f"Total de Classes: {self.total_classes}")
        print(f"Total de Métodos: {self.total_methods}")
        print(f"Total de Linhas: {self.total_lines}")

        if self.total_classes > 0:
            print(f"Média de Linhas por Classe: {sum(count for _, count in self.class_line_counts) / self.total_classes:.2f}")

        if self.total_methods > 0:
            print(f"Média de Linhas por Método: {sum(count for _, count in self.method_line_counts) / self.total_methods:.2f}")


if __name__ == "__main__":
    project_path = input("Digite o caminho do projeto Java: ").strip()
    analyzer = JavaAnalyzer(project_path)
    analyzer.analyze_project()
    analyzer.report()
