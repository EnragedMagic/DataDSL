# Machine Learning con librerias propias.
matriz x := [[1], [2], [3], [4], [5]];
lista valores_y := [3, 5, 7, 9, 11];

modelo := regresion_lineal(x, valores_y);
prediccion := predecir_lineal(modelo, [[6]]);
imprimir prediccion;

matriz train_x := [[2,5], [3,6], [1,4], [7,7], [8,8], [6,7], [9,6]];
lista train_y := [0,0,0,1,1,1,1];
resultado_knn := knn(train_x, train_y, [[7,6]], 3);
imprimir resultado_knn;
