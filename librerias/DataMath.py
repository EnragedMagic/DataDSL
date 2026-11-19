# Matematicas propias de DataDSL.

PI = 3.141592653589793
E = 2.718281828459045


def raiz(x, tolerancia=1e-12):
    # Calcula raiz con Newton-Raphson.
    x = float(x)
    if x < 0:
        raise ValueError("No existe raiz real de un numero negativo.")
    if x == 0:
        return 0.0
    estimado = x if x >= 1 else 1.0
    for _ in range(100):
        nuevo = 0.5 * (estimado + x / estimado)
        if abs(nuevo - estimado) < tolerancia:
            return nuevo
        estimado = nuevo
    return estimado


def potencia(base, exponente):
    # Calcula potencias enteras rapido.
    if int(exponente) != exponente:
        return float(base) ** float(exponente)
    exponente = int(exponente)
    if exponente == 0:
        return 1
    if exponente < 0:
        return 1 / potencia(base, -exponente)
    resultado = 1
    actual = base
    while exponente:
        if exponente % 2:
            resultado *= actual
        actual *= actual
        exponente //= 2
    return resultado


def factorial(n):
    # Multiplica desde 1 hasta n.
    n = int(n)
    if n < 0:
        raise ValueError("Factorial requiere un entero no negativo.")
    resultado = 1
    for i in range(2, n + 1):
        resultado *= i
    return resultado


def mcd(a, b):
    # Usa el algoritmo de Euclides.
    a, b = abs(int(a)), abs(int(b))
    while b:
        a, b = b, a % b
    return a


def exponencial(x, terminos=35):
    # Aproxima e^x con Taylor.
    x = float(x)
    if x < 0:
        return 1.0 / exponencial(-x, terminos)
    mitad = 0
    while x > 1:
        x /= 2.0
        mitad += 1
    total = 1.0
    termino = 1.0
    for n in range(1, terminos):
        termino *= x / n
        total += termino
    for _ in range(mitad):
        total *= total
    return total


def seno(x, terminos=14):
    # Aproxima seno con Taylor.
    x = ((float(x) + PI) % (2 * PI)) - PI
    total = 0.0
    termino = x
    for n in range(terminos):
        if n:
            termino *= -x * x / ((2 * n) * (2 * n + 1))
        total += termino
    return total


def coseno(x, terminos=14):
    # Aproxima coseno con Taylor.
    x = ((float(x) + PI) % (2 * PI)) - PI
    total = 0.0
    termino = 1.0
    for n in range(terminos):
        if n:
            termino *= -x * x / ((2 * n - 1) * (2 * n))
        total += termino
    return total


def tangente(x):
    # Divide seno entre coseno.
    valor_coseno = coseno(x)
    if abs(valor_coseno) < 1e-12:
        raise ZeroDivisionError("Tangente indefinida.")
    return seno(x) / valor_coseno


def es_primo(n):
    # Comprueba si un entero es primo.
    n = int(n)
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    limite = int(raiz(n))
    divisor = 3
    while divisor <= limite:
        if n % divisor == 0:
            return False
        divisor += 2
    return True


FUNCTIONS = {
    "raiz": raiz,
    "potencia": potencia,
    "factorial": factorial,
    "mcd": mcd,
    "exponencial": exponencial,
    "seno": seno,
    "coseno": coseno,
    "tangente": tangente,
    "es_primo": es_primo,
    "abs": abs,
}
