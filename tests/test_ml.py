# Pruebas de Machine Learning propio.

import unittest

from librerias.DataML import (
    regresion_lineal,
    predecir_lineal,
    regresion_logistica,
    predecir_logistica,
    knn,
    kmeans,
    accuracy,
)
from librerias.DataTable import TablaDatos


class TestDataML(unittest.TestCase):
    def test_regresion_lineal(self):
        # Aprende y = 2x + 1.
        modelo = regresion_lineal([[1], [2], [3], [4]], [3, 5, 7, 9])
        self.assertAlmostEqual(predecir_lineal(modelo, [[5]]), 11, places=6)

    def test_regresion_logistica(self):
        # Separa dos grupos simples.
        modelo = regresion_logistica([[0], [1], [4], [5]], [0, 0, 1, 1], 0.2, 1500)
        pred = predecir_logistica(modelo, [[0], [5]])
        self.assertEqual(pred, [0, 1])

    def test_knn(self):
        # Clasifica por vecinos.
        pred = knn([[0], [1], [10], [11]], [0, 0, 1, 1], [[9]], 3)
        self.assertEqual(pred, 1)

    def test_kmeans_tabla(self):
        # Agrupa datos desde TablaDatos.
        tabla = TablaDatos(
            ["x", "y"],
            [{"x": 1, "y": 1}, {"x": 2, "y": 2}, {"x": 9, "y": 9}, {"x": 10, "y": 10}],
        )
        modelo = kmeans(tabla, ["x", "y"], 2)
        self.assertEqual(len(modelo["centroides"]), 2)

    def test_accuracy(self):
        # Calcula exactitud.
        self.assertEqual(accuracy([1, 0, 1], [1, 0, 0]), 2 / 3)


if __name__ == "__main__":
    unittest.main()
