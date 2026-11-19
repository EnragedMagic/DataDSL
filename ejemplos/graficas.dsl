# Cinco tipos de graficas.
datos := abrir "datos/ventas.csv";

limpios := datos
-> rellenar precio con 0
-> cuando cantidad > 0
-> crear total := cantidad * precio;

resumen := limpios
-> agrupar por [ciudad]
-> resumir ingreso := suma(total), promedio := media(total);

graficar barras de resumen eje_x ciudad eje_y ingreso titulo "Barras" como "salidas/barras.png";
graficar lineas de resumen eje_x ciudad eje_y promedio titulo "Lineas" como "salidas/lineas.png";
graficar histograma de limpios eje_x precio titulo "Histograma" como "salidas/histograma.png";
graficar dispersion de limpios eje_x cantidad eje_y precio titulo "Dispersion" como "salidas/dispersion.png";
graficar caja de limpios eje_y precio titulo "Caja" como "salidas/caja.png";
