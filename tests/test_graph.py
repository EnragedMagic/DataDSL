# Pruebas de graficas PNG.

import tempfile
import unittest
from pathlib import Path

from librerias.DataGraph import graficar
from librerias.DataTable import TablaDatos


class TestDataGraph(unittest.TestCase):
    def setUp(self):
        # Crea una tabla para graficar.
        self.tabla = TablaDatos(
            ["x", "y"],
            [
                {"x": 1, "y": 2},
                {"x": 2, "y": 4},
                {"x": 3, "y": 3},
                {"x": 4, "y": 5},
            ],
        )

    def test_cinco_graficas(self):
        # Verifica los cinco PNG.
        with tempfile.TemporaryDirectory() as carpeta:
            casos = [
                ("barras", "x", "y"),
                ("lineas", "x", "y"),
                ("histograma", "x", None),
                ("dispersion", "x", "y"),
                ("caja", None, "y"),
            ]
            for tipo, x, y in casos:
                ruta = Path(carpeta) / f"{tipo}.png"
                graficar(tipo, self.tabla, x=x, y=y, titulo=tipo, ruta=ruta)
                self.assertTrue(ruta.exists())
                self.assertGreater(ruta.stat().st_size, 1000)


if __name__ == "__main__":
    unittest.main()
