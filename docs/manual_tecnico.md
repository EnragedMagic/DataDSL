# Manual técnico

## Flujo interno

1. `main.py` lee el archivo `.dsl`.
2. ANTLR crea tokens con el Lexer.
3. El Parser construye el árbol.
4. `DataDSLVisitorImpl` recorre el árbol.
5. `ContextoEjecucion` guarda símbolos.
6. `MotorDatos` coordina las operaciones tabulares.
7. `TablaDatos` almacena filas como diccionarios propios.
8. Las librerías propias ejecutan matemáticas, estadística, matrices y ML.
9. Matplotlib recibe los valores finales y renderiza PNG.

## Regenerar gramática

```bash
bash generar_antlr.sh
```

Debe ejecutarse cada vez que se modifica `grammar/DataDSL.g4`.
