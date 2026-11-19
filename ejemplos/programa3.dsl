# Agrupa y crea estadisticas.
datos := abrir "datos/ventas.csv";

limpios := datos
-> rellenar precio con 0
-> cuando cantidad > 0
-> crear total := cantidad * precio;

resumen := limpios
-> agrupar por [ciudad]
-> resumir ingreso := suma(total), promedio := media(total), registros := contar();

guardar resumen como "salidas/resumen_ciudades.csv";

graficar barras de resumen eje_x ciudad eje_y ingreso titulo "Ingresos por ciudad" como "salidas/ingresos_ciudad.png";
