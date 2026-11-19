# Consola sencilla de DataDSL.

from antlr4 import InputStream, CommonTokenStream

from main import _cargar_componentes


def main():
    # Mantiene el mismo Visitor entre lineas.
    DataDSLLexer, DataDSLParser, DataDSLVisitorImpl = _cargar_componentes()
    visitor = DataDSLVisitorImpl()
    print("DataDSL REPL - escribe salir para terminar")

    while True:
        texto = input("datadsl> ").strip()
        if texto.lower() == "salir":
            break
        if not texto:
            continue
        try:
            lexer = DataDSLLexer(InputStream(texto))
            parser = DataDSLParser(CommonTokenStream(lexer))
            arbol = parser.programa()
            visitor.visit(arbol)
        except Exception as error:
            print(f"[DataDSL] {error}")


if __name__ == "__main__":
    main()
