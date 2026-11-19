# Punto de entrada de DataDSL.

import sys
from pathlib import Path

from antlr4 import FileStream, CommonTokenStream


def _cargar_componentes():
    # Importa archivos generados por ANTLR.
    try:
        from generated.DataDSLLexer import DataDSLLexer
        from generated.DataDSLParser import DataDSLParser
        from src.DataDSLVisitorImpl import DataDSLVisitorImpl
        return DataDSLLexer, DataDSLParser, DataDSLVisitorImpl
    except ModuleNotFoundError as error:
        if "generated.DataDSL" in str(error) or "DataDSLVisitor" in str(error):
            raise RuntimeError(
                "Falta generar ANTLR. Ejecuta: bash generar_antlr.sh"
            ) from error
        raise


def ejecutar(ruta):
    # Ejecuta un archivo .dsl.
    ruta = Path(str(ruta))
    if not ruta.exists():
        raise FileNotFoundError(str(ruta))

    DataDSLLexer, DataDSLParser, DataDSLVisitorImpl = _cargar_componentes()
    from ErrorListener import DataDSLErrorListener

    entrada = FileStream(str(ruta), encoding="utf-8")
    lexer = DataDSLLexer(entrada)
    tokens = CommonTokenStream(lexer)
    parser = DataDSLParser(tokens)

    # Reemplaza mensajes genericos.
    parser.removeErrorListeners()
    parser.addErrorListener(DataDSLErrorListener())

    arbol = parser.programa()
    visitor = DataDSLVisitorImpl()
    return visitor.visit(arbol)


def main():
    # Lee la ruta desde terminal.
    if len(sys.argv) != 2:
        print("Uso: python3 main.py archivo.dsl")
        return 1
    try:
        ejecutar(sys.argv[1])
        return 0
    except Exception as error:
        print(f"[DataDSL] {error}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
