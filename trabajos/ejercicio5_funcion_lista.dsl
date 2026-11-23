funcion es_primo_dsl(valor) {
    si (valor < 2) {
        retornar falso;
    }

    numero divisor := 2;

    mientras (divisor * divisor <= valor) {
        si (valor % divisor == 0) {
            retornar falso;
        }
        divisor := divisor + 1;
    }

    retornar verdadero;
}

funcion filtrar_lista(lista_datos, criterio) {
    lista resultado := [];
    numero i := 0;

    mientras (i < longitud(lista_datos)) {
        si (criterio(lista_datos[i])) {
            resultado := agregar(resultado, lista_datos[i]);
        }
        i := i + 1;
    }

    retornar resultado;
}

lista numeros := rango(1, 500);
lista primos := filtrar_lista(numeros, es_primo_dsl);
imprimir primos;
