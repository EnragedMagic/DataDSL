# Caso completo de DataDSL.
datos := abrir "datos/ventas.csv";

limpios := datos
-> rellenar precio con 0
-> eliminar_duplicados
-> cuando cantidad > 0
-> crear total := cantidad * precio
-> ordenar por total desc;

si (filas(limpios) > 0) {
    imprimir "Datos preparados correctamente";
}

resumen := limpios
-> agrupar por [ciudad]
-> resumir ingreso := suma(total), promedio := media(total), registros := contar();

guardar resumen como "salidas/resumen_final.csv";

graficar barras de resumen eje_x ciudad eje_y ingreso titulo "Ingresos por ciudad" como "salidas/final_barras.png";
graficar lineas de resumen eje_x ciudad eje_y promedio titulo "Promedio por ciudad" como "salidas/final_lineas.png";
graficar histograma de limpios eje_x precio titulo "Precios" como "salidas/final_histograma.png";
graficar dispersion de limpios eje_x cantidad eje_y precio titulo "Cantidad vs precio" como "salidas/final_dispersion.png";
graficar caja de limpios eje_y precio titulo "Distribucion de precios" como "salidas/final_caja.png";

regresion := abrir "datos/regresion.csv";
modelo := entrenar_regresion(regresion, ["metros", "habitaciones"], "precio");
prediccion := predecir_lineal(modelo, [[90, 3]]);
imprimir prediccion;

clasificacion := abrir "datos/clasificacion.csv";
modelo_knn := entrenar_knn(clasificacion, ["horas_estudio", "horas_sueno"], "aprobo", 3);
imprimir predecir_knn(modelo_knn, [[7, 6]]);

clientes := abrir "datos/clientes.csv";
grupos := kmeans(clientes, ["frecuencia", "ticket"], 3);
imprimir grupos;
