# Instrucciones principales

## Variables

```text
numero edad := 20;
texto nombre := "Johan";
lista valores := [1, 2, 3];
matriz m := [[1, 2], [3, 4]];
```

## Condicional

```text
si (edad >= 18) {
    imprimir "Mayor";
} sino {
    imprimir "Menor";
}
```

## Ciclos

```text
mientras (i < 5) {
    i := i + 1;
}

para i desde 1 hasta 5 {
    imprimir i;
}
```

## Función

```text
funcion cuadrado(x) {
    retornar x * x;
}
```

## Datos

```text
datos := abrir "datos/ventas.csv";

limpios := datos
-> tomar [ciudad, cantidad, precio]
-> cuando cantidad > 0
-> rellenar precio con 0
-> crear total := cantidad * precio
-> ordenar por total desc;
```

## Resumen

```text
resumen := limpios
-> agrupar por [ciudad]
-> resumir ingreso := suma(total), promedio := media(total), registros := contar();
```

## Guardado

```text
guardar resumen como "salidas/resumen.csv";
```

## Gráfica

```text
graficar barras de resumen eje_x ciudad eje_y ingreso titulo "Ingresos" como "salidas/ingresos.png";
```

## Factorial y primos

```text
imprimir factorial(5);
imprimir es_primo(17);
```

## Sigmoide

```text
imprimir sigmoide(0);
graficar_funcion("sigmoide", -10, 10, 0.2, "salidas/sigmoide.png", "Sigmoide");
```

## MLP para XOR

```text
matriz entradas := [[0, 0], [0, 1], [1, 0], [1, 1]];
lista valores_xor := [0, 1, 1, 0];
modelo_xor := entrenar_mlp(entradas, valores_xor, 2, 1, 3000);
imprimir predecir_mlp(modelo_xor, entradas);
graficar_entrenamiento(modelo_xor, "salidas/xor_error.png", "XOR");
```

## Excel y EDA

```text
datos_excel := abrir "Data.xlsx";
resumen_eda := eda(datos_excel);
imprimir resumen_eda;
guardar resumen_eda como "salidas/eda_data.csv";
```
