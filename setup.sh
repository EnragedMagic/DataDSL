#!/usr/bin/env bash
set -e

# Crea el entorno virtual.
python3 -m venv .venv
source .venv/bin/activate

# Instala solo dependencias externas justificadas.
pip install -r requirements.txt

# Genera ANTLR si esta disponible.
if command -v antlr4 >/dev/null 2>&1; then
    bash generar_antlr.sh
else
    echo "ANTLR no esta instalado. Ejecuta: sudo apt install antlr4"
fi

# Ejecuta las pruebas propias.
python3 -m unittest discover -s tests -v
