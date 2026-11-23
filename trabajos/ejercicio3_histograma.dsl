texto archivo := "Data.xlsx";
texto columna := "edad";

datos := abrir_archivo(archivo);
grafica_histograma(datos, columna, "Histograma", "salidas/ejercicio3_histograma.png");
