# Machine Learning propio de DataDSL.

from librerias.DataMath import exponencial, raiz
from librerias.DataMatrix import transpuesta, multiplicar_matrices, inversa
from librerias.DataTable import TablaDatos


def _matriz_x(x):
    # Convierte vector o matriz a matriz.
    if not isinstance(x, list):
        raise TypeError("X debe ser una lista.")
    if not x:
        return []
    if isinstance(x[0], list):
        return [[float(v) for v in fila] for fila in x]
    return [[float(v)] for v in x]


def _vector_y(y):
    # Convierte etiquetas a vector.
    if not isinstance(y, list):
        raise TypeError("y debe ser una lista.")
    return [float(v) for v in y]


def regresion_lineal(x, y):
    # Ajusta una recta o hiperplano.
    x = _matriz_x(x)
    y = _vector_y(y)
    if len(x) != len(y) or not x:
        raise ValueError("X e y deben tener igual cantidad de filas.")
    diseno = [[1.0] + fila for fila in x]
    xt = transpuesta(diseno)
    xtx = multiplicar_matrices(xt, diseno)
    pesos = multiplicar_matrices(
        multiplicar_matrices(inversa(xtx), xt),
        [[v] for v in y],
    )
    return {"tipo": "regresion_lineal", "pesos": [fila[0] for fila in pesos]}


def predecir_lineal(modelo, x):
    # Predice con los pesos aprendidos.
    if modelo.get("tipo") != "regresion_lineal":
        raise TypeError("El modelo no es regresion lineal.")
    filas = _matriz_x(x)
    pesos = modelo["pesos"]
    resultados = [
        pesos[0] + sum(w * v for w, v in zip(pesos[1:], fila))
        for fila in filas
    ]
    return resultados[0] if len(resultados) == 1 else resultados


def sigmoide(z):
    # Convierte un valor en probabilidad.
    z = float(z)
    if z >= 0:
        ez = exponencial(-z)
        return 1.0 / (1.0 + ez)
    ez = exponencial(z)
    return ez / (1.0 + ez)


def regresion_logistica(x, y, tasa=0.1, epocas=1000):
    # Entrena con gradiente descendente.
    x = _matriz_x(x)
    y = _vector_y(y)
    if len(x) != len(y) or not x:
        raise ValueError("X e y deben tener igual cantidad de filas.")
    diseno = [[1.0] + fila for fila in x]
    pesos = [0.0] * len(diseno[0])
    n = len(diseno)
    for _ in range(int(epocas)):
        gradiente = [0.0] * len(pesos)
        for fila, objetivo in zip(diseno, y):
            prob = sigmoide(sum(w * v for w, v in zip(pesos, fila)))
            error = prob - objetivo
            for j, valor in enumerate(fila):
                gradiente[j] += error * valor
        for j in range(len(pesos)):
            pesos[j] -= float(tasa) * gradiente[j] / n
    return {"tipo": "regresion_logistica", "pesos": pesos}


def probabilidad_logistica(modelo, x):
    # Calcula probabilidades binarias.
    if modelo.get("tipo") != "regresion_logistica":
        raise TypeError("El modelo no es regresion logistica.")
    filas = _matriz_x(x)
    pesos = modelo["pesos"]
    probs = [
        sigmoide(pesos[0] + sum(w * v for w, v in zip(pesos[1:], fila)))
        for fila in filas
    ]
    return probs[0] if len(probs) == 1 else probs


def predecir_logistica(modelo, x, umbral=0.5):
    # Convierte probabilidades en clases.
    probs = probabilidad_logistica(modelo, x)
    if isinstance(probs, list):
        return [1 if p >= umbral else 0 for p in probs]
    return 1 if probs >= umbral else 0


def _distancia(a, b):
    # Calcula distancia euclidiana.
    return raiz(sum((x - y) ** 2 for x, y in zip(a, b)))


def knn(x_train, y_train, x_test, k=3):
    # Clasifica por vecinos cercanos.
    x_train = _matriz_x(x_train)
    y_train = list(y_train)
    x_test = _matriz_x(x_test)
    if len(x_train) != len(y_train) or not x_train:
        raise ValueError("Datos de entrenamiento invalidos.")
    k = max(1, min(int(k), len(x_train)))
    resultados = []
    for punto in x_test:
        vecinos = sorted(
            (_distancia(punto, fila), etiqueta)
            for fila, etiqueta in zip(x_train, y_train)
        )[:k]
        conteo = {}
        for _, etiqueta in vecinos:
            conteo[etiqueta] = conteo.get(etiqueta, 0) + 1
        resultados.append(max(conteo, key=conteo.get))
    return resultados[0] if len(resultados) == 1 else resultados


