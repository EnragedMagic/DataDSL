# Comprueba que las variables y los ambitos se recuerdan correctamente.

import unittest

from src.ContextoEjecucion import ContextoEjecucion
from src.ErroresSemanticos import VariableNoDefinidaError


class TestContexto(unittest.TestCase):
    def test_guardar_obtener(self):
        # Guarda y recupera una variable.
        contexto = ContextoEjecucion()
        contexto.guardar("x", 10, "numero")
        self.assertEqual(contexto.obtener("x"), 10)
        self.assertEqual(contexto.obtener_tipo("x"), "numero")

    def test_ambito_local(self):
        # El ambito local desaparece al salir.
        contexto = ContextoEjecucion()
        contexto.entrar_ambito({"local": 7})
        self.assertEqual(contexto.obtener("local"), 7)
        contexto.salir_ambito()
        with self.assertRaises(VariableNoDefinidaError):
            contexto.obtener("local")


if __name__ == "__main__":
    unittest.main()
