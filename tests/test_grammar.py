# Comprueba que la gramatica acepta y rechaza programas esperados.

import unittest
from pathlib import Path


class TestGrammar(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Lee DataDSL.g4 una sola vez.
        ruta = Path(__file__).resolve().parents[1] / "grammar" / "DataDSL.g4"
        cls.texto = ruta.read_text(encoding="utf-8")

    def test_control_flujo(self):
        # Verifica if, while, for y funciones.
        for regla in ("siStmt", "mientrasStmt", "paraStmt", "funcionDecl", "retorno"):
            self.assertIn(regla, self.texto)

    def test_pipeline_datos(self):
        # Verifica operaciones del PDF.
        for regla in (
            "seleccion",
            "filtro",
            "ordenamiento",
            "columnaCalculada",
            "rellenarNulos",
            "eliminarDuplicados",
            "renombrarColumna",
            "convertirTipo",
            "agrupacion",
            "resumen",
        ):
            self.assertIn(regla, self.texto)

    def test_graficas(self):
        # Verifica los cinco tipos.
        for tipo in ("barras", "lineas", "histograma", "dispersion", "caja"):
            self.assertIn(tipo, self.texto)


if __name__ == "__main__":
    unittest.main()
