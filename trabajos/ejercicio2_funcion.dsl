funcion uno_sobre(x) {
    retornar 1 / (1 - exponencial(x));
}

lista valores_x := [];
lista valores_y := [];
decimal actual := -5;

mientras (actual <= 5) {
    valores_x := agregar(valores_x, actual);

    si (abs(actual) > 0.0001) {
        valores_y := agregar(valores_y, uno_sobre(actual));
    } sino {
        valores_y := agregar(valores_y, indefinido());
    }

    actual := actual + 0.1;
}

grafica_xy(valores_x, valores_y, "f(x)=1/(1-e^x)", "salidas/ejercicio2_funcion.png");
