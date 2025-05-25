import antlr4
from antlr4 import *
from java.antlr_unit2 import Java8Parser, Java8Lexer

def main():
    code = open('test.txt', 'r').read()
    lexer = Java8Lexer.Java8Lexer(antlr4.InputStream(code))
    stream = antlr4.CommonTokenStream(lexer)
    parser = Java8Parser.Java8Parser(stream)
    tree = parser.compilationUnit()
    print(tree.toStringTree(recog=parser))

if __name__ == '__main__':
    main()