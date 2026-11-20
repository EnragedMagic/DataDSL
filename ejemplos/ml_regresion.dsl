# Entrena una regresion y dibuja los datos y la recta del modelo.
tabla := abrir "datos/regresion.csv";
modelo := entrenar_regresion(tabla, ["metros"], "precio");
imprimir predecir_lineal(modelo, [[90]]);
imprimir graficar_regresion(tabla, modelo, "metros", "precio", "salidas/ml_regresion.png", "Precio segun metros");
