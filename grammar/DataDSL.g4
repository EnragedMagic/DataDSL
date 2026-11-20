// Aqui se definen las reglas y palabras que ANTLR reconoce en un archivo .dsl.
grammar DataDSL;

// Programa completo.
programa
    : sentencia* EOF
    ;

// Sentencias disponibles.
sentencia
    : declaracion FIN
    | asignacion FIN
    | imprimir FIN
    | guardado FIN
    | visualizacion FIN
    | siStmt
    | mientrasStmt
    | paraStmt
    | funcionDecl
    | retorno FIN
    | expr FIN
    ;

// Variable con tipo.
declaracion
    : tipo ID ASIGNAR expr
    ;

// Tipos principales.
tipo
    : NUMERO_T
    | ENTERO_T
    | DECIMAL_T
    | TEXTO_T
    | LOGICO_T
    | LISTA_T
    | MATRIZ_T
    ;

// Asignacion normal o tabular.
asignacion
    : ID ASIGNAR lectura
    | ID ASIGNAR flujo
    | ID ASIGNAR expr
    | ID CORCHETE_IZQ expr CORCHETE_DER ASIGNAR expr
    ;

// Carga un CSV.
lectura
    : ABRIR STRING
    ;

// Pipeline de datos.
flujo
    : ID paso+
    ;

// Transformaciones del pipeline.
paso
    : FLECHA seleccion
    | FLECHA filtro
    | FLECHA ordenamiento
    | FLECHA columnaCalculada
    | FLECHA rellenarNulos
    | FLECHA eliminarNulos
    | FLECHA eliminarDuplicados
    | FLECHA renombrarColumna
    | FLECHA convertirTipo
    | FLECHA agrupacion
    | FLECHA resumen
    ;

// Selecciona columnas.
seleccion
    : TOMAR CORCHETE_IZQ columnas CORCHETE_DER
    ;

// Lista de columnas.
columnas
    : ID (COMA ID)*
    ;

// Filtra filas.
filtro
    : CUANDO expr
    ;

// Ordena una columna.
ordenamiento
    : ORDENAR POR ID (ASC | DESC)?
    ;

// Crea una columna.
columnaCalculada
    : CREAR ID ASIGNAR expr
    ;

// Rellena valores nulos.
rellenarNulos
    : RELLENAR ID CON expr
    ;

// Elimina filas con nulos.
eliminarNulos
    : ELIMINAR_NULOS CORCHETE_IZQ columnas CORCHETE_DER
    ;

// Elimina filas repetidas.
eliminarDuplicados
    : ELIMINAR_DUPLICADOS
    ;

// Renombra una columna.
renombrarColumna
    : RENOMBRAR ID COMO ID
    ;

// Convierte tipos de columna.
convertirTipo
    : CONVERTIR ID A (NUMERO_T | ENTERO_T | DECIMAL_T | TEXTO_T | LOGICO_T)
    ;

// Agrupa por columnas.
agrupacion
    : AGRUPAR POR CORCHETE_IZQ columnas CORCHETE_DER
    ;

// Resume grupos.
resumen
    : RESUMIR agregacion (COMA agregacion)*
    ;

// Define una agregacion.
agregacion
    : ID ASIGNAR ID PAREN_IZQ ID? PAREN_DER
    ;

// Imprime una expresion.
imprimir
    : IMPRIMIR expr
    ;

// Guarda una tabla CSV.
guardado
    : GUARDAR ID COMO STRING
    ;

// Genera una grafica PNG.
visualizacion
    : GRAFICAR TIPO_GRAFICA DE ID
      (EJE_X ID)?
      (EJE_Y ID)?
      (TITULO STRING)?
      COMO STRING
    ;

// Condicional.
siStmt
    : SI PAREN_IZQ expr PAREN_DER bloque (SINO bloque)?
    ;

// Ciclo mientras.
mientrasStmt
    : MIENTRAS PAREN_IZQ expr PAREN_DER bloque
    ;

// Ciclo para inclusivo.
paraStmt
    : PARA ID DESDE expr HASTA expr (PASO expr)? bloque
    ;

// Funcion del lenguaje.
funcionDecl
    : FUNCION ID PAREN_IZQ parametros? PAREN_DER bloque
    ;

// Parametros de funcion.
parametros
    : ID (COMA ID)*
    ;

// Retorno de funcion.
retorno
    : RETORNAR expr
    ;

// Bloque de sentencias.
bloque
    : LLAVE_IZQ sentencia* LLAVE_DER
    ;

