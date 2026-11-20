# Comprueba resultados de las funciones matematicas.

import unittest

from librerias.DataMath import raiz, factorial, mcd, seno, coseno, exponencial


class TestDataMath(unittest.TestCase):
    def test_raiz(self):
        # Verifica Newton-Raphson.
        self.assertAlmostEqual(raiz(25), 5.0, places=8)

    def test_factorial(self):
        # Verifica factorial.
        self.assertEqual(factorial(6), 720)

    def test_mcd(self):
        # Verifica Euclides.
        self.assertEqual(mcd(48, 18), 6)

    def test_trigonometria(self):
        # Verifica seno y coseno.
        self.assertAlmostEqual(seno(0), 0.0, places=8)
        self.assertAlmostEqual(coseno(0), 1.0, places=8)

    def test_exponencial(self):
        # Verifica e^1.
        self.assertAlmostEqual(exponencial(1), 2.718281828, places=6)


if __name__ == "__main__":
    unittest.main()
