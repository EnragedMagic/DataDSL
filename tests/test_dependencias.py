# Pruebas de independencia del proyecto.

import unittest
from pathlib import Path


class TestDependencias(unittest.TestCase):
    def test_sin_librerias_prohibidas(self):
        # Evita pandas, numpy, sklearn y pytest.
        raiz = Path(__file__).resolve().parents[1]
        prohibidas = ("import pandas", "import numpy", "sklearn", "import pytest", "from pytest")
        carpetas = [raiz / "src", raiz / "librerias", raiz / "tests"]
        encontrados = []
        for carpeta in carpetas:
            for archivo in carpeta.rglob("*.py"):
                texto = archivo.read_text(encoding="utf-8").lower()
                for palabra in prohibidas:
                    if palabra in texto and archivo.name != "test_dependencias.py":
                        encontrados.append(f"{archivo.name}: {palabra}")
        self.assertEqual(encontrados, [])

    def test_requirements_minimos(self):
        # Solo permite ANTLR y Matplotlib externos.
        raiz = Path(__file__).resolve().parents[1]
        lineas = [
            linea.strip().lower()
            for linea in (raiz / "requirements.txt").read_text(encoding="utf-8").splitlines()
            if linea.strip() and not linea.startswith("#")
        ]
        self.assertEqual(len(lineas), 2)
        self.assertTrue(any("antlr4-python3-runtime" in linea for linea in lineas))
        self.assertTrue(any("matplotlib" in linea for linea in lineas))


if __name__ == "__main__":
    unittest.main()
