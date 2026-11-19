# Pruebas de estadistica propia.

import unittest

from librerias.DataStats import media, mediana, varianza, desviacion, correlacion


class TestDataStats(unittest.TestCase):
    def test_media_mediana(self):
        # Verifica medidas centrales.
        self.assertEqual(media([1, 2, 3, 4]), 2.5)
        self.assertEqual(mediana([4, 1, 3, 2]), 2.5)

    def test_dispersion(self):
        # Verifica varianza y desviacion.
        self.assertAlmostEqual(varianza([1, 2, 3]), 2 / 3)
        self.assertGreater(desviacion([1, 2, 3]), 0)

    def test_correlacion(self):
        # Verifica relacion lineal perfecta.
        self.assertAlmostEqual(correlacion([1, 2, 3], [2, 4, 6]), 1.0)


if __name__ == "__main__":
    unittest.main()
