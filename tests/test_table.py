# Comprueba la lectura y las operaciones sobre tablas.

import tempfile
import unittest
from pathlib import Path

from librerias.DataTable import TablaDatos


class TestTablaDatos(unittest.TestCase):
    def setUp(self):
        # Crea datos simples.
        self.tabla = TablaDatos(
            ["ciudad", "cantidad", "precio"],
            [
                {"ciudad": "Bogota", "cantidad": 2, "precio": 10},
                {"ciudad": "Cali", "cantidad": 1, "precio": None},
                {"ciudad": "Bogota", "cantidad": 3, "precio": 20},
            ],
        )

    def test_tomar_columnas(self):
        # Conserva columnas elegidas.
        resultado = self.tabla.tomar(["ciudad", "precio"])
        self.assertEqual(resultado.columnas, ["ciudad", "precio"])

    def test_filtrar(self):
        # Conserva filas verdaderas.
        resultado = self.tabla.filtrar(lambda fila, _: fila["cantidad"] > 1)
        self.assertEqual(len(resultado), 2)

    def test_crear_columna(self):
        # Crea una columna calculada.
        resultado = self.tabla.crear_columna(
            "total",
            lambda fila, _: fila["cantidad"] * (fila["precio"] or 0),
        )
        self.assertEqual(resultado.filas[0]["total"], 20)

    def test_nulos_y_conversion(self):
        # Rellena nulos y convierte tipos.
        resultado = self.tabla.rellenar_nulos("precio", 0).convertir("precio", "decimal")
        self.assertEqual(resultado.filas[1]["precio"], 0.0)

    def test_csv(self):
        # Guarda y vuelve a cargar CSV.
        with tempfile.TemporaryDirectory() as carpeta:
            ruta = Path(carpeta) / "tabla.csv"
            self.tabla.a_csv(ruta)
            cargada = TablaDatos.desde_csv(ruta)
            self.assertEqual(len(cargada), 3)
            self.assertEqual(cargada.columnas, self.tabla.columnas)


if __name__ == "__main__":
    unittest.main()
