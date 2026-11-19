# Reglas semánticas

La gramática comprueba la forma de una instrucción. La semántica comprueba si esa instrucción tiene sentido al ejecutarse.

DataDSL valida, entre otros casos:

- variables no declaradas;
- columnas inexistentes;
- tipos incompatibles;
- archivos inexistentes;
- división por cero;
- operaciones tabulares sobre valores que no son tablas;
- `resumir` sin un agrupamiento previo;
- argumentos incorrectos en funciones;
- paso cero en un ciclo `para`.

Los errores sintácticos reportados por ANTLR incluyen línea y columna.
