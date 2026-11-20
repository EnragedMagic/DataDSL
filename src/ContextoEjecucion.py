# Recuerda variables, tipos y funciones mientras corre el programa.

from src.ErroresSemanticos import VariableNoDefinidaError


class ContextoEjecucion:
    def __init__(self):
        # Pila de ambitos y tipos.
        self.ambitos = [{}]
        self.tipos = [{}]
        self.funciones = {}

    def entrar_ambito(self, inicial=None):
        # Crea memoria local.
        self.ambitos.append(dict(inicial or {}))
        self.tipos.append({})

    def salir_ambito(self):
        # Cierra memoria local.
        if len(self.ambitos) == 1:
            raise RuntimeError("No se puede cerrar el ambito global.")
        self.ambitos.pop()
        self.tipos.pop()

    def guardar(self, nombre, valor, tipo=None):
        # Actualiza la variable visible.
        for indice in range(len(self.ambitos) - 1, -1, -1):
            if nombre in self.ambitos[indice]:
                self.ambitos[indice][nombre] = valor
                if tipo:
                    self.tipos[indice][nombre] = tipo
                return valor
        self.ambitos[-1][nombre] = valor
        if tipo:
            self.tipos[-1][nombre] = tipo
        return valor

    def obtener(self, nombre):
        # Busca una variable visible.
        for ambito in reversed(self.ambitos):
            if nombre in ambito:
                return ambito[nombre]
        raise VariableNoDefinidaError(nombre)

    def existe(self, nombre):
        # Comprueba si existe.
        return any(nombre in ambito for ambito in self.ambitos)

    def obtener_tipo(self, nombre):
        # Busca el tipo declarado.
        for tipos in reversed(self.tipos):
            if nombre in tipos:
                return tipos[nombre]
        return None

    def guardar_funcion(self, nombre, parametros, bloque):
        # Registra una funcion del DSL.
        self.funciones[nombre] = {
            "parametros": list(parametros),
            "bloque": bloque,
        }

    def obtener_funcion(self, nombre):
        # Recupera una funcion.
        return self.funciones.get(nombre)

    def mostrar_simbolos(self):
        # Une simbolos visibles.
        resultado = {}
        for ambito in self.ambitos:
            resultado.update(ambito)
        return resultado
