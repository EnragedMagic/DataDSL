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
