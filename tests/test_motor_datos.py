# Pruebas del motor tabular.

import unittest

from librerias.DataTable import TablaDatos
from src.MotorDatos import MotorDatos


class TestMotorDatos(unittest.TestCase):
    def setUp(self):
        # Crea una tabla de ventas.
        self.tabla = TablaDatos(
            ["ciudad", "cantidad", "precio"],
            [
                {"ciudad": "Bogota", "cantidad": 2, "precio": 10},
                {"ciudad": "Bogota", "cantidad": 3, "precio": 20},
                {"ciudad": "Cali", "cantidad": 1, "precio": 15},
            ],
        )

    def test_ordenar(self):
        # Ordena de mayor a menor.
        resultado = MotorDatos.ordenar(self.tabla, "precio", "desc")
        self.assertEqual(resultado.filas[0]["precio"], 20)

    def test_renombrar(self):
        # Cambia un nombre de columna.
        resultado = MotorDatos.renombrar(self.tabla, "precio", "valor")
        self.assertIn("valor", resultado.columnas)

    def test_resumir(self):
        # Agrupa y calcula estadisticas.
        grupos = MotorDatos.agrupar(self.tabla, ["ciudad"])
        resumen = MotorDatos.resumir(
            grupos,
            [("total", "suma", "precio"), ("registros", "contar", None)],
        )
        bogota = next(f for f in resumen.filas if f["ciudad"] == "Bogota")
        self.assertEqual(bogota["total"], 30.0)
        self.assertEqual(bogota["registros"], 2)


if __name__ == "__main__":
    unittest.main()
