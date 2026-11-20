# Convierte datos y resultados de modelos en graficas PNG con Matplotlib.
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
    from librerias.DataMath import seno, coseno, tangente, funcion_tablero

    funciones = {
        "sigmoide": sigmoide,
        "seno": seno,
        "coseno": coseno,
        "tangente": tangente,
        "funcion_tablero": funcion_tablero,
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



# Representaciones especificas de algoritmos que calcula DataML.
def graficar_regresion(tabla, modelo, x, y, ruta="salidas/ml_regresion.png", titulo="Regresion lineal"):
    # Puntos observados y recta predicha por un modelo de una sola entrada.
    from librerias.DataML import predecir_lineal
    if not isinstance(tabla, TablaDatos):
        raise TypeError("Se esperaba una TablaDatos.")
    tabla.validar_columnas([x, y])
    if len(modelo.get("pesos", [])) != 2:
        raise ValueError("Se necesita una regresion con una sola variable de entrada.")
    pares = sorted((float(f[x]), float(f[y])) for f in tabla.filas)
    xs, ys = zip(*pares)
    pred = predecir_lineal(modelo, [[v] for v in xs])
    ruta = Path(str(ruta))
    ruta.parent.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.scatter(xs, ys, label="Datos observados")
    ax.plot(xs, pred, label="Modelo lineal")
    ax.set(xlabel=x, ylabel=y, title=titulo)
    ax.legend()
    fig.tight_layout()
    fig.savefig(ruta, dpi=140)
    plt.close(fig)
    return str(ruta)


def graficar_knn(tabla, modelo, punto, x, y, ruta="salidas/ml_knn.png", titulo="KNN"):
    # Muestra clases, un punto nuevo y los K vecinos mas cercanos.
    if not isinstance(tabla, TablaDatos) or modelo.get("tipo") != "knn":
        raise TypeError("Se necesita una tabla y un modelo KNN.")
    if modelo.get("columnas") != [x, y] or len(punto) != 2:
        raise ValueError("Las dos columnas y el punto deben coincidir con el modelo.")
    datos, clases = modelo["x"], modelo["y"]
    if not datos:
        raise ValueError("El modelo no tiene datos.")
    px, py = float(punto[0]), float(punto[1])
    fig, ax = plt.subplots(figsize=(8, 5))
    for clase in dict.fromkeys(clases):
        filas = [p for p, etiqueta in zip(datos, clases) if etiqueta == clase]
        ax.scatter([p[0] for p in filas], [p[1] for p in filas], label=f"Clase {clase}")
    cercanos = sorted(range(len(datos)), key=lambda i: (datos[i][0]-px)**2+(datos[i][1]-py)**2)
    cercanos = cercanos[:max(1, min(int(modelo["k"]), len(datos)))]
    ax.scatter([datos[i][0] for i in cercanos], [datos[i][1] for i in cercanos],
               s=220, facecolors="none", edgecolors="black", label="Vecinos")
    ax.scatter([px], [py], marker="*", s=230, color="red", label="Nuevo dato", zorder=5)
    ax.set(xlabel=x, ylabel=y, title=titulo)
    ax.legend()
    ruta = Path(str(ruta))
    ruta.parent.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(ruta, dpi=140)
    plt.close(fig)
    return str(ruta)


def graficar_kmeans(tabla, modelo, x, y, ruta="salidas/ml_kmeans.png", titulo="K-Means"):
    # Dibuja grupos calculados y centroides.
    if not isinstance(tabla, TablaDatos) or modelo.get("tipo") != "kmeans":
        raise TypeError("Se necesita una tabla y un modelo K-Means.")
    if modelo.get("columnas") != [x, y]:
        raise ValueError("Las columnas no coinciden con el modelo.")
    datos = tabla.matriz_columnas([x, y])
    etiquetas = modelo["etiquetas"]
    if len(datos) != len(etiquetas):
        raise ValueError("Los grupos no coinciden con las filas.")
    fig, ax = plt.subplots(figsize=(8, 5))
    for grupo in sorted(set(etiquetas)):
        filas = [p for p, e in zip(datos, etiquetas) if e == grupo]
        ax.scatter([p[0] for p in filas], [p[1] for p in filas], label=f"Grupo {grupo+1}")
    centros = modelo["centroides"]
    ax.scatter([p[0] for p in centros], [p[1] for p in centros],
               marker="x", s=180, linewidths=3, color="black", label="Centroides")
    ax.set(xlabel=x, ylabel=y, title=titulo)
    ax.legend()
    ruta = Path(str(ruta))
    ruta.parent.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(ruta, dpi=140)
    plt.close(fig)
    return str(ruta)


FUNCTIONS = {
    "graficar_regresion": graficar_regresion,
    "graficar_knn": graficar_knn,
    "graficar_kmeans": graficar_kmeans,
    "grafica_barras": barras,
    "grafica_lineas": lineas,
    "grafica_histograma": histograma,
    "grafica_dispersion": dispersion,
    "grafica_caja": caja,
    "graficar_funcion": graficar_funcion,
    "graficar_entrenamiento": graficar_entrenamiento,
}
