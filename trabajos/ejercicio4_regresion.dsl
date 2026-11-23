funcion regresion_lineal_dsl(datos_x, datos_y) {
    numero n := longitud(datos_x);
    decimal suma_x := 0;
    decimal suma_y := 0;
    decimal suma_xy := 0;
    decimal suma_x2 := 0;
    numero i := 0;

    mientras (i < n) {
        suma_x := suma_x + datos_x[i];
        suma_y := suma_y + datos_y[i];
        suma_xy := suma_xy + datos_x[i] * datos_y[i];
        suma_x2 := suma_x2 + datos_x[i] * datos_x[i];
        i := i + 1;
    }

    decimal pendiente := (n * suma_xy - suma_x * suma_y) / (n * suma_x2 - suma_x * suma_x);
    decimal intercepto := (suma_y - pendiente * suma_x) / n;

    retornar [pendiente, intercepto];
}

lista datos_x := [1, 2, 3, 4, 5];
lista datos_y := [3, 5, 7, 9, 11];

modelo := regresion_lineal_dsl(datos_x, datos_y);
imprimir modelo;
