# Visitor principal de DataDSL.

import json

from generated.DataDSLVisitor import DataDSLVisitor
from librerias.DataFiles import FUNCTIONS as FILE_FUNCTIONS
from librerias.DataGraph import FUNCTIONS as GRAPH_FUNCTIONS, graficar
from librerias.DataML import FUNCTIONS as ML_FUNCTIONS
from librerias.DataMath import FUNCTIONS as MATH_FUNCTIONS, PI, E
from librerias.DataMatrix import FUNCTIONS as MATRIX_FUNCTIONS
from librerias.DataRandom import FUNCTIONS as RANDOM_FUNCTIONS
from librerias.DataStats import FUNCTIONS as STATS_FUNCTIONS
from librerias.DataTable import TablaDatos, AgrupacionDatos
from src.ContextoEjecucion import ContextoEjecucion
from src.MotorDatos import MotorDatos
from src.ErroresSemanticos import (
    VariableNoDefinidaError,
    TipoIncompatibleError,
    OperacionNoPermitidaError,
)


class _RetornoSignal(Exception):
    def __init__(self, valor):
        # Transporta el retorno.
        self.valor = valor


class DataDSLVisitorImpl(DataDSLVisitor):
    def __init__(self):
        super().__init__()
        # Crea memoria y funciones internas.
        self.contexto = ContextoEjecucion()
        self._fila_actual = None
        self.builtins = {}

        for grupo in (
            MATH_FUNCTIONS,
            STATS_FUNCTIONS,
            MATRIX_FUNCTIONS,
            RANDOM_FUNCTIONS,
            FILE_FUNCTIONS,
            ML_FUNCTIONS,
            GRAPH_FUNCTIONS,
        ):
            self.builtins.update(grupo)

        # Agrega utilidades tabulares.
        self.builtins.update({
            "columna": MotorDatos.columna,
            "filas": MotorDatos.filas,
            "columnas": MotorDatos.nombres_columnas,
            "matriz_columnas": MotorDatos.matriz_columnas,
            "longitud": len,
        })

        # Agrega constantes comunes.
        self.contexto.guardar("pi", PI)
        self.contexto.guardar("e", E)

    def visitPrograma(self, ctx):
        # Ejecuta todas las sentencias.
        resultado = None
        for sentencia in ctx.sentencia():
            resultado = self.visit(sentencia)
        return resultado

    def visitDeclaracion(self, ctx):
        # Crea una variable tipada.
        nombre = ctx.ID().getText()
        tipo = ctx.tipo().getText()
        valor = self.visit(ctx.expr())
        self._validar_tipo(tipo, valor)
        return self.contexto.guardar(nombre, valor, tipo)

    def _validar_tipo(self, tipo, valor):
        # Comprueba el tipo declarado.
        validaciones = {
            "numero": lambda v: isinstance(v, int) and not isinstance(v, bool),
            "entero": lambda v: isinstance(v, int) and not isinstance(v, bool),
            "decimal": lambda v: isinstance(v, (int, float)) and not isinstance(v, bool),
            "texto": lambda v: isinstance(v, str),
            "logico": lambda v: isinstance(v, bool),
            "lista": lambda v: isinstance(v, list),
            "matriz": lambda v: isinstance(v, list) and all(isinstance(f, list) for f in v),
        }
        if tipo in validaciones and not validaciones[tipo](valor):
            raise TipoIncompatibleError(f"'{valor}' no corresponde a {tipo}.")

    def visitAsignacion(self, ctx):
        # Asigna valores o tablas.
        nombre = ctx.ID().getText()

        if ctx.CORCHETE_IZQ():
            indice = int(self.visit(ctx.expr(0)))
            valor = self.visit(ctx.expr(1))
            lista = self.contexto.obtener(nombre)
            if not isinstance(lista, list):
                raise TipoIncompatibleError("La asignacion por indice requiere una lista.")
            lista[indice] = valor
            return valor

        if ctx.lectura():
            valor = self.visit(ctx.lectura())
        elif ctx.flujo():
            valor = self.visit(ctx.flujo())
        else:
            valor = self.visit(ctx.expr(0))

        tipo = self.contexto.obtener_tipo(nombre)
        if tipo:
            self._validar_tipo(tipo, valor)
        return self.contexto.guardar(nombre, valor)

    def visitLectura(self, ctx):
        # Abre un archivo CSV.
        return MotorDatos.abrir_csv(self._string(ctx.STRING().getText()))

    def visitFlujo(self, ctx):
        # Ejecuta un pipeline tabular.
        datos = self.contexto.obtener(ctx.ID().getText())
        if not isinstance(datos, (TablaDatos, AgrupacionDatos)):
            raise TipoIncompatibleError("Un pipeline debe iniciar con datos tabulares.")
        datos = datos.copiar() if isinstance(datos, TablaDatos) else datos
        for paso in ctx.paso():
            datos = self._ejecutar_paso(paso, datos)
        return datos

    def _ejecutar_paso(self, ctx, datos):
        # Ejecuta una transformacion.
        if ctx.seleccion():
            self._exigir_tabla(datos)
            return MotorDatos.tomar_columnas(datos, self._obtener_columnas(ctx.seleccion().columnas()))

        if ctx.filtro():
            self._exigir_tabla(datos)
            regla = ctx.filtro()
            return MotorDatos.filtrar(
                datos,
                lambda fila, _: self._evaluar_en_fila(regla.expr(), fila),
            )

        if ctx.ordenamiento():
            self._exigir_tabla(datos)
            regla = ctx.ordenamiento()
            direccion = "desc" if regla.DESC() else "asc"
            return MotorDatos.ordenar(datos, regla.ID().getText(), direccion)

        if ctx.columnaCalculada():
            self._exigir_tabla(datos)
            regla = ctx.columnaCalculada()
            return MotorDatos.crear_columna(
                datos,
                regla.ID().getText(),
                lambda fila, _: self._evaluar_en_fila(regla.expr(), fila),
            )

        if ctx.rellenarNulos():
            self._exigir_tabla(datos)
            regla = ctx.rellenarNulos()
            valor = self.visit(regla.expr())
            return MotorDatos.rellenar_nulos(datos, regla.ID().getText(), valor)

        if ctx.eliminarNulos():
            self._exigir_tabla(datos)
            return MotorDatos.eliminar_nulos(
                datos,
                self._obtener_columnas(ctx.eliminarNulos().columnas()),
            )

        if ctx.eliminarDuplicados():
            self._exigir_tabla(datos)
            return MotorDatos.eliminar_duplicados(datos)

        if ctx.renombrarColumna():
            self._exigir_tabla(datos)
            ids = ctx.renombrarColumna().ID()
            return MotorDatos.renombrar(datos, ids[0].getText(), ids[1].getText())

        if ctx.convertirTipo():
            self._exigir_tabla(datos)
            regla = ctx.convertirTipo()
            tipo = regla.getChild(regla.getChildCount() - 1).getText()
            return MotorDatos.convertir(datos, regla.ID().getText(), tipo)

        if ctx.agrupacion():
            self._exigir_tabla(datos)
            return MotorDatos.agrupar(
                datos,
                self._obtener_columnas(ctx.agrupacion().columnas()),
            )

        if ctx.resumen():
            if not isinstance(datos, AgrupacionDatos):
                raise OperacionNoPermitidaError("resumir requiere agrupar primero.")
            agregaciones = []
            for item in ctx.resumen().agregacion():
                ids = [token.getText() for token in item.ID()]
                nombre = ids[0]
                funcion = ids[1]
                columna = ids[2] if len(ids) > 2 else None
                agregaciones.append((nombre, funcion, columna))
            return MotorDatos.resumir(datos, agregaciones)

        raise OperacionNoPermitidaError("Paso del pipeline no reconocido.")

    @staticmethod
    def _exigir_tabla(datos):
        # Exige una TablaDatos.
        if not isinstance(datos, TablaDatos):
            raise TipoIncompatibleError("La operacion requiere una TablaDatos.")

    @staticmethod
    def _obtener_columnas(ctx):
        # Convierte tokens en nombres.
        return [token.getText() for token in ctx.ID()]

    def _evaluar_en_fila(self, ctx, fila):
        # Evalua expresiones con columnas.
        anterior = self._fila_actual
        self._fila_actual = fila
        try:
            return self.visit(ctx)
        finally:
            self._fila_actual = anterior

    def visitImprimir(self, ctx):
        # Muestra un resultado.
        valor = self.visit(ctx.expr())
        print(self._representar(valor))
        return valor

    def visitGuardado(self, ctx):
        # Guarda una tabla en CSV.
        datos = self.contexto.obtener(ctx.ID().getText())
        ruta = self._string(ctx.STRING().getText())
        salida = MotorDatos.guardar_csv(datos, ruta)
        print(f"CSV generado: {salida}")
        return salida

    def visitVisualizacion(self, ctx):
        # Genera una grafica PNG.
        ids = [token.getText() for token in ctx.ID()]
        datos = self.contexto.obtener(ids[0])
        self._exigir_tabla(datos)

        indice = 1
        eje_x = None
        eje_y = None
        if ctx.EJE_X():
            eje_x = ids[indice]
            indice += 1
        if ctx.EJE_Y():
            eje_y = ids[indice]

        cadenas = [self._string(token.getText()) for token in ctx.STRING()]
        titulo = cadenas[0] if ctx.TITULO() else ""
        ruta = cadenas[-1]
        salida = graficar(
            ctx.TIPO_GRAFICA().getText(),
            datos,
            x=eje_x,
            y=eje_y,
            titulo=titulo,
            ruta=ruta,
        )
        print(f"Grafica generada: {salida}")
        return salida

    def visitSiStmt(self, ctx):
        # Ejecuta una rama condicional.
        bloques = ctx.bloque()
        if bool(self.visit(ctx.expr())):
            return self.visit(bloques[0])
        if ctx.SINO() and len(bloques) > 1:
            return self.visit(bloques[1])
        return None

    def visitMientrasStmt(self, ctx):
        # Repite mientras sea verdadero.
        resultado = None
        iteraciones = 0
        while bool(self.visit(ctx.expr())):
            resultado = self.visit(ctx.bloque())
            iteraciones += 1
            if iteraciones > 100000:
                raise OperacionNoPermitidaError("El ciclo excedio el limite de seguridad.")
        return resultado

    def visitParaStmt(self, ctx):
        # Recorre un rango inclusivo.
        expresiones = ctx.expr()
        inicio = int(self.visit(expresiones[0]))
        fin = int(self.visit(expresiones[1]))
        paso = int(self.visit(expresiones[2])) if len(expresiones) > 2 else 1
        if paso == 0:
            raise OperacionNoPermitidaError("El paso del ciclo no puede ser 0.")
        limite = fin + (1 if paso > 0 else -1)
        resultado = None
        for valor in range(inicio, limite, paso):
            self.contexto.guardar(ctx.ID().getText(), valor)
            resultado = self.visit(ctx.bloque())
        return resultado

    def visitFuncionDecl(self, ctx):
        # Registra una funcion.
        parametros = []
        if ctx.parametros():
            parametros = [token.getText() for token in ctx.parametros().ID()]
        self.contexto.guardar_funcion(ctx.ID().getText(), parametros, ctx.bloque())
        return None

    def visitRetorno(self, ctx):
        # Sale de una funcion.
        raise _RetornoSignal(self.visit(ctx.expr()))

    def visitBloque(self, ctx):
        # Ejecuta un bloque.
        resultado = None
        for sentencia in ctx.sentencia():
            resultado = self.visit(sentencia)
        return resultado

    def visitLlamada(self, ctx):
        # Ejecuta una funcion.
        nombre = ctx.ID().getText()
        argumentos = []
        if ctx.argumentos():
            argumentos = [self.visit(exp) for exp in ctx.argumentos().expr()]

        if nombre in self.builtins:
            try:
                return self.builtins[nombre](*argumentos)
            except Exception as error:
                if isinstance(error, (TipoIncompatibleError, OperacionNoPermitidaError)):
                    raise
                raise OperacionNoPermitidaError(f"{nombre}: {error}") from error

        funcion = self.contexto.obtener_funcion(nombre)
        if not funcion:
            raise VariableNoDefinidaError(nombre)
        parametros = funcion["parametros"]
        if len(parametros) != len(argumentos):
            raise OperacionNoPermitidaError(
                f"{nombre} espera {len(parametros)} parametros y recibio {len(argumentos)}."
            )

        self.contexto.entrar_ambito(dict(zip(parametros, argumentos)))
        try:
            self.visit(funcion["bloque"])
        except _RetornoSignal as retorno:
            return retorno.valor
        finally:
            self.contexto.salir_ambito()
        return None

    def visitLogicaO(self, ctx):
        # Evalua OR.
        valores = ctx.logicaY()
        resultado = self.visit(valores[0])
        for valor_ctx in valores[1:]:
            resultado = bool(resultado) or bool(self.visit(valor_ctx))
        return resultado

    def visitLogicaY(self, ctx):
        # Evalua AND.
        valores = ctx.igualdad()
        resultado = self.visit(valores[0])
        for valor_ctx in valores[1:]:
            resultado = bool(resultado) and bool(self.visit(valor_ctx))
        return resultado

    def visitIgualdad(self, ctx):
        # Evalua igualdad.
        valores = ctx.comparacion()
        resultado = self.visit(valores[0])
        for i in range(1, len(valores)):
            derecha = self.visit(valores[i])
            operador = ctx.getChild(2 * i - 1).getText()
            resultado = resultado == derecha if operador == "==" else resultado != derecha
        return resultado

    def visitComparacion(self, ctx):
        # Evalua comparadores.
        valores = ctx.suma()
        resultado = self.visit(valores[0])
        for i in range(1, len(valores)):
            derecha = self.visit(valores[i])
            operador = ctx.getChild(2 * i - 1).getText()
            if operador == ">":
                resultado = resultado > derecha
            elif operador == "<":
                resultado = resultado < derecha
            elif operador == ">=":
                resultado = resultado >= derecha
            else:
                resultado = resultado <= derecha
        return resultado

    def visitSuma(self, ctx):
        # Evalua suma y resta.
        valores = ctx.producto()
        resultado = self.visit(valores[0])
        for i in range(1, len(valores)):
            derecha = self.visit(valores[i])
            operador = ctx.getChild(2 * i - 1).getText()
            resultado = resultado + derecha if operador == "+" else resultado - derecha
        return resultado

    def visitProducto(self, ctx):
        # Evalua producto, division y modulo.
        valores = ctx.potencia()
        resultado = self.visit(valores[0])
        for i in range(1, len(valores)):
            derecha = self.visit(valores[i])
            operador = ctx.getChild(2 * i - 1).getText()
            if operador == "*":
                resultado = resultado * derecha
            elif operador == "/":
                if derecha == 0:
                    raise OperacionNoPermitidaError("Division por cero.")
                resultado = resultado / derecha
            else:
                resultado = resultado % derecha
        return resultado

    def visitPotencia(self, ctx):
        # Evalua potencia.
        base = self.visit(ctx.unario())
        return base ** self.visit(ctx.potencia()) if ctx.potencia() else base

    def visitUnario(self, ctx):
        # Evalua negacion y signo.
        if ctx.primario():
            return self.visit(ctx.primario())
        operador = ctx.getChild(0).getText()
        valor = self.visit(ctx.unario())
        return -valor if operador == "-" else not bool(valor)

    def visitPrimario(self, ctx):
        # Convierte literales y variables.
        if ctx.NUMBER():
            texto = ctx.NUMBER().getText()
            return float(texto) if "." in texto else int(texto)
        if ctx.STRING():
            return self._string(ctx.STRING().getText())
        if ctx.VERDADERO():
            return True
        if ctx.FALSO():
            return False
        if ctx.listaLiteral():
            return self.visit(ctx.listaLiteral())
        if ctx.llamada():
            return self.visit(ctx.llamada())
        if ctx.ID():
            nombre = ctx.ID().getText()
            valor = self._resolver_identificador(nombre)
            if ctx.CORCHETE_IZQ():
                return valor[int(self.visit(ctx.expr()))]
            return valor
        return self.visit(ctx.expr())

    def visitListaLiteral(self, ctx):
        # Construye listas y matrices.
        return [self.visit(exp) for exp in ctx.expr()]

    def _resolver_identificador(self, nombre):
        # Prioriza columnas en una fila.
        if self._fila_actual is not None and nombre in self._fila_actual:
            return self._fila_actual[nombre]
        return self.contexto.obtener(nombre)

    @staticmethod
    def _string(texto):
        # Decodifica una cadena del DSL.
        return json.loads(texto)

    @staticmethod
    def _representar(valor):
        # Crea texto para terminal.
        if isinstance(valor, bool):
            return "verdadero" if valor else "falso"
        if isinstance(valor, TablaDatos):
            return str(valor)
        return str(valor)
