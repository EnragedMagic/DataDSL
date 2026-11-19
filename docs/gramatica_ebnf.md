# Gramática EBNF resumida

```ebnf
programa = { sentencia } ;

sentencia = declaracion, ";"
          | asignacion, ";"
          | imprimir, ";"
          | guardado, ";"
          | visualizacion, ";"
          | condicional
          | mientras
          | para
          | funcion
          | retorno, ";"
          | expresion, ";" ;

condicional = "si", "(", expresion, ")", bloque,
              [ "sino", bloque ] ;

mientras = "mientras", "(", expresion, ")", bloque ;

para = "para", identificador, "desde", expresion,
       "hasta", expresion, [ "paso", expresion ], bloque ;

funcion = "funcion", identificador, "(", [ parametros ], ")", bloque ;

flujo = identificador, paso, { paso } ;

paso = "->", seleccion
     | "->", filtro
     | "->", ordenamiento
     | "->", columna_calculada
     | "->", rellenar_nulos
     | "->", eliminar_nulos
     | "->", eliminar_duplicados
     | "->", renombrar
     | "->", convertir
     | "->", agrupacion
     | "->", resumen ;
```

El archivo completo y ejecutable está en `grammar/DataDSL.g4`.
