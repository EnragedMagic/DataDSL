# Punto 3: MLP propio para XOR.
matriz entradas := [[0, 0], [0, 1], [1, 0], [1, 1]];
lista valores_xor := [0, 1, 1, 0];

modelo_xor := entrenar_mlp(entradas, valores_xor, 2, 1, 3000);
estimados := predecir_mlp(modelo_xor, entradas);

imprimir estimados;
graficar_entrenamiento(modelo_xor, "salidas/xor_error.png", "Entrenamiento XOR");
