datos := abrir "Data.xlsx";
limpios := datos
-> eliminar_nulos [edad];

graficar histograma de limpios eje_x edad titulo "Histograma de edad" como "salidas/ejercicio3_histograma.png";
