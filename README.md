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

- `DataTable.py`: estructura tabular propia, sin pandas.
- `DataMath.py`: matemáticas básicas.
- `DataStats.py`: estadística descriptiva.
- `DataMatrix.py`: álgebra lineal.
- `DataRandom.py`: generador pseudoaleatorio LCG.
- `DataFiles.py`: lectura y escritura de texto.
- `DataML.py`: regresión lineal, logística, KNN, K-Means y métricas.
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
- carga y guardado CSV;
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

## Instalación en Ubuntu

```bash
cd DataDSL_Final_v2
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

También hay una auditoría del proyecto:

```bash
python3 scripts/auditar_proyecto.py
```

Y, después de generar ANTLR, se pueden validar todos los programas `.dsl`:

```bash
python3 scripts/validar_dsl.py
```

## Estructura

```text
DataDSL_Final_v2/
├── grammar/            # Gramática ANTLR
├── generated/          # Lexer, Parser y Visitor generados
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

## Explicación corta para sustentación

- **Gramática:** define cómo se escribe DataDSL.
- **Lexer:** reconoce palabras y símbolos.
- **Parser:** verifica la estructura.
- **Visitor:** interpreta las instrucciones.
- **ContextoEjecucion:** guarda variables y funciones.
- **MotorDatos:** ejecuta operaciones tabulares.
- **DataTable:** reemplaza pandas con una tabla propia.
- **DataML:** implementa algoritmos de Machine Learning.
- **DataGraph:** genera las visualizaciones PNG.

La idea es mantener cada archivo con una sola responsabilidad para que el proyecto sea fácil de explicar.
