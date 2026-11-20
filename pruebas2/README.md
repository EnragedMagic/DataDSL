# Pruebas 2: ejercicios del tablero

Los cinco ejercicios se ejecutan desde la **raíz de DataDSL** con el intérprete propio (`main.py`). No utilizan scikit-learn ni pandas.

## Ejecutar

```bash
python3 main.py pruebas2/01_factoriales.dsl
python3 main.py pruebas2/02_sigmoide.dsl
python3 main.py pruebas2/03_perceptron_xor.dsl
python3 main.py pruebas2/04_analisis_excel.dsl
python3 main.py pruebas2/05_filtro_primos.dsl
```

## Resultados

| Punto | Qué realiza | Resultado |
| --- | --- | --- |
| 1 | Calcula los factoriales del 5 al 100. | Valores impresos en terminal. |
| 2 | Evalúa y visualiza la función sigmoide. | `salidas/pruebas2_sigmoide.png` |
| 3 | Entrena un MLP para XOR, imprime probabilidades y predicciones y grafica el error de entrenamiento. | Terminal y `salidas/pruebas2_xor_error.png` |
| 4 | Analiza un Excel por columna: tipo, registros, nulos, únicos, media, mínimo y máximo cuando corresponde. | `salidas/pruebas2_eda_excel.csv` |
| 5 | Conserva solo los primos de los números de ejemplo. | `salidas/pruebas2_primos.csv` |

**Punto 4:** debes colocar el archivo original `Data.xlsx` del profesor en la raíz del repositorio; no está incluido en GitHub. El análisis utiliza la primera hoja del archivo y depende de los encabezados y datos que contenga.

**Preparación:** si todavía no se han generado Lexer, Parser y Visitor, ejecuta `bash generar_antlr.sh`. También debes instalar las dependencias de `requirements.txt`.

Estos programas aprovechan funciones ya existentes: `factorial`, `sigmoide`, `entrenar_mlp`, `predecir_mlp`, `probabilidad_mlp`, `eda` y `es_primo`. Matplotlib se utiliza para exportar las dos gráficas.
