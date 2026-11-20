numero n := 10;
numero primero := 0;
numero segundo := 1;
numero i := 1;

mientras (i <= n) {
    imprimir segundo;
    numero siguiente := primero + segundo;
    primero := segundo;
    segundo := siguiente;
    i := i + 1;
}
