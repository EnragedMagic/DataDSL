# Agrupa clientes y dibuja sus grupos y centroides.
tabla := abrir "datos/clientes.csv";
modelo := kmeans(tabla, ["frecuencia", "ticket"], 3);
imprimir modelo;
imprimir graficar_kmeans(tabla, modelo, "frecuencia", "ticket", "salidas/ml_kmeans.png", "Segmentacion K-Means");
