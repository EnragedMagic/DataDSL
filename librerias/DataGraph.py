# Graficas de DataDSL.
# Matplotlib solo renderiza el PNG.

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from librerias.DataTable import TablaDatos


def _columna(tabla, nombre):
    # Obtiene una columna valida.
    if not isinstance(tabla, TablaDatos):
        raise TypeError("Se esperaba una TablaDatos.")
    tabla.validar_columnas([nombre])
    return tabla.columna(nombre)


def graficar(tipo, tabla, x=None, y=None, titulo="", ruta="salidas/grafica.png"):
    # Genera una grafica PNG.
    if not isinstance(tabla, TablaDatos):
        raise TypeError("graficar requiere una TablaDatos.")
    ruta = Path(str(ruta))
    ruta.parent.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(8, 5))

    if tipo == "barras":
        if not x or not y:
            raise ValueError("Barras necesita eje_x y eje_y.")
        ax.bar([str(v) for v in _columna(tabla, x)], _columna(tabla, y))
        ax.set_xlabel(x)
        ax.set_ylabel(y)

    elif tipo == "lineas":
        if not x or not y:
            raise ValueError("Lineas necesita eje_x y eje_y.")
        ax.plot(_columna(tabla, x), _columna(tabla, y), marker="o")
        ax.set_xlabel(x)
        ax.set_ylabel(y)

    elif tipo == "histograma":
        if not x:
            raise ValueError("Histograma necesita eje_x.")
        ax.hist(_columna(tabla, x))
        ax.set_xlabel(x)
        ax.set_ylabel("frecuencia")

    elif tipo == "dispersion":
        if not x or not y:
            raise ValueError("Dispersion necesita eje_x y eje_y.")
        ax.scatter(_columna(tabla, x), _columna(tabla, y))
        ax.set_xlabel(x)
        ax.set_ylabel(y)

    elif tipo == "caja":
        columna = y or x
        if not columna:
            raise ValueError("Caja necesita una columna.")
        ax.boxplot(_columna(tabla, columna))
        ax.set_xticks([1])
        ax.set_xticklabels([columna])
        ax.set_ylabel(columna)

    else:
        raise ValueError(f"Grafica no soportada: {tipo}")

    if titulo:
        ax.set_title(titulo)
    fig.tight_layout()
    fig.savefig(ruta, dpi=140)
    plt.close(fig)
    return str(ruta)


def barras(tabla, x, y, titulo="", ruta="salidas/barras.png"):
    # Atajo para barras.
    return graficar("barras", tabla, x, y, titulo, ruta)


def lineas(tabla, x, y, titulo="", ruta="salidas/lineas.png"):
    # Atajo para lineas.
    return graficar("lineas", tabla, x, y, titulo, ruta)


def histograma(tabla, x, titulo="", ruta="salidas/histograma.png"):
    # Atajo para histograma.
    return graficar("histograma", tabla, x, None, titulo, ruta)


def dispersion(tabla, x, y, titulo="", ruta="salidas/dispersion.png"):
    # Atajo para dispersion.
    return graficar("dispersion", tabla, x, y, titulo, ruta)


def caja(tabla, columna, titulo="", ruta="salidas/caja.png"):
    # Atajo para caja.
    return graficar("caja", tabla, None, columna, titulo, ruta)


def graficar_funcion(nombre, inicio, fin, paso=0.1, ruta="salidas/funcion.png", titulo=""):
    # Grafica una funcion matematica conocida.
    from librerias.DataML import sigmoide
    from librerias.DataMath import seno, coseno, tangente

    funciones = {
        "sigmoide": sigmoide,
        "seno": seno,
        "coseno": coseno,
        "tangente": tangente,
    }
    if nombre not in funciones:
        raise ValueError(f"Funcion no graficable: {nombre}")

    inicio = float(inicio)
    fin = float(fin)
    paso = float(paso)
    if paso <= 0:
        raise ValueError("El paso debe ser positivo.")

    xs = []
    ys = []
    actual = inicio
    funcion = funciones[nombre]
    while actual <= fin + 1e-12:
        xs.append(actual)
        ys.append(funcion(actual))
        actual += paso

    ruta = Path(str(ruta))
    ruta.parent.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(xs, ys)
    ax.set_xlabel("x")
    ax.set_ylabel(nombre)
    ax.set_title(titulo or nombre)
    fig.tight_layout()
    fig.savefig(ruta, dpi=140)
    plt.close(fig)
    return str(ruta)


def graficar_entrenamiento(modelo, ruta="salidas/entrenamiento.png", titulo="Error de entrenamiento"):
    # Grafica el historial de error de un modelo.
    epocas = modelo.get("historial_epocas")
    errores = modelo.get("historial_error")
    if not epocas or not errores:
        raise ValueError("El modelo no tiene historial de entrenamiento.")

    ruta = Path(str(ruta))
    ruta.parent.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(epocas, errores)
    ax.set_xlabel("epoca")
    ax.set_ylabel("error")
    ax.set_title(titulo)
    fig.tight_layout()
    fig.savefig(ruta, dpi=140)
    plt.close(fig)
    return str(ruta)


FUNCTIONS = {
    "grafica_barras": barras,
    "grafica_lineas": lineas,
    "grafica_histograma": histograma,
    "grafica_dispersion": dispersion,
    "grafica_caja": caja,
    "graficar_funcion": graficar_funcion,
    "graficar_entrenamiento": graficar_entrenamiento,
}
