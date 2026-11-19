# Aleatorios propios de DataDSL.

_estado = 123456789


def semilla(valor):
    # Cambia el estado inicial.
    global _estado
    _estado = int(valor) & 0x7FFFFFFF
    return _estado


def aleatorio():
    # Genera un decimal con LCG.
    global _estado
    _estado = (1103515245 * _estado + 12345) & 0x7FFFFFFF
    return _estado / 2147483648.0


def aleatorio_entero(minimo, maximo):
    # Genera un entero inclusivo.
    minimo, maximo = int(minimo), int(maximo)
    if minimo > maximo:
        minimo, maximo = maximo, minimo
    return minimo + int(aleatorio() * (maximo - minimo + 1))


def elegir(lista):
    # Elige un elemento de una lista.
    if not lista:
        raise ValueError("La lista esta vacia.")
    return lista[aleatorio_entero(0, len(lista) - 1)]


FUNCTIONS = {
    "semilla": semilla,
    "aleatorio": aleatorio,
    "aleatorio_entero": aleatorio_entero,
    "elegir": elegir,
}
