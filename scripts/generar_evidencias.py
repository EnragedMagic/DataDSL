# Genera evidencias sin usar el parser.

from pathlib import Path
import sys

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ))

from librerias.DataGraph import graficar
from librerias.DataML import entrenar_regresion, predecir_lineal, entrenar_knn, predecir_knn, kmeans
from src.MotorDatos import MotorDatos


EVIDENCIAS = RAIZ / "evidencias"


def main():
    # Prepara ventas y resumen.
    ventas = MotorDatos.abrir_csv(RAIZ / "datos" / "ventas.csv")
    ventas = MotorDatos.rellenar_nulos(ventas, "precio", 0)
    ventas = MotorDatos.eliminar_duplicados(ventas)
    ventas = MotorDatos.filtrar(ventas, lambda fila, _: fila["cantidad"] > 0)
    ventas = MotorDatos.crear_columna(
        ventas,
        "total",
        lambda fila, _: fila["cantidad"] * fila["precio"],
    )
    grupos = MotorDatos.agrupar(ventas, ["ciudad"])
    resumen = MotorDatos.resumir(
        grupos,
        [
            ("ingreso", "suma", "total"),
            ("promedio", "media", "total"),
            ("registros", "contar", None),
        ],
    )

    # Guarda CSV y cinco graficas.
    EVIDENCIAS.mkdir(parents=True, exist_ok=True)
    MotorDatos.guardar_csv(resumen, EVIDENCIAS / "resumen_ciudades.csv")
    graficar("barras", resumen, "ciudad", "ingreso", "Ingresos", EVIDENCIAS / "barras.png")
    graficar("lineas", resumen, "ciudad", "promedio", "Promedios", EVIDENCIAS / "lineas.png")
    graficar("histograma", ventas, "precio", None, "Precios", EVIDENCIAS / "histograma.png")
    graficar("dispersion", ventas, "cantidad", "precio", "Cantidad vs precio", EVIDENCIAS / "dispersion.png")
    graficar("caja", ventas, None, "precio", "Caja de precios", EVIDENCIAS / "caja.png")

    # Prueba modelos propios.
    regresion = MotorDatos.abrir_csv(RAIZ / "datos" / "regresion.csv")
    modelo = entrenar_regresion(regresion, ["metros", "habitaciones"], "precio")
    prediccion = predecir_lineal(modelo, [[90, 3]])

    clasificacion = MotorDatos.abrir_csv(RAIZ / "datos" / "clasificacion.csv")
    knn = entrenar_knn(clasificacion, ["horas_estudio", "horas_sueno"], "aprobo", 3)
    clase = predecir_knn(knn, [[7, 6]])

    clientes = MotorDatos.abrir_csv(RAIZ / "datos" / "clientes.csv")
    grupos_ml = kmeans(clientes, ["frecuencia", "ticket"], 3)

    texto = (
        f"Prediccion regresion: {prediccion}\n"
        f"Prediccion KNN: {clase}\n"
        f"Centroides KMeans: {grupos_ml['centroides']}\n"
    )
    (EVIDENCIAS / "resultados_ml.txt").write_text(texto, encoding="utf-8")
    print("Evidencias generadas en evidencias/.")


if __name__ == "__main__":
    main()
