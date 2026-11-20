datos := abrir "Data.xlsx";
limpios := datos
-> eliminar_nulos [edad, ingreso_mensual];

modelo := entrenar_regresion(limpios, ["edad"], "ingreso_mensual");
imprimir modelo;
graficar_regresion(limpios, modelo, "edad", "ingreso_mensual", "salidas/ejercicio4_regresion.png", "Regresion lineal");
