# Comprueba operaciones completas desde la entrada hasta los resultados.

import tempfile
import unittest
from pathlib import Path

from librerias.DataGraph import graficar
from librerias.DataML import entrenar_regresion, predecir_lineal
from librerias.DataTable import TablaDatos
from src.MotorDatos import MotorDatos


class TestIntegracion(unittest.TestCase):
    def test_flujo_completo(self):
        # Ejecuta datos, estadistica, ML y grafica.
        tabla = TablaDatos(
            ["ciudad", "cantidad", "precio"],
            [
                {"ciudad": "Bogota", "cantidad": 2, "precio": 10},
                {"ciudad": "Bogota", "cantidad": 3, "precio": 20},
                {"ciudad": "Cali", "cantidad": 1, "precio": 15},
            ],
        )
        tabla = MotorDatos.crear_columna(
            tabla,
            "total",
            lambda fila, _: fila["cantidad"] * fila["precio"],
        )
        grupos = MotorDatos.agrupar(tabla, ["ciudad"])
        resumen = MotorDatos.resumir(grupos, [("ingreso", "suma", "total")])

        regresion = TablaDatos(
            ["x", "y"],
            [{"x": 1, "y": 3}, {"x": 2, "y": 5}, {"x": 3, "y": 7}],
        )
        modelo = entrenar_regresion(regresion, ["x"], "y")
        prediccion = predecir_lineal(modelo, [[4]])

        with tempfile.TemporaryDirectory() as carpeta:
            csv_salida = Path(carpeta) / "resumen.csv"
            png_salida = Path(carpeta) / "resumen.png"
            MotorDatos.guardar_csv(resumen, csv_salida)
            graficar("barras", resumen, x="ciudad", y="ingreso", ruta=png_salida)
            self.assertTrue(csv_salida.exists())
            self.assertTrue(png_salida.exists())
            self.assertAlmostEqual(prediccion, 9, places=6)


if __name__ == "__main__":
    unittest.main()
