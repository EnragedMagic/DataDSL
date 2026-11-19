#!/usr/bin/env bash
set -e

# Genera Lexer, Parser y Visitor.
if ! command -v antlr4 >/dev/null 2>&1; then
    echo "No se encontro antlr4. En Ubuntu: sudo apt install antlr4"
    exit 1
fi

rm -f generated/DataDSL*.py generated/DataDSL*.tokens generated/DataDSL*.interp
cd grammar
antlr4 -Dlanguage=Python3 -visitor -no-listener -o ../generated DataDSL.g4
cd ..
touch generated/__init__.py

echo "ANTLR generado correctamente en generated/."
