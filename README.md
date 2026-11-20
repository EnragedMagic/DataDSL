# DataDSL

**Autor:** Johan Steven Galeano González  
**Curso:** Lenguajes de Programación y Transducción  
**Universidad Sergio Arboleda**

DataDSL es un lenguaje de dominio específico orientado a ciencia de datos, estadística, visualización y Machine Learning. Usa ANTLR4 para Lexer/Parser y un Visitor en Python para ejecutar el lenguaje.

## Idea principal

```text
Programa .dsl
   ↓
Lexer ANTLR
   ↓
Parser ANTLR
   ↓
Árbol sintáctico
   ↓
Visitor
   ↓
Tabla de símbolos / MotorDatos
   ↓
Librerías propias de DataDSL
   ↓
CSV / estadísticas / ML / PNG
```

## Política de librerías

La lógica del lenguaje está implementada en módulos propios:

- `DataTable.py`: estructura tabular propia, con lectura CSV y XLSX sin pandas ni openpyxl.
- `DataMath.py`: matemáticas básicas.
- `DataStats.py`: estadística descriptiva.
- `DataMatrix.py`: álgebra lineal.
- `DataRandom.py`: generador pseudoaleatorio LCG.
- `DataFiles.py`: lectura y escritura de texto.
- `DataML.py`: regresión lineal, logística, KNN, K-Means, MLP y métricas.
- `DataGraph.py`: prepara las gráficas.

### Excepciones externas justificadas

1. **ANTLR4 Runtime:** obligatorio para ejecutar el Lexer/Parser generado.
2. **Matplotlib:** se usa únicamente como motor para dibujar y exportar las gráficas PNG.

DataDSL **no importa pandas, NumPy, scikit-learn ni pytest**.

## Funcionalidades

DataDSL soporta:

- variables tipadas;
- números, decimales, texto, booleanos, listas y matrices;
- `si / sino`;
- `mientras`;
- `para`;
- funciones y `retornar`;
- archivos de texto;
- números aleatorios;
- carga CSV y XLSX con lector propio;
- guardado CSV;
- selección y filtrado de filas;
- ordenamiento;
- columnas calculadas;
- tratamiento de nulos;
- eliminación de duplicados;
- renombrado de columnas;
- conversión de tipos;
- agrupaciones y agregaciones;
- estadísticas descriptivas;
- cinco tipos de gráficas;
- regresión lineal y logística;
- KNN y K-Means;
- perceptrón multicapa (MLP) con backpropagation;
- sigmoide pública y gráfica de entrenamiento;
- análisis exploratorio de datos (EDA);
- filtro de números primos;
- métricas de clasificación.

## Gráficas

Se incluyen cinco tipos:

```text
barras
lineas
histograma
dispersion
caja
```

Ejemplo:

```text
graficar barras de resumen
    eje_x ciudad
    eje_y ingreso
    titulo "Ingresos por ciudad"
    como "salidas/ingresos.png";
```


## Gráficas de Machine Learning

Además de los cinco tipos de gráficas normales, ahora hay ejemplos ejecutables de ML:

```bash
python3 main.py ejemplos/ml_regresion.dsl
python3 main.py ejemplos/ml_knn.dsl
python3 main.py ejemplos/ml_kmeans.dsl
```

- **Regresión lineal:** puntos y recta ajustada en `salidas/ml_regresion.png`.
- **KNN:** clases, dato nuevo y vecinos en `salidas/ml_knn.png`.
- **K-Means:** grupos y centroides en `salidas/ml_kmeans.png`.

Los archivos de `datos/` son ejemplos didácticos. Cada CSV tiene una nota de procedencia que DataDSL ignora al leer los datos.

## Pruebas 2: ejercicios del tablero

Los cinco ejercicios del tablero también están separados en [`pruebas2/`](pruebas2/README.md), con un archivo `.dsl` por punto y sus instrucciones de ejecución. El ejercicio de Excel utiliza el archivo `Data.xlsx` de ejemplo incluido en la raíz (datos ficticios, no el archivo original del profesor).

## Ejercicios del tablero

DataDSL incluye ejemplos listos para los cinco ejercicios:

```bash
python3 main.py ejemplos/tablero_factorial_primos.dsl
python3 main.py ejemplos/tablero_sigmoide.dsl
python3 main.py ejemplos/tablero_xor.dsl
```

Para el EDA de Excel, se incluye `Data.xlsx` de demostración en la raíz. Ejecuta:

```bash
python3 main.py ejemplos/tablero_excel.dsl
```

Los ejemplos cubren:

1. factoriales del 5 al 100;
2. función sigmoide y exportación PNG;
3. MLP propio para XOR con backpropagation y gráfica de error;
4. lectura `.xlsx` propia + EDA;
5. filtrado de valores primos.

La lectura XLSX se implementa directamente sobre ZIP/XML con módulos estándar de Python. No usa `openpyxl`.

## Instalación en Ubuntu

```bash
cd DataDSL
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
sudo apt install antlr4
bash generar_antlr.sh
```

La versión del runtime se mantiene en `4.9.2` para coincidir con el ANTLR disponible por `apt` en el entorno usado durante el desarrollo.

## Ejecutar

```bash
python3 main.py ejemplos/programa1.dsl
python3 main.py ejemplos/programa2.dsl
python3 main.py ejemplos/programa3.dsl
python3 main.py ejemplos/programa_final.dsl
```

O ejecutar toda la demostración:

```bash
bash demo.sh
```

## Pruebas

No se usa pytest. Las pruebas utilizan `unittest`, incluido en Python.

```bash
python3 -m unittest discover -s tests -v
```

## Estructura

```text
DataDSL/
├── grammar/            # Gramática ANTLR
├── generated/          # Archivos ANTLR generados localmente
├── src/                # Visitor, contexto, motor y errores
├── librerias/          # Librerías propias
├── datos/              # CSV de ejemplo
├── ejemplos/           # Programas .dsl
├── tests/              # Pruebas unittest
├── docs/               # Documentación
├── evidencias/         # CSV, PNG y resultados ML
├── salidas/            # Resultados de ejecución
├── main.py             # Punto de entrada
├── repl.py             # Consola interactiva
├── requirements.txt
└── generar_antlr.sh
```


- **DataML:** implementa algoritmos de Machine Learning.
- **DataGraph:** genera las visualizaciones PNG.

La idea es mantener cada archivo con una sola responsabilidad para que el proyecto sea fácil de explicar.
