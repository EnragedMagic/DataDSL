# Carga, selecciona, filtra y ordena.
datos := abrir "datos/ventas.csv";

resultado := datos
-> tomar [ciudad, producto, cantidad, precio]
-> cuando cantidad > 0
-> ordenar por precio desc;

guardar resultado como "salidas/ventas_filtradas.csv";
