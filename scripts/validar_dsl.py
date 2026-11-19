# Valida programas escritos en DataDSL.

from pathlib import Path
import sys


RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ))

from main import ejecutar


PROGRAMAS = [
    "programa1.dsl",
    "programa2.dsl",
    "programa3.dsl",
    "control.dsl",
    "funciones.dsl",
    "ml.dsl",
    "graficas.dsl",
    "programa_final.dsl",
]


def main():
    # Exige primero el Parser generado.
    if not (RAIZ / "generated" / "DataDSLParser.py").exists():
        print("Falta ANTLR generado. Ejecuta: bash generar_antlr.sh")
        return 1

    # Ejecuta todos los ejemplos.
    for nombre in PROGRAMAS:
        print(f"\n=== {nombre} ===")
        ejecutar(RAIZ / "ejemplos" / nombre)

    print("\nVALIDACION DSL: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
