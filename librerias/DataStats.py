# Estadistica propia de DataDSL.

from librerias.DataMath import raiz


def _numeros(datos):
    # Convierte valores a decimal.
    return [float(x) for x in datos if x is not None]


def suma(datos):
    # Suma todos los valores.
    return sum(_numeros(datos))


def media(datos):
    # Calcula el promedio.
    valores = _numeros(datos)
    if not valores:
        raise ValueError("No hay datos.")
    return sum(valores) / len(valores)


def mediana(datos):
    # Busca el valor central.
    valores = sorted(_numeros(datos))
    if not valores:
        raise ValueError("No hay datos.")
    mitad = len(valores) // 2
    if len(valores) % 2:
        return valores[mitad]
    return (valores[mitad - 1] + valores[mitad]) / 2


def minimo(datos):
    # Retorna el menor valor.
    valores = _numeros(datos)
    if not valores:
        raise ValueError("No hay datos.")
    return min(valores)


def maximo(datos):
    # Retorna el mayor valor.
    valores = _numeros(datos)
    if not valores:
        raise ValueError("No hay datos.")
    return max(valores)


def varianza(datos, muestral=False):
    # Mide la dispersion.
    valores = _numeros(datos)
    if not valores:
        raise ValueError("No hay datos.")
    divisor = len(valores) - 1 if muestral else len(valores)
    if divisor <= 0:
        return 0.0
    promedio = media(valores)
    return sum((x - promedio) ** 2 for x in valores) / divisor


def desviacion(datos, muestral=False):
    # Calcula la desviacion estandar.
    return raiz(varianza(datos, muestral))


def correlacion(x, y):
    # Calcula correlacion de Pearson.
    x = _numeros(x)
    y = _numeros(y)
    if not x or len(x) != len(y):
        raise ValueError("Las listas deben tener igual longitud.")
    mx, my = media(x), media(y)
    numerador = sum((a - mx) * (b - my) for a, b in zip(x, y))
    dx = sum((a - mx) ** 2 for a in x)
    dy = sum((b - my) ** 2 for b in y)
    denominador = raiz(dx * dy)
    return numerador / denominador if denominador else 0.0


def contar(datos):
    # Cuenta elementos.
    return len(list(datos))


FUNCTIONS = {
    "suma_lista": suma,
    "media_lista": media,
    "mediana_lista": mediana,
    "minimo_lista": minimo,
    "maximo_lista": maximo,
    "varianza": varianza,
    "desviacion_lista": desviacion,
    "correlacion": correlacion,
    "contar_lista": contar,
}
