# Motor tabular propio de DataDSL.

from librerias.DataStats import media, mediana, minimo, maximo, desviacion
from librerias.DataTable import TablaDatos, AgrupacionDatos
from src.ErroresSemanticos import (
    ArchivoNoExisteError,
    ColumnaNoExisteError,
    TipoIncompatibleError,
    OperacionNoPermitidaError,
)


class MotorDatos:
    @staticmethod
    def abrir_csv(ruta):
        # Carga CSV o XLSX en TablaDatos.
        try:
            texto = str(ruta).lower()
            if texto.endswith(".xlsx"):
                return TablaDatos.desde_xlsx(ruta)
            return TablaDatos.desde_csv(ruta)
        except FileNotFoundError:
            raise ArchivoNoExisteError(str(ruta))
        except Exception as error:
            raise OperacionNoPermitidaError(str(error)) from error

    @staticmethod
    def guardar_csv(datos, ruta):
        # Exporta TablaDatos a CSV.
        if not isinstance(datos, TablaDatos):
            raise TipoIncompatibleError("guardar requiere una TablaDatos.")
        return datos.a_csv(ruta)

    @staticmethod
    def _validar_tabla(datos):
        # Comprueba el tipo tabular.
        if not isinstance(datos, TablaDatos):
            raise TipoIncompatibleError("Se esperaba una TablaDatos.")

    @staticmethod
    def _traducir_error_columna(error):
        # Convierte KeyError a error del DSL.
        columna = str(error).strip("'")
        raise ColumnaNoExisteError(columna) from error

    @staticmethod
    def tomar_columnas(datos, columnas):
        # Selecciona columnas.
        MotorDatos._validar_tabla(datos)
        try:
            return datos.tomar(columnas)
        except KeyError as error:
            MotorDatos._traducir_error_columna(error)

    @staticmethod
    def filtrar(datos, predicado):
        # Filtra filas con una funcion.
        MotorDatos._validar_tabla(datos)
        try:
            return datos.filtrar(predicado)
        except Exception as error:
            if isinstance(error, (ColumnaNoExisteError, TipoIncompatibleError)):
                raise
            raise OperacionNoPermitidaError(f"filtro invalido: {error}") from error

    @staticmethod
    def ordenar(datos, columna, direccion="asc"):
        # Ordena filas.
        MotorDatos._validar_tabla(datos)
        try:
            return datos.ordenar(columna, direccion)
        except KeyError as error:
            MotorDatos._traducir_error_columna(error)

    @staticmethod
    def crear_columna(datos, nombre, generador):
        # Crea una columna calculada.
        MotorDatos._validar_tabla(datos)
        return datos.crear_columna(nombre, generador)

    @staticmethod
    def rellenar_nulos(datos, columna, valor):
        # Reemplaza valores nulos.
        MotorDatos._validar_tabla(datos)
        try:
            return datos.rellenar_nulos(columna, valor)
        except KeyError as error:
            MotorDatos._traducir_error_columna(error)

    @staticmethod
    def eliminar_nulos(datos, columnas):
        # Elimina filas con nulos.
        MotorDatos._validar_tabla(datos)
        try:
            return datos.eliminar_nulos(columnas)
        except KeyError as error:
            MotorDatos._traducir_error_columna(error)

    @staticmethod
    def eliminar_duplicados(datos):
        # Elimina filas duplicadas.
        MotorDatos._validar_tabla(datos)
        return datos.eliminar_duplicados()

    @staticmethod
    def renombrar(datos, anterior, nuevo):
        # Renombra una columna.
        MotorDatos._validar_tabla(datos)
        try:
            return datos.renombrar(anterior, nuevo)
        except KeyError as error:
            MotorDatos._traducir_error_columna(error)

    @staticmethod
    def convertir(datos, columna, tipo):
        # Convierte el tipo de una columna.
        MotorDatos._validar_tabla(datos)
        try:
            return datos.convertir(columna, tipo)
        except KeyError as error:
            MotorDatos._traducir_error_columna(error)
        except Exception as error:
            raise TipoIncompatibleError(str(error)) from error

    @staticmethod
    def agrupar(datos, columnas):
        # Agrupa por columnas.
        MotorDatos._validar_tabla(datos)
        try:
            return datos.agrupar(columnas)
        except KeyError as error:
            MotorDatos._traducir_error_columna(error)

    @staticmethod
    def resumir(agrupados, agregaciones):
        # Resume cada grupo.
        if not isinstance(agrupados, AgrupacionDatos):
            raise TipoIncompatibleError("resumir requiere un agrupamiento.")

        columnas_salida = list(agrupados.columnas) + [nombre for nombre, _, _ in agregaciones]
        filas_salida = []

        for clave, filas in agrupados.items():
            salida = {col: valor for col, valor in zip(agrupados.columnas, clave)}
            for nombre, funcion, columna in agregaciones:
                if funcion == "contar":
                    salida[nombre] = len(filas)
                    continue

                if columna not in agrupados.tabla.columnas:
                    raise ColumnaNoExisteError(columna)
                valores = [fila.get(columna) for fila in filas if fila.get(columna) is not None]
                operaciones = {
                    "suma": lambda x: sum(float(v) for v in x),
                    "media": media,
                    "mediana": mediana,
                    "minimo": minimo,
                    "maximo": maximo,
                    "desviacion": desviacion,
                }
                if funcion not in operaciones:
                    raise OperacionNoPermitidaError(f"Agregacion desconocida: {funcion}")
                salida[nombre] = operaciones[funcion](valores)
            filas_salida.append(salida)

        return TablaDatos(columnas_salida, filas_salida)

    @staticmethod
    def columna(datos, nombre):
        # Devuelve una columna como lista.
        MotorDatos._validar_tabla(datos)
        try:
            return datos.columna(str(nombre))
        except KeyError as error:
            MotorDatos._traducir_error_columna(error)

    @staticmethod
    def matriz_columnas(datos, columnas):
        # Convierte columnas en matriz.
        MotorDatos._validar_tabla(datos)
        try:
            return datos.matriz_columnas(columnas)
        except KeyError as error:
            MotorDatos._traducir_error_columna(error)

    @staticmethod
    def filas(datos):
        # Cuenta filas.
        MotorDatos._validar_tabla(datos)
        return len(datos)

    @staticmethod
    def nombres_columnas(datos):
        # Lista columnas.
        MotorDatos._validar_tabla(datos)
        return datos.nombres_columnas()
