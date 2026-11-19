# Pruebas del generador propio.

import unittest

from librerias.DataRandom import semilla, aleatorio, aleatorio_entero


class TestDataRandom(unittest.TestCase):
    def test_repetible(self):
        # Misma semilla produce mismo valor.
        semilla(100)
        primero = aleatorio()
        semilla(100)
        segundo = aleatorio()
        self.assertEqual(primero, segundo)

    def test_entero_en_rango(self):
        # Mantiene limites indicados.
        semilla(5)
        valor = aleatorio_entero(1, 5)
        self.assertTrue(1 <= valor <= 5)


if __name__ == "__main__":
    unittest.main()
