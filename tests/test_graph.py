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

    def test_visualizaciones_ml(self):
        # Verifica que los tres algoritmos pueden producir imagenes PNG.
        from librerias.DataGraph import graficar_regresion, graficar_knn, graficar_kmeans
        from librerias.DataML import entrenar_regresion, entrenar_knn, kmeans
        with tempfile.TemporaryDirectory() as carpeta:
            t = TablaDatos(["x", "y"], [
                {"x": 1, "y": 3}, {"x": 2, "y": 5}, {"x": 3, "y": 7}
            ])
            r = Path(carpeta) / "reg.png"
            graficar_regresion(t, entrenar_regresion(t, ["x"], "y"), "x", "y", r)
            self.assertGreater(r.stat().st_size, 1000)

            c = TablaDatos(["x", "y", "clase"], [
                {"x": 1, "y": 1, "clase": 0}, {"x": 2, "y": 2, "clase": 0},
                {"x": 8, "y": 8, "clase": 1}, {"x": 9, "y": 9, "clase": 1},
            ])
            r = Path(carpeta) / "knn.png"
            graficar_knn(c, entrenar_knn(c, ["x", "y"], "clase", 3), [8, 7], "x", "y", r)
            self.assertGreater(r.stat().st_size, 1000)

            r = Path(carpeta) / "kmeans.png"
            graficar_kmeans(t, kmeans(t, ["x", "y"], 2), "x", "y", r)
            self.assertGreater(r.stat().st_size, 1000)

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