// Expresion general.
expr
    : logicaO
    ;

// Operador OR.
logicaO
    : logicaY (O logicaY)*
    ;

// Operador AND.
logicaY
    : igualdad (Y igualdad)*
    ;

// Igualdad y diferencia.
igualdad
    : comparacion ((IGUAL | DIFERENTE) comparacion)*
    ;

// Comparadores.
comparacion
    : suma ((MAYOR | MENOR | MAYOR_IGUAL | MENOR_IGUAL) suma)*
    ;

// Suma y resta.
suma
    : producto ((MAS | MENOS) producto)*
    ;

// Producto, division y modulo.
producto
    : potencia ((MULT | DIV | MOD) potencia)*
    ;

// Potencia.
potencia
    : unario (POT potencia)?
    ;

// Operadores unarios.
unario
    : (NO | MENOS) unario
    | primario
    ;

// Valores primarios.
primario
    : NUMBER
    | STRING
    | VERDADERO
    | FALSO
    | listaLiteral
    | llamada
    | ID CORCHETE_IZQ expr CORCHETE_DER
    | ID
    | PAREN_IZQ expr PAREN_DER
    ;

// Lista o matriz anidada.
listaLiteral
    : CORCHETE_IZQ (expr (COMA expr)*)? CORCHETE_DER
    ;

// Llamada a funcion.
llamada
    : ID PAREN_IZQ argumentos? PAREN_DER
    ;

// Argumentos de funcion.
argumentos
    : expr (COMA expr)*
    ;

// Datos.
ABRIR               : 'abrir';
TOMAR               : 'tomar';
CUANDO              : 'cuando';
ORDENAR             : 'ordenar';
POR                 : 'por';
ASC                 : 'asc';
DESC                : 'desc';
CREAR               : 'crear';
RELLENAR            : 'rellenar';
CON                  : 'con';
ELIMINAR_NULOS      : 'eliminar_nulos';
ELIMINAR_DUPLICADOS : 'eliminar_duplicados';
RENOMBRAR           : 'renombrar';
CONVERTIR           : 'convertir';
A                   : 'a';
AGRUPAR             : 'agrupar';
RESUMIR             : 'resumir';
GUARDAR             : 'guardar';
COMO                : 'como';

// Control.
IMPRIMIR : 'imprimir';
SI       : 'si';
SINO     : 'sino';
MIENTRAS : 'mientras';
PARA     : 'para';
DESDE    : 'desde';
HASTA    : 'hasta';
PASO     : 'paso';
FUNCION  : 'funcion';
RETORNAR : 'retornar';

// Tipos.
NUMERO_T  : 'numero';
ENTERO_T  : 'entero';
DECIMAL_T : 'decimal';
TEXTO_T   : 'texto';
LOGICO_T  : 'logico';
LISTA_T   : 'lista';
MATRIZ_T  : 'matriz';

// Graficas.
GRAFICAR     : 'graficar';
TIPO_GRAFICA : 'barras' | 'lineas' | 'histograma' | 'dispersion' | 'caja';
DE           : 'de';
EJE_X        : 'eje_x';
EJE_Y        : 'eje_y';
TITULO       : 'titulo';

// Logica.
VERDADERO : 'verdadero';
FALSO     : 'falso';
Y         : 'y';
O         : 'o';
NO        : 'no';

// Operadores.
ASIGNAR     : ':=';
IGUAL       : '==';
DIFERENTE   : '!=';
MAYOR_IGUAL : '>=';
MENOR_IGUAL : '<=';
MAYOR       : '>';
MENOR       : '<';
MAS         : '+';
MENOS       : '-';
MULT        : '*';
DIV         : '/';
MOD         : '%';
POT         : '^';
FLECHA      : '->';

// Delimitadores.
PAREN_IZQ    : '(';
PAREN_DER    : ')';
CORCHETE_IZQ : '[';
CORCHETE_DER : ']';
LLAVE_IZQ    : '{';
LLAVE_DER    : '}';
COMA         : ',';
FIN          : ';';

// Literales.
NUMBER : [0-9]+ ('.' [0-9]+)?;
STRING : '"' ( '\\' . | ~["\\\r\n] )* '"';
ID     : [a-zA-Z_][a-zA-Z0-9_]*;

// Espacios y comentarios.
WS              : [ \t\r\n]+ -> skip;
COMENTARIO      : '//' ~[\r\n]* -> skip;
COMENTARIO_HASH : '#' ~[\r\n]* -> skip;
COMENTARIO_BLOQ : '/*' .*? '*/' -> skip;
