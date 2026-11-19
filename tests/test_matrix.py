# Pruebas de matrices propias.

import unittest

from librerias.DataMatrix import (
    transpuesta,
    multiplicar_matrices,
    determinante,
    inversa,
)


class TestDataMatrix(unittest.TestCase):
    def test_transpuesta(self):
        # Intercambia filas y columnas.
        self.assertEqual(transpuesta([[1, 2], [3, 4]]), [[1, 3], [2, 4]])

    def test_producto(self):
        # Multiplica matrices.
        resultado = multiplicar_matrices([[1, 2]], [[3], [4]])
        self.assertEqual(resultado, [[11]])

    def test_determinante(self):
        # Calcula determinante.
        self.assertAlmostEqual(determinante([[1, 2], [3, 4]]), -2)

    def test_inversa(self):
        # Comprueba un valor de la inversa.
        resultado = inversa([[1, 2], [3, 4]])
        self.assertAlmostEqual(resultado[0][0], -2.0)


if __name__ == "__main__":
    unittest.main()
