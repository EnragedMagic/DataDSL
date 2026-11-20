#!/usr/bin/env bash
set -e

# Activa el entorno si existe.
if [ -d .venv ]; then
    source .venv/bin/activate
fi

# Genera ANTLR si hace falta.
if [ ! -f generated/DataDSLParser.py ]; then
    bash generar_antlr.sh
fi

# Ejecuta los programas principales.
python3 main.py ejemplos/programa1.dsl
python3 main.py ejemplos/programa2.dsl
python3 main.py ejemplos/programa3.dsl
python3 main.py ejemplos/control.dsl
python3 main.py ejemplos/funciones.dsl
python3 main.py ejemplos/ml.dsl
python3 main.py ejemplos/graficas.dsl
python3 main.py ejemplos/programa_final.dsl

# Genera las tres visualizaciones de Machine Learning.
python3 main.py ejemplos/ml_regresion.dsl
python3 main.py ejemplos/ml_knn.dsl
python3 main.py ejemplos/ml_kmeans.dsl

# Ejecuta todas las pruebas.
python3 -m unittest discover -s tests -v

echo "Demo terminada. Revisa salidas/."