def kmeans_lista(x, k=2, max_iter=100):
    # Agrupa datos por centroides.
    datos = _matriz_x(x)
    if not datos:
        raise ValueError("No hay datos.")
    k = int(k)
    if k < 1 or k > len(datos):
        raise ValueError("k fuera de rango.")
    indices = [0] if k == 1 else [round(i * (len(datos) - 1) / (k - 1)) for i in range(k)]
    centroides = [datos[i][:] for i in indices]
    etiquetas = [-1] * len(datos)
    for _ in range(int(max_iter)):
        nuevas = [min(range(k), key=lambda j: _distancia(p, centroides[j])) for p in datos]
        if nuevas == etiquetas:
            break
        etiquetas = nuevas
        for j in range(k):
            grupo = [p for p, e in zip(datos, etiquetas) if e == j]
            if grupo:
                centroides[j] = [sum(col) / len(col) for col in zip(*grupo)]
    return {"tipo": "kmeans", "centroides": centroides, "etiquetas": etiquetas}


def accuracy(real, pred):
    # Calcula porcentaje de aciertos.
    if len(real) != len(pred) or not real:
        raise ValueError("Listas invalidas.")
    return sum(a == b for a, b in zip(real, pred)) / len(real)


def precision(real, pred):
    # Calcula precision de clase 1.
    tp = sum(a == 1 and b == 1 for a, b in zip(real, pred))
    fp = sum(a == 0 and b == 1 for a, b in zip(real, pred))
    return tp / (tp + fp) if tp + fp else 0.0


def recall(real, pred):
    # Calcula recall de clase 1.
    tp = sum(a == 1 and b == 1 for a, b in zip(real, pred))
    fn = sum(a == 1 and b == 0 for a, b in zip(real, pred))
    return tp / (tp + fn) if tp + fn else 0.0


def matriz_confusion(real, pred):
    # Devuelve [[TN, FP], [FN, TP]].
    tn = sum(a == 0 and b == 0 for a, b in zip(real, pred))
    fp = sum(a == 0 and b == 1 for a, b in zip(real, pred))
    fn = sum(a == 1 and b == 0 for a, b in zip(real, pred))
    tp = sum(a == 1 and b == 1 for a, b in zip(real, pred))
    return [[tn, fp], [fn, tp]]


def _extraer_xy(tabla, columnas, objetivo):
    # Extrae columnas desde TablaDatos.
    if not isinstance(tabla, TablaDatos):
        raise TypeError("Se esperaba una TablaDatos.")
    x = tabla.matriz_columnas(columnas)
    y = tabla.columna(objetivo)
    if len(x) != len(y):
        raise ValueError("Hay valores nulos incompatibles con ML.")
    return x, y


def entrenar_regresion(tabla, columnas, objetivo):
    # Entrena regresion desde una tabla.
    x, y = _extraer_xy(tabla, columnas, objetivo)
    modelo = regresion_lineal(x, y)
    modelo["columnas"] = list(columnas)
    modelo["objetivo"] = objetivo
    return modelo


def entrenar_logistica(tabla, columnas, objetivo, tasa=0.1, epocas=1000):
    # Entrena clasificacion desde tabla.
    x, y = _extraer_xy(tabla, columnas, objetivo)
    modelo = regresion_logistica(x, y, tasa, epocas)
    modelo["columnas"] = list(columnas)
    modelo["objetivo"] = objetivo
    return modelo


def entrenar_knn(tabla, columnas, objetivo, k=3):
    # Guarda ejemplos para KNN.
    x, y = _extraer_xy(tabla, columnas, objetivo)
    return {
        "tipo": "knn",
        "columnas": list(columnas),
        "objetivo": objetivo,
        "k": int(k),
        "x": x,
        "y": y,
    }


def predecir_knn(modelo, valores):
    # Predice con un modelo KNN.
    if modelo.get("tipo") != "knn":
        raise TypeError("El modelo no es KNN.")
    return knn(modelo["x"], modelo["y"], valores, modelo["k"])


def kmeans(datos, columnas_o_k=2, k=3, max_iter=100):
    # Acepta lista o TablaDatos.
    if isinstance(datos, TablaDatos):
        columnas = list(columnas_o_k)
        modelo = kmeans_lista(datos.matriz_columnas(columnas), k, max_iter)
        modelo["columnas"] = columnas
        return modelo
    return kmeans_lista(datos, columnas_o_k, k)


