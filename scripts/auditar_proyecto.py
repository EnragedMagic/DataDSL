# Auditoria simple de DataDSL.

from pathlib import Path


RAIZ = Path(__file__).resolve().parents[1]
PROHIBIDAS = ("import pandas", "import numpy", "sklearn", "import pytest", "from pytest")


def revisar_dependencias():
    # Busca imports no permitidos.
    fallos = []
    for carpeta in (RAIZ / "src", RAIZ / "librerias", RAIZ / "tests"):
        for archivo in carpeta.rglob("*.py"):
            texto = archivo.read_text(encoding="utf-8").lower()
            for palabra in PROHIBIDAS:
                if palabra in texto and archivo.name not in {"test_dependencias.py", "auditar_proyecto.py"}:
                    fallos.append(f"{archivo}: {palabra}")
    return fallos


def revisar_comentarios():
    # Comprueba que cada Python tenga comentarios.
    fallos = []
    for carpeta in (RAIZ / "src", RAIZ / "librerias", RAIZ / "tests"):
        for archivo in carpeta.rglob("*.py"):
            if archivo.name == "__init__.py":
                continue
            lineas = archivo.read_text(encoding="utf-8").splitlines()
            comentarios = [l for l in lineas if l.strip().startswith("#")]
            if len(comentarios) < 2:
                fallos.append(str(archivo))
    return fallos


def main():
    # Imprime el resultado de auditoria.
    dependencias = revisar_dependencias()
    comentarios = revisar_comentarios()
    if dependencias or comentarios:
        print("AUDITORIA: FALLA")
        for fallo in dependencias:
            print("Dependencia:", fallo)
        for fallo in comentarios:
            print("Comentarios:", fallo)
        return 1
    print("AUDITORIA: OK")
    print("Sin pandas, numpy, sklearn ni pytest.")
    print("Archivos Python principales con comentarios.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
