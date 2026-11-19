# Limpia y transforma datos.
datos := abrir "datos/ventas.csv";

resultado := datos
-> rellenar precio con 0
-> eliminar_nulos [cantidad]
-> eliminar_duplicados
-> crear total := cantidad * precio
-> convertir cantidad a entero
-> ordenar por total desc;

guardar resultado como "salidas/ventas_preparadas.csv";