def entrenar_mlp(x, y, ocultas=2, tasa=1.0, epocas=3000):
    # Entrena una red de una capa oculta.
    x = _matriz_x(x)
    y = _vector_y(y)
    if len(x) != len(y) or not x:
        raise ValueError("X e y deben tener igual cantidad de filas.")

    entradas = len(x[0])
    ocultas = int(ocultas)
    if ocultas < 1:
        raise ValueError("La red necesita al menos una neurona oculta.")

    # Inicializa pesos de forma determinista.
    w1 = [
        [((((i + 1) * (j + 2)) % 7) - 3) / 5.0 for j in range(entradas)]
        for i in range(ocultas)
    ]
    b1 = [0.0] * ocultas
    w2 = [((((i + 2) * 3) % 7) - 3) / 5.0 for i in range(ocultas)]
    b2 = 0.0

    historial_error = []
    historial_epocas = []
    tasa = float(tasa)
    epocas = int(epocas)
    salto = max(1, epocas // 100)

    for epoca in range(epocas):
        grad_w1 = [[0.0] * entradas for _ in range(ocultas)]
        grad_b1 = [0.0] * ocultas
        grad_w2 = [0.0] * ocultas
        grad_b2 = 0.0
        error_total = 0.0

        for fila, objetivo in zip(x, y):
            # Propagacion hacia adelante.
            salida_oculta = [
                sigmoide(sum(w1[i][j] * fila[j] for j in range(entradas)) + b1[i])
                for i in range(ocultas)
            ]
            salida = sigmoide(sum(w2[i] * salida_oculta[i] for i in range(ocultas)) + b2)
            error_total += (salida - objetivo) ** 2

            # Retropropagacion.
            delta_salida = salida - objetivo
            for i in range(ocultas):
                grad_w2[i] += delta_salida * salida_oculta[i]
                delta_oculta = (
                    delta_salida
                    * w2[i]
                    * salida_oculta[i]
                    * (1.0 - salida_oculta[i])
                )
                for j in range(entradas):
                    grad_w1[i][j] += delta_oculta * fila[j]
                grad_b1[i] += delta_oculta
            grad_b2 += delta_salida

        cantidad = len(x)
        for i in range(ocultas):
            w2[i] -= tasa * grad_w2[i] / cantidad
            b1[i] -= tasa * grad_b1[i] / cantidad
            for j in range(entradas):
                w1[i][j] -= tasa * grad_w1[i][j] / cantidad
        b2 -= tasa * grad_b2 / cantidad

        if epoca % salto == 0 or epoca == epocas - 1:
            historial_epocas.append(epoca)
            historial_error.append(error_total / cantidad)

    return {
        "tipo": "mlp",
        "entradas": entradas,
        "ocultas": ocultas,
        "w1": w1,
        "b1": b1,
        "w2": w2,
        "b2": b2,
        "historial_epocas": historial_epocas,
        "historial_error": historial_error,
    }


def probabilidad_mlp(modelo, x):
    # Calcula la salida de la red.
    if modelo.get("tipo") != "mlp":
        raise TypeError("El modelo no es un MLP.")
    filas = _matriz_x(x)
    resultados = []
    for fila in filas:
        salida_oculta = [
            sigmoide(
                sum(modelo["w1"][i][j] * fila[j] for j in range(modelo["entradas"]))
                + modelo["b1"][i]
            )
            for i in range(modelo["ocultas"])
        ]
        salida = sigmoide(
            sum(modelo["w2"][i] * salida_oculta[i] for i in range(modelo["ocultas"]))
            + modelo["b2"]
        )
        resultados.append(salida)
    return resultados[0] if len(resultados) == 1 else resultados


def predecir_mlp(modelo, x, umbral=0.5):
    # Convierte la salida del MLP en clases.
    probabilidades = probabilidad_mlp(modelo, x)
    if isinstance(probabilidades, list):
        return [1 if valor >= umbral else 0 for valor in probabilidades]
    return 1 if probabilidades >= umbral else 0


FUNCTIONS = {
    "sigmoide": sigmoide,
    "regresion_lineal": regresion_lineal,
    "predecir_lineal": predecir_lineal,
    "regresion_logistica": regresion_logistica,
    "probabilidad_logistica": probabilidad_logistica,
    "predecir_logistica": predecir_logistica,
    "knn": knn,
    "kmeans": kmeans,
    "accuracy": accuracy,
    "precision": precision,
    "recall": recall,
    "matriz_confusion": matriz_confusion,
    "entrenar_regresion": entrenar_regresion,
    "entrenar_logistica": entrenar_logistica,
    "entrenar_knn": entrenar_knn,
    "predecir_knn": predecir_knn,
    "entrenar_mlp": entrenar_mlp,
    "probabilidad_mlp": probabilidad_mlp,
    "predecir_mlp": predecir_mlp,
}
