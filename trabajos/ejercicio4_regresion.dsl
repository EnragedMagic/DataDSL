matriz datos_x := [[1], [2], [3], [4], [5]];
lista datos_y := [3, 5, 7, 9, 11];

modelo := regresion_lineal(datos_x, datos_y);
imprimir modelo;
imprimir predecir_lineal(modelo, [[6]]);
