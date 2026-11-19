# Librerías propias

DataDSL prioriza implementaciones propias.

## Propias

- `DataTable`: tablas y CSV.
- `DataMath`: matemáticas.
- `DataStats`: estadística.
- `DataMatrix`: matrices.
- `DataRandom`: pseudoaleatorios.
- `DataFiles`: archivos de texto.
- `DataML`: Machine Learning.
- `DataGraph`: interfaz de visualización.

## Externas justificadas

### ANTLR4 Runtime

Es necesario porque el proyecto exige ANTLR4 para generar y ejecutar Lexer, Parser y Visitor base.

### Matplotlib

Solo se utiliza para convertir los datos preparados por DataDSL en imágenes PNG. La lógica de selección de datos, estadísticas y ML no depende de Matplotlib.

## No utilizadas

DataDSL no usa directamente:

- pandas;
- NumPy;
- scikit-learn;
- pytest.
