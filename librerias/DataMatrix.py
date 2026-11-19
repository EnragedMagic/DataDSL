# Algebra lineal propia de DataDSL.


def _matriz(datos):
    # Convierte valores a decimal.
    return [[float(v) for v in fila] for fila in datos]


def transpuesta(a):
    # Intercambia filas por columnas.
    if not a:
        return []
    return [list(columna) for columna in zip(*a)]


def suma_matrices(a, b):
    # Suma elemento a elemento.
    if len(a) != len(b) or any(len(x) != len(y) for x, y in zip(a, b)):
        raise ValueError("Las matrices deben tener igual dimension.")
    return [[x + y for x, y in zip(fa, fb)] for fa, fb in zip(a, b)]


def resta_matrices(a, b):
    # Resta elemento a elemento.
    if len(a) != len(b) or any(len(x) != len(y) for x, y in zip(a, b)):
        raise ValueError("Las matrices deben tener igual dimension.")
    return [[x - y for x, y in zip(fa, fb)] for fa, fb in zip(a, b)]


def multiplicar_matrices(a, b):
    # Ejecuta el producto matricial.
    if not a or not b or len(a[0]) != len(b):
        raise ValueError("Dimensiones incompatibles.")
    bt = transpuesta(b)
    return [[sum(x * y for x, y in zip(fila, col)) for col in bt] for fila in a]


def determinante(a):
    # Usa eliminacion gaussiana.
    m = _matriz(a)
    n = len(m)
    if n == 0 or any(len(fila) != n for fila in m):
        raise ValueError("La matriz debe ser cuadrada.")
    resultado = 1.0
    for i in range(n):
        pivote = max(range(i, n), key=lambda r: abs(m[r][i]))
        if abs(m[pivote][i]) < 1e-12:
            return 0.0
        if pivote != i:
            m[i], m[pivote] = m[pivote], m[i]
            resultado *= -1
        valor_pivote = m[i][i]
        resultado *= valor_pivote
        for r in range(i + 1, n):
            factor = m[r][i] / valor_pivote
            for c in range(i + 1, n):
                m[r][c] -= factor * m[i][c]
    return resultado


def inversa(a):
    # Usa Gauss-Jordan.
    m = _matriz(a)
    n = len(m)
    if n == 0 or any(len(fila) != n for fila in m):
        raise ValueError("La matriz debe ser cuadrada.")
    aug = [fila + [1.0 if i == j else 0.0 for j in range(n)] for i, fila in enumerate(m)]
    for i in range(n):
        pivote = max(range(i, n), key=lambda r: abs(aug[r][i]))
        if abs(aug[pivote][i]) < 1e-12:
            raise ValueError("La matriz no es invertible.")
        aug[i], aug[pivote] = aug[pivote], aug[i]
        divisor = aug[i][i]
        aug[i] = [v / divisor for v in aug[i]]
        for r in range(n):
            if r == i:
                continue
            factor = aug[r][i]
            aug[r] = [x - factor * y for x, y in zip(aug[r], aug[i])]
    return [fila[n:] for fila in aug]


FUNCTIONS = {
    "transpuesta": transpuesta,
    "suma_matrices": suma_matrices,
    "resta_matrices": resta_matrices,
    "multiplicar_matrices": multiplicar_matrices,
    "determinante": determinante,
    "inversa": inversa,
}
