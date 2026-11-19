# Errores propios de DataDSL.


class ErrorDataDSL(Exception):
    # Error base del lenguaje.
    pass


class VariableNoDefinidaError(ErrorDataDSL):
    def __init__(self, nombre):
        # Variable no declarada.
        super().__init__(f"Variable no definida: '{nombre}'.")


class ColumnaNoExisteError(ErrorDataDSL):
    def __init__(self, columna):
        # Columna ausente en la tabla.
        super().__init__(f"Columna inexistente: '{columna}'.")


class TipoIncompatibleError(ErrorDataDSL):
    def __init__(self, mensaje):
        # Tipo invalido para una operacion.
        super().__init__(f"Tipo incompatible: {mensaje}")


class OperacionNoPermitidaError(ErrorDataDSL):
    def __init__(self, mensaje):
        # Operacion invalida en ejecucion.
        super().__init__(f"Operacion no permitida: {mensaje}")


class ArchivoNoExisteError(ErrorDataDSL):
    def __init__(self, ruta):
        # Archivo que no existe.
        super().__init__(f"Archivo no encontrado: '{ruta}'.")


class ErrorSintacticoDataDSL(ErrorDataDSL):
    # Error reportado por ANTLR.
    pass
