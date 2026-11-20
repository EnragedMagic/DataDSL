# Comprueba operaciones de lectura y escritura de archivos.

import tempfile
import unittest
from pathlib import Path

from librerias.DataFiles import escribir_texto, leer_texto, agregar_texto


class TestDataFiles(unittest.TestCase):
    def test_escribir_y_leer(self):
        # Escribe y recupera texto.
        with tempfile.TemporaryDirectory() as carpeta:
            ruta = Path(carpeta) / "nota.txt"
            escribir_texto(ruta, "hola")
            self.assertEqual(leer_texto(ruta), "hola")

    def test_agregar(self):
        # Agrega contenido al final.
        with tempfile.TemporaryDirectory() as carpeta:
            ruta = Path(carpeta) / "nota.txt"
            escribir_texto(ruta, "a")
            agregar_texto(ruta, "b")
            self.assertEqual(leer_texto(ruta), "ab")


if __name__ == "__main__":
    unittest.main()
