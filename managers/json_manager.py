import javalang

class JsonManager:

    def __init__(self):
        print("JsonManager inicializado.")
    
    def javalang_parser(self, codigo_java: str):
        try:
            tree = javalang.parse.parse(codigo_java)
            return tree
        except Exception as e:
            print(f"Erro ao analisar o código Java: {e}")
            return None
        
    def extrair_classes_interfaces_javalang(self, codigo_java: str):
        """
        Extracts classes and interfaces from Java code using the javalang library.

        This method parses the provided Java source code and identifies all class and interface
        declarations. For each class or interface, it extracts its name, type (class or interface),
        and methods. Each method includes its signature and body.

        Args:
            codigo_java (str): The Java source code as a string.

        Returns:
            list: A list of dictionaries, where each dictionary represents a class or interface with
                  the following structure:
                  - "type" (str): Either "class" or "interface".
                  - "name" (str): The name of the class or interface.
                  - "methods" (dict): A dictionary of methods, where the key is the method name and
                    the value is another dictionary with:
                    - "signature" (str): The method's signature, including modifiers, return type,
                      name, and parameters.
                    - "body" (list): A list of strings representing the statements in the method body.

        Notes:
            - This method relies on the `javalang` library to parse the Java code.
            - If the provided Java code cannot be parsed, an empty list is returned.
            - The method body is represented as a list of strings, which may require further
              processing for detailed analysis.

        Example:
            >>> codigo_java = '''
            ... public class Example {
            ...     public void sayHello() {
            ...         System.out.println("Hello, world!");
            ...     }
            ... }
            ... '''
            >>> manager = JsonManager()
            >>> result = manager.extrair_classes_interfaces_javalang(codigo_java)
            >>> print(result)
            [{'type': 'class', 'name': 'Example', 'methods': {'sayHello': {'signature': 'public void sayHello()', 'body': ['System.out.println("Hello, world!");']}}}]
        """
        tree = self.javalang_parser(codigo_java)
        if not tree:
            return []

        classes_interfaces = []
        for node in tree.types:
            if isinstance(node, (javalang.tree.ClassDeclaration, javalang.tree.InterfaceDeclaration)):
                tipo = "class" if isinstance(node, javalang.tree.ClassDeclaration) else "interface"
                metodos = {}
                for method in node.methods:
                    metodo_corpo = []
                    if method.body:
                        for statement in method.body:
                            metodo_corpo.append(str(statement))
                    metodos[method.name] = {
                        "signature": f"{' '.join(method.modifiers)} {method.return_type.name if method.return_type else 'void'} {method.name}({', '.join([f'{p.type.name} {p.name}' for p in method.parameters])})",
                        "body": metodo_corpo
                    }
                classes_interfaces.append({
                    "type": tipo,
                    "name": node.name,
                    "methods": metodos
                })

        return classes_interfaces
