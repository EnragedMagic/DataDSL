# Filtra los numeros primos de datos/numeros.csv y guarda el resultado.
datos := abrir "datos/numeros.csv";
primos := datos -> cuando es_primo(valor);
imprimir primos;
guardar primos como "salidas/pruebas2_primos.csv";
