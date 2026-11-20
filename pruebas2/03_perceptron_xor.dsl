# Entrena un perceptron multicapa para XOR, muestra las predicciones y grafica el error.
matriz entradas := [[0, 0], [0, 1], [1, 0], [1, 1]];
lista salidas_esperadas := [0, 1, 1, 0];

modelo := entrenar_mlp(entradas, salidas_esperadas, 2, 1, 3000);
imprimir "Salidas esperadas:";
imprimir salidas_esperadas;
imprimir "Probabilidades estimadas:";
imprimir probabilidad_mlp(modelo, entradas);
imprimir "Clases estimadas:";
imprimir predecir_mlp(modelo, entradas);
graficar_entrenamiento(modelo, "salidas/pruebas2_xor_error.png", "Error de entrenamiento XOR");
