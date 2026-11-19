# Reporta errores de sintaxis.

from antlr4.error.ErrorListener import ErrorListener

from src.ErroresSemanticos import ErrorSintacticoDataDSL


class DataDSLErrorListener(ErrorListener):
    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        # Incluye linea y columna.
        raise ErrorSintacticoDataDSL(
            f"Error sintactico en linea {line}, columna {column}: {msg}"
        )
