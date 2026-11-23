funcion fibonacci(n) {
    lista serie := [];
    numero primero := 0;
    numero segundo := 1;
    numero i := 0;

    mientras (i < n) {
        serie := agregar(serie, primero);
        numero siguiente := primero + segundo;
        primero := segundo;
        segundo := siguiente;
        i := i + 1;
    }

    retornar serie;
}

numero n := 10;
imprimir fibonacci(n);
