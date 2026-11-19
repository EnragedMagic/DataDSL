# Punto 1: factoriales del 5 al 100.
para valor desde 5 hasta 100 {
    imprimir factorial(valor);
}

# Punto 5: filtra numeros primos.
datos_numeros := abrir "datos/numeros.csv";
primos := datos_numeros
-> cuando es_primo(valor);

guardar primos como "salidas/primos.csv";
imprimir primos;
