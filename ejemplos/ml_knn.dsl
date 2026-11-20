# Clasifica un caso nuevo y destaca sus tres vecinos cercanos.
tabla := abrir "datos/clasificacion.csv";
modelo := entrenar_knn(tabla, ["horas_estudio", "horas_sueno"], "aprobo", 3);
imprimir predecir_knn(modelo, [[7, 6]]);
imprimir graficar_knn(tabla, modelo, [7, 6], "horas_estudio", "horas_sueno", "salidas/ml_knn.png", "Clasificacion KNN");
