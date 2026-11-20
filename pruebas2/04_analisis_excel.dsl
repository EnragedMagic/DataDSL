# Lee Data.xlsx del profesor y exporta un resumen exploratorio por columna.
# Coloca Data.xlsx en la raiz del repositorio antes de ejecutar.
datos_excel := abrir "Data.xlsx";
resumen := eda(datos_excel);
imprimir resumen;
guardar resumen como "salidas/pruebas2_eda_excel.csv";
